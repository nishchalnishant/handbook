"""
DL USE CASE: Seq2Seq (machine translation, summarization, chatbot pre-transformer)
Examples: EN→FR translation, headline generation

WHY Encoder-Decoder: encoder compresses input; decoder generates output token by token.
WHY attention: decoder looks at relevant encoder positions (Bahdanau attention).
Modern alternative: use transformer (llm/04_generation_finetuning.py) — mention this.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SOS_TOKEN, EOS_TOKEN, PAD_TOKEN = 1, 2, 0


class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, hidden_dim=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=PAD_TOKEN)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)
        outputs, (hidden, cell) = self.lstm(embedded)
        return outputs, hidden, cell


class Decoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, hidden_dim=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=PAD_TOKEN)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden, cell):
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded, (hidden, cell))
        return self.fc(output), hidden, cell


class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, src, tgt, teacher_forcing_ratio=0.5):
        """
        WHY teacher forcing: feed ground-truth token during training → faster convergence.
        At inference: feed model's own prediction (autoregressive).
        """
        batch_size, tgt_len = tgt.shape
        vocab_size = self.decoder.fc.out_features
        outputs = torch.zeros(batch_size, tgt_len, vocab_size, device=DEVICE)

        enc_out, hidden, cell = self.encoder(src)
        decoder_input = tgt[:, 0].unsqueeze(1)  # <SOS>

        for t in range(1, tgt_len):
            out, hidden, cell = self.decoder(decoder_input, hidden, cell)
            outputs[:, t] = out.squeeze(1)
            teacher_force = torch.rand(1).item() < teacher_forcing_ratio
            decoder_input = (tgt[:, t] if teacher_force else out.argmax(-1)).unsqueeze(1)

        return outputs


def train_step(model, src, tgt, optimizer, criterion):
    model.train()
    optimizer.zero_grad()
    output = model(src, tgt)
    loss = criterion(output[:, 1:].reshape(-1, output.size(-1)), tgt[:, 1:].reshape(-1))
    loss.backward()
    optimizer.step()
    return loss.item()


@torch.no_grad()
def translate(model, src, max_len=50, sos=SOS_TOKEN, eos=EOS_TOKEN):
    """Greedy decoding — mention beam search for better quality."""
    model.eval()
    _, hidden, cell = model.encoder(src)
    decoder_input = torch.tensor([[sos]], device=DEVICE)
    tokens = []
    for _ in range(max_len):
        out, hidden, cell = model.decoder(decoder_input, hidden, cell)
        token = out.argmax(-1).item()
        if token == eos:
            break
        tokens.append(token)
        decoder_input = torch.tensor([[token]], device=DEVICE)
    return tokens
