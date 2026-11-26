"""
============================================================
RAG (Retrieval-Augmented Generation) — Standard Workflow
============================================================
Grounds an LLM in private/up-to-date knowledge without retraining.

Pipeline:
  Documents → Chunk → Embed → Vector Store
                                    ↓
  Query ──────────── Embed → Retrieve top-k → Augment Prompt → LLM → Answer

WHY RAG over fine-tuning:
  - Knowledge changes frequently; RAG updates without retraining.
  - Fine-tuning teaches style/behaviour, not facts — LLMs still hallucinate facts.
  - RAG gives a citation trail (retrieved chunks are inspectable).
  - Faster and cheaper to update than retraining.
============================================================

# ============================================================
# Standard RAG Workflow
# ============================================================
# 1. Load Documents
#    - PDF, Markdown, HTML, database rows, API responses, etc.
# 2. Chunk Documents
#    - Split into overlapping chunks (fixed-size or semantic).
#    - Overlap ensures context is not lost at chunk boundaries.
# 3. Embed Chunks
#    - Convert each chunk to a dense vector with an embedding model.
#    - Fit-once: precompute and store; never re-embed at query time.
# 4. Build Vector Store (index)
#    - Store (embedding, chunk_text, metadata) tuples.
#    - Supports ANN (approximate nearest neighbour) search at query time.
# 5. Query Processing
#    - Embed the user query with the SAME embedding model.
#    - Retrieve top-k chunks by cosine similarity.
# 6. Augment Prompt
#    - Inject retrieved chunks as context into the LLM prompt.
# 7. Generate Answer
#    - LLM reads context + question → produces a grounded answer.
# 8. Evaluate
#    - Retrieval: recall@k, MRR, NDCG.
#    - Generation: faithfulness, answer relevancy (RAGAS framework).
# ============================================================
"""

import json
import os

import numpy as np

# pip install openai sentence-transformers chromadb langchain langchain-community langchain-openai ragas


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
CHUNK_SIZE       = 500        # characters per chunk
CHUNK_OVERLAP    = 50         # overlap to preserve context at boundaries
TOP_K            = 4          # number of chunks to retrieve per query
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"   # local; swap for "text-embedding-3-small" (OpenAI)
LLM_MODEL        = "gpt-4o-mini"
VECTOR_STORE_DIR = "./chroma_db"
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY", "")


# ============================================================
# APPROACH A: From-Scratch (no LangChain)
# ============================================================
# Walk through this in interviews to show you understand the internals
# that LangChain/LlamaIndex abstract away.


# ------------------------------------------------------------
# 1. Chunking
# ------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Fixed-size character chunking with overlap.
    WHY overlap: a fact split across a boundary would be lost without it.
    WHY recursive splitters (LangChain) are better: they respect paragraph/
    sentence boundaries before falling back to characters — fewer mid-sentence cuts.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap   # slide forward, keeping 'overlap' chars
    return chunks


def chunk_documents(documents: list[str], chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Chunk a list of documents. In production use:
    langchain.text_splitter.RecursiveCharacterTextSplitter for smarter splits."""
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunk_text(doc, chunk_size, overlap))
    return all_chunks


# ------------------------------------------------------------
# 2. Embedding
# ------------------------------------------------------------
def load_embedding_model(model_name: str = EMBEDDING_MODEL):
    """Load a sentence-transformer embedding model.
    WHY same model for chunks AND queries: embedding space must match.
    WHY not OpenAI embeddings: sentence-transformers runs locally, no API cost.
    """
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)


def embed_chunks(chunks: list[str], model) -> np.ndarray:
    """Returns (N, D) float32 array — one embedding per chunk.
    In production: batch embed, cache to disk, reload on restart."""
    return model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
    # normalize_embeddings=True → cosine similarity becomes a dot product (faster)


# ------------------------------------------------------------
# 3. Vector Store (in-memory for scratch implementation)
# ------------------------------------------------------------
def build_index(chunks: list[str], embeddings: np.ndarray) -> dict:
    """Simple dict-based index. In production replace with:
    - ChromaDB / FAISS (local)
    - Pinecone / Weaviate / Qdrant (managed cloud)
    """
    return {"chunks": chunks, "embeddings": embeddings}


def retrieve(query: str, index: dict, model, top_k: int = TOP_K) -> list[str]:
    """Embed query → cosine similarity → top-k chunks.
    WHY cosine: measures directional similarity, not magnitude.
    Cosine(q, c) = q · c  (when both are L2-normalised, which we did above).
    """
    q_emb = model.encode(query, normalize_embeddings=True)          # (D,)
    scores = index["embeddings"] @ q_emb                            # (N,) dot products = cosine sim
    top_idx = np.argsort(scores)[::-1][:top_k]                     # descending
    return [index["chunks"][i] for i in top_idx]


# ------------------------------------------------------------
# 4. Prompt construction
# ------------------------------------------------------------
RAG_PROMPT_TEMPLATE = """You are a helpful assistant. Answer using ONLY the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}

