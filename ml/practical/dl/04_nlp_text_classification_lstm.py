"""
DL USE CASE: NLP Text Classification with LSTM (pre-transformer approach)
Examples: sentiment analysis, spam detection, intent classification

WHY LSTM: captures sequential context; still valid for small data / edge deployment.
WHY embeddings: convert tokens to dense vectors (trainable or pretrained GloVe/FastText).
WHEN to use BERT instead: more data, need SOTA — see llm/01_nlp_text_classification.py
"""

import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence
from torch.utils.data import DataLoader, Dataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TextDataset(Dataset):
    def __init__(self, texts: list[str], labels: list[int], vocab: dict):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        tokens = self.texts[idx].lower().split()
        ids = [self.vocab.get(t, self.vocab["<UNK>"]) for t in tokens]
        return torch.tensor(ids, dtype=torch.long), torch.tensor(self.labels[idx])


def build_vocab(texts: list[str], min_freq: int = 2) -> dict:
    from collections import Counter
    counts = Counter()
    for text in texts:
        counts.update(text.lower().split())
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for word, count in counts.items():
        if count >= min_freq:
            vocab[word] = len(vocab)
    return vocab


def collate_fn(batch):
    """WHY pad_sequence: sentences have variable length; pad to max in batch."""
    sequences, labels = zip(*batch)
    lengths = torch.tensor([len(s) for s in sequences])
    padded = pad_sequence(sequences, batch_first=True, padding_value=0)
    return padded, lengths, torch.tensor(labels)


class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int = 128, hidden_dim: int = 256, num_classes: int = 2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        # WHY bidirectional: context from both directions improves classification
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x, lengths):
        embedded = self.embedding(x)
        packed = pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
        _, (hidden, _) = self.lstm(packed)
        # concat forward + backward final hidden states
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
        return self.fc(hidden)


def train_epoch(model, loader, optimizer, criterion):
    model.train()
    for x, lengths, y in loader:
        x, y = x.to(DEVICE), y.to(DEVICE)
        optimizer.zero_grad()
        loss = criterion(model(x, lengths), y)
        loss.backward()
        optimizer.step()


def train(texts, labels, vocab, epochs: int = 10):
    ds = TextDataset(texts, labels, vocab)
    loader = DataLoader(ds, batch_size=32, shuffle=True, collate_fn=collate_fn)
    model = LSTMClassifier(vocab_size=len(vocab)).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        train_epoch(model, loader, optimizer, criterion)
        print(f"Epoch {epoch + 1} done")
    return model
