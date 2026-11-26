"""
LLM USE CASE: RAG (Retrieval-Augmented Generation)
Examples: internal knowledge base Q&A, support bot, doc chat

WHY RAG: grounds LLM in your private data → reduces hallucination.
WHY not fine-tune alone: knowledge changes frequently; RAG updates without retraining.
Pipeline: chunk docs → embed → store → retrieve top-k → inject into prompt → generate.
"""

from dataclasses import dataclass

# pip install langchain langchain-community chromadb sentence-transformers openai


@dataclass
class RAGConfig:
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 4
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "gpt-4o-mini"  # or local: "llama3", "mistral"
    vector_store_path: str = "./chroma_db"


def chunk_documents(texts: list[str], chunk_size: int, overlap: int) -> list[str]:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " "],  # WHY recursive: respects paragraph/sentence boundaries
    )
    return splitter.split_text("\n\n".join(texts))


def build_vector_store(chunks: list[str], config: RAGConfig):
    """
    WHY Chroma/FAISS/Pinecone: fast similarity search over millions of vectors.
    Chroma = local dev; Pinecone = managed production.
    """
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(model_name=config.embedding_model)
    vectorstore = Chroma.from_texts(chunks, embeddings, persist_directory=config.vector_store_path)
    return vectorstore


def build_rag_chain(vectorstore, config: RAGConfig):
    from langchain_openai import ChatOpenAI
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate

    template = """Use ONLY the context below to answer. If unsure, say "I don't know."

Context:
{context}

Question: {question}
Answer:"""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    llm = ChatOpenAI(model=config.llm_model, temperature=0)  # WHY temp=0: factual Q&A

    retriever = vectorstore.as_retriever(search_kwargs={"k": config.top_k})
    return RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, chain_type_kwargs={"prompt": prompt}
    )


def query_rag(question: str, chain) -> str:
    return chain.invoke({"query": question})["result"]


# --- Minimal RAG without LangChain (show you understand internals) ---
def minimal_rag(question: str, chunks: list[str], embed_model, llm_client):
    """Interview: walk through this to show you know what LangChain abstracts."""
    import numpy as np

    # 1. Embed all chunks (precomputed in prod)
    chunk_embs = embed_model.encode(chunks)
    q_emb = embed_model.encode(question)

    # 2. Retrieve top-k by cosine similarity
    scores = chunk_embs @ q_emb / (np.linalg.norm(chunk_embs, axis=1) * np.linalg.norm(q_emb))
    top_idx = scores.argsort()[-4:][::-1]
    context = "\n".join(chunks[i] for i in top_idx)

    # 3. Augment prompt
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    return llm_client.generate(prompt)  # OpenAI / local LLM