Answer:"""

def build_prompt(question: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(retrieved_chunks)
    return RAG_PROMPT_TEMPLATE.format(context=context, question=question)


# ------------------------------------------------------------
# 5. Generation
# ------------------------------------------------------------
def generate_answer(prompt: str, model: str = LLM_MODEL, api_key: str = OPENAI_API_KEY) -> str:
    """Call an LLM with the augmented prompt.
    WHY temperature=0: factual Q&A — we want the most deterministic answer.
    """
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content


def rag_query_scratch(question: str, index: dict, embed_model, top_k: int = TOP_K) -> str:
    """Full RAG pipeline in one function — walk through this in interviews."""
    retrieved = retrieve(question, index, embed_model, top_k)
    prompt = build_prompt(question, retrieved)
    return generate_answer(prompt)


# ============================================================
# APPROACH B: LangChain (production pattern)
# ============================================================
# Shows you know the production tooling. Reference implementation only
# (not run in main() to avoid mandatory langchain install for scratch demo).

def build_langchain_rag(documents: list[str]):
    """
    Production RAG with LangChain.
    Key decisions:
      - RecursiveCharacterTextSplitter: smarter chunking (paragraph → sentence → char).
      - HuggingFaceEmbeddings: local model, no API cost for embedding.
      - Chroma: persistent local vector store, easy to swap for Pinecone.
      - RetrievalQA: handles the retrieve → augment → generate loop.
      - temperature=0: deterministic factual answers.
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_openai import ChatOpenAI
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate

    # Chunk
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_text("\n\n".join(documents))

    # Embed + store
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma.from_texts(chunks, embeddings, persist_directory=VECTOR_STORE_DIR)

    # Chain
    prompt = PromptTemplate(
        template=RAG_PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,   # useful for citations
    )
    return chain


def query_langchain_rag(chain, question: str) -> dict:
    result = chain.invoke({"query": question})
    return {
        "answer": result["result"],
        "sources": [doc.page_content[:100] for doc in result["source_documents"]],
    }


# ============================================================
# APPROACH C: Advanced RAG Patterns (mention in interviews)
# ============================================================
# --- Hybrid Search (keyword + semantic) ---
# Problem: dense retrieval misses exact keyword matches (e.g., product codes).
# Solution: combine BM25 (keyword) + cosine (semantic) scores.
# from langchain.retrievers import EnsembleRetriever, BM25Retriever
# bm25 = BM25Retriever.from_texts(chunks)
# dense = vectorstore.as_retriever()
# hybrid = EnsembleRetriever(retrievers=[bm25, dense], weights=[0.4, 0.6])

# --- Re-ranking ---
# Problem: top-k by embedding similarity ≠ most relevant for the LLM.
# Solution: retrieve top-20 cheap, re-rank with a cross-encoder, pass top-5 to LLM.
# from sentence_transformers import CrossEncoder
# reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
# pairs = [(question, chunk) for chunk in retrieved_20]
# scores = reranker.predict(pairs)
# top5 = [retrieved_20[i] for i in np.argsort(scores)[::-1][:5]]

# --- Contextual Compression ---
# Problem: retrieved chunks contain irrelevant sentences that dilute the answer.
# Solution: LLM compresses each chunk to only the relevant sentences before prompting.
# from langchain.retrievers.document_compressors import LLMChainExtractor
# from langchain.retrievers import ContextualCompressionRetriever


# ============================================================
# Evaluation (RAGAS)
# ============================================================
def evaluate_rag(questions: list[str], ground_truths: list[str], chain) -> dict:
    """
    RAGAS evaluates 4 things:
      - faithfulness:        is the answer supported by the retrieved context?
      - answer_relevancy:    does the answer address the question?
      - context_precision:   how many retrieved chunks are relevant?
      - context_recall:      were all relevant facts retrieved?

    All metrics score 0–1; higher is better.
    """
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
    from datasets import Dataset

    rows = []
    for q, gt in zip(questions, ground_truths):
        result = query_langchain_rag(chain, q)
        rows.append({
            "question": q,
            "answer": result["answer"],
            "contexts": result["sources"],
            "ground_truth": gt,
        })

    dataset = Dataset.from_list(rows)
    scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
    print(scores)
    return scores


# ============================================================
# Demo (scratch implementation — no API key needed)
# ============================================================
def main() -> None:
    # --- Synthetic documents (replace with real docs) ---
    documents = [
        "PyTorch is an open-source deep learning framework developed by Meta AI. "
        "It uses dynamic computation graphs, making debugging easier than TensorFlow's static graphs.",

        "RAG (Retrieval-Augmented Generation) combines information retrieval with LLMs. "
        "It retrieves relevant documents and injects them into the prompt context before generation.",

        "Transformers use self-attention to compute relationships between all tokens in parallel. "
        "The attention score is computed as softmax(QK^T / sqrt(d_k)) * V.",

        "Fine-tuning adapts a pretrained model on a downstream task. "
        "LoRA (Low-Rank Adaptation) injects trainable rank-decomposition matrices, "
        "reducing trainable parameters by 10000x vs full fine-tuning.",
    ]

    print("=== RAG Scratch Demo ===")

    # 1. Chunk
    chunks = chunk_documents(documents)
    print(f"Documents: {len(documents)} → Chunks: {len(chunks)}")

    # 2. Embed
    embed_model = load_embedding_model()
    embeddings = embed_chunks(chunks, embed_model)
    print(f"Embedding shape: {embeddings.shape}")   # (N, 384) for MiniLM

    # 3. Index
    index = build_index(chunks, embeddings)

    # 4. Retrieve (no LLM needed to test retrieval)
    question = "What is RAG and why is it used?"
    retrieved = retrieve(question, index, embed_model, top_k=2)
    print(f"\nQuestion: {question}")
    print(f"Retrieved chunks:")
    for i, chunk in enumerate(retrieved, 1):
        print(f"  [{i}] {chunk[:120]}...")

    # 5. Build prompt (show what the LLM receives)
    prompt = build_prompt(question, retrieved)
    print(f"\nPrompt sent to LLM:\n{prompt}\n")

    # 6. Generate (comment out if no API key)
    if OPENAI_API_KEY:
        answer = generate_answer(prompt)
        print(f"Answer: {answer}")
    else:
        print("(Set OPENAI_API_KEY to test LLM generation)")


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use RAG:
#   - Private/proprietary knowledge (internal docs, product manuals).
#   - Frequently updated knowledge (news, pricing, inventory).
#   - Need citations/auditability (retrieved chunks are inspectable).
#
# RAG vs Fine-tuning vs Prompt Engineering:
#   - Prompt engineering: no new knowledge, fast, cheap → good for format/behaviour.
#   - RAG: inject new knowledge at inference time → best for factual grounding.
#   - Fine-tuning: teaches style/reasoning patterns, not facts → combine with RAG.
#
# Critical failure modes (common interview question):
#   1. Retrieval failure: correct chunk never in top-k.
#      → Diagnose: log retrieval recall on labeled eval set.
#      → Fix: better chunking, hybrid search (BM25 + dense), re-ranking.
#   2. Generation failure: correct chunk retrieved but wrong answer.
#      → Diagnose: "lost in the middle" (LLMs attend more to start/end of context).
#      → Fix: reorder chunks with most relevant last; explicit "answer from context only" prompt.
#   3. Context window overflow: too many chunks exceed the LLM's token limit.
#      → Fix: reduce top_k, compression retriever, map-reduce chain.
#   4. Embedding mismatch: different model used at index vs query time.
#      → Fix: persist and reload embedding model name alongside the index.
#   5. Chunking destroys context: table split across chunks, pronoun without referent.
#      → Fix: semantic chunking, add metadata (doc title, section header) to each chunk.
#
# Metrics:
#   - Retrieval: recall@k, MRR (mean reciprocal rank), NDCG.
#   - Generation (RAGAS): faithfulness, answer_relevancy, context_precision, context_recall.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# Conversational RAG: maintain chat history, rephrase query with history
#   before retrieval (ConversationalRetrievalChain in LangChain).
# Agentic RAG: LLM decides whether to retrieve, what to query, and
#   iterates over multiple retrieval rounds (ReAct agent + RAG tool).
# Multi-modal RAG: embed and retrieve images alongside text
#   (CLIP embeddings for images + ColPali for PDF page images).
# GraphRAG (Microsoft): build a knowledge graph from documents;
#   traverse graph relationships for richer context than flat chunk retrieval.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: LLM needs private/fresh knowledge it wasn't trained on.
# Key decisions: chunk size, overlap, embedding model, top_k, LLM temperature.
# Key failure modes: retrieval recall, lost-in-the-middle, chunking destroying context.
# Evaluation: RAGAS (faithfulness, relevancy, precision, recall).
# Production stack: chunking → embedding → Chroma/Pinecone → retrieve → LLM.
# Common mistakes:
#   - Using different embedding model at index and query time.
#   - Fitting/transforming text with LLM-specific tokenizer before embedding.
#   - Retrieving chunks with cosine similarity but ignoring metadata filters.
#   - Not evaluating retrieval and generation stages separately.
# ============================================================
