"""
LLM USE CASE: Production Serving
Covers: FastAPI, batching, quantization, vLLM, caching, guardrails
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="LLM Production API")


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=4000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    tokens_used: int
    model: str


class RAGRequest(BaseModel):
    question: str
    top_k: int = 4


# Load models at startup
@app.on_event("startup")
def load_models():
    global classifier, rag_chain
    # from transformers import pipeline
    # classifier = pipeline("text-classification", model="./models/text_classifier")
    # rag_chain = build_rag_chain(...)  # from 05_rag_pipeline.py
    pass


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify")
def classify(req: ChatRequest):
    # result = classifier(req.message)[0]
    return {"label": "positive", "score": 0.95}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Production checklist:
    - rate limiting (per user/IP)
    - input sanitization (prompt injection defense)
    - output filtering (PII, toxicity)
    - log prompts + responses for audit
    - cache frequent queries (Redis)
    """
    # reply = rag_chain.invoke({"query": req.message})
    return ChatResponse(reply="placeholder", tokens_used=150, model="gpt-4o-mini")


@app.post("/rag")
def rag_query(req: RAGRequest):
    # return query_rag(req.question, rag_chain)
    return {"answer": "placeholder", "sources": []}


# --- High-throughput alternative ---
def serve_with_vllm():
    """
    WHY vLLM: PagedAttention + continuous batching → 10-20x throughput.
    from vllm import LLM, SamplingParams
    llm = LLM(model="meta-llama/Llama-3.2-1B", quantization="awq")
    params = SamplingParams(temperature=0, max_tokens=512)
    outputs = llm.generate(["Hello!"], params)
    """
    pass


# uvicorn llm.12_production_serving:app --port 8002
