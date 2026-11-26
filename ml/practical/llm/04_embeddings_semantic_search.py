"""
LLM USE CASE: Embeddings + Semantic Search
Examples: document search, duplicate detection, recommendation, RAG retrieval step

WHY embeddings: map text to vectors where semantic similarity = cosine distance.
WHY sentence-transformers: purpose-built for semantic similarity (better than raw BERT CLS).
"""

import numpy as np
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"  # fast, 384-dim; alt: "BAAI/bge-small-en-v1.5"


def build_index(documents: list[str], model_name: str = MODEL_NAME):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(documents, convert_to_tensor=True, show_progress_bar=True)
    return model, embeddings, documents


def semantic_search(query: str, model, doc_embeddings, documents: list[str], top_k: int = 5):
    query_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, doc_embeddings)[0]
    top_results = scores.topk(top_k)
    return [
        {"document": documents[idx], "score": float(scores[idx])}
        for idx in top_results.indices
    ]


# --- Alternative: raw HuggingFace embeddings ---
def embed_with_hf(texts: list[str], model_name="sentence-transformers/all-MiniLM-L6-v2"):
    from transformers import AutoTokenizer, AutoModel
    import torch

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    @torch.no_grad()
    def embed(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        # WHY mean pooling: average all token embeddings (better than CLS alone)
        return outputs.last_hidden_state.mean(dim=1).numpy()

    return [embed(t) for t in texts]


def chunk_documents(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    WHY chunking: embedding models have max length; long docs need splitting for RAG.
    WHY overlap: prevents losing context at chunk boundaries.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks
