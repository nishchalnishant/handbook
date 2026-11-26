"""
LLM imports cheat sheet — copy-paste the block you need.
"""

# --- HuggingFace core ---
from transformers import (
    AutoTokenizer,
    AutoModel,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    AutoModelForSeq2SeqLM,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    pipeline,
)

# --- Fine-tuning ---
from peft import LoraConfig, get_peft_model, PeftModel
from datasets import Dataset

# --- Embeddings ---
from sentence_transformers import SentenceTransformer, util

# --- RAG / Agents ---
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma, FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import AgentExecutor, create_react_agent

# --- MCP ---
from mcp.server.fastmcp import FastMCP

# --- Eval ---
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# --- OpenAI ---
from openai import OpenAI

# --- Production ---
import torch
import json
from fastapi import FastAPI
from pydantic import BaseModel
