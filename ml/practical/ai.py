"""
============================================================
MCP Server — Standard Workflow
============================================================
1. Initialise server — FastMCP("server-name")
2. Register Tools     — @mcp.tool() functions the LLM can invoke
3. Register Resources — @mcp.resource("uri") read-only data
4. Register Prompts   — @mcp.prompt() reusable templates
5. Run                — mcp.run() (stdio) or transport="sse" (remote)
"""

import json
import sqlite3
from datetime import datetime

# pip install mcp
from mcp.server.fastmcp import FastMCP

SERVER_NAME = "interview-demo-server"
DB_PATH = ":memory:"
MAX_ROWS = 100

mcp = FastMCP(name=SERVER_NAME)


@mcp.tool()
def search_knowledge_base(query: str, top_k: int = 5) -> str:
    """Search the internal knowledge base by semantic similarity."""
    top_k = max(1, min(top_k, 20))          # clamp: never trust LLM-provided numbers
    results = [
        {"title": "Q3 Earnings Report", "snippet": f"Content matching '{query}'...", "score": 0.92},
        {"title": "Product FAQ", "snippet": f"Answer about '{query}'...", "score": 0.87},
    ]
    return json.dumps(results[:top_k])


@mcp.tool()
def run_sql(query: str) -> str:
    """Execute a read-only SQL SELECT query."""
    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed."})
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchmany(MAX_ROWS)       # cap rows to avoid context overflow
        return json.dumps({"columns": columns, "rows": rows})
    except sqlite3.Error as e:
        return json.dumps({"error": str(e)})
    finally:
        con.close()


@mcp.resource("data://schema/tables")
def get_db_schema() -> str:
    """Database schema — agent reads this to construct valid SQL queries."""
    schema = {"users": ["id INT", "name TEXT", "email TEXT"]}
    return json.dumps(schema, indent=2)


@mcp.prompt()
def analyze_dataset(dataset_name: str, goal: str = "identify trends and anomalies") -> str:
    """Generate a structured data analysis prompt."""
    return f"""Analyse the dataset '{dataset_name}'.
Your goal: {goal}
Structure your response as: Summary, Key Trends, Anomalies, Recommendations."""


if __name__ == "__main__":
    mcp.run()   # defaults to stdio; set transport="sse" in FastMCP() for remote


####################################################################################################################################


"""
============================================================
RAG — Standard Workflow
============================================================
Documents -> Chunk -> Embed -> Vector Store
Query -> Embed -> Retrieve top-k -> Augment Prompt -> LLM -> Answer
"""

import numpy as np

# pip install sentence-transformers openai

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "gpt-4o-mini"


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Fixed-size character chunking with overlap so a fact split across a
    boundary isn't lost."""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks


def load_embedding_model(model_name: str = EMBEDDING_MODEL):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)


def embed_chunks(chunks: list[str], model) -> np.ndarray:
    # normalize_embeddings=True -> cosine similarity becomes a dot product
    return model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)


def build_index(chunks: list[str], embeddings: np.ndarray) -> dict:
    return {"chunks": chunks, "embeddings": embeddings}


def retrieve(query: str, index: dict, model, top_k: int = TOP_K) -> list[str]:
    q_emb = model.encode(query, normalize_embeddings=True)
    scores = index["embeddings"] @ q_emb            # dot product = cosine sim (both normalized)
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [index["chunks"][i] for i in top_idx]


RAG_PROMPT_TEMPLATE = """You are a helpful assistant. Answer using ONLY the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}

Answer:"""


def build_prompt(question: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(retrieved_chunks)
    return RAG_PROMPT_TEMPLATE.format(context=context, question=question)


def generate_answer(prompt: str, model: str = LLM_MODEL) -> str:
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,   # deterministic for factual Q&A
    )
    return response.choices[0].message.content


def rag_query(question: str, index: dict, embed_model, top_k: int = TOP_K) -> str:
    retrieved = retrieve(question, index, embed_model, top_k)
    prompt = build_prompt(question, retrieved)
    return generate_answer(prompt)


def main() -> None:
    documents = [
        "PyTorch is an open-source deep learning framework developed by Meta AI.",
        "RAG combines information retrieval with LLMs to ground answers in retrieved context.",
    ]
    chunks = [c for doc in documents for c in chunk_text(doc)]
    embed_model = load_embedding_model()
    embeddings = embed_chunks(chunks, embed_model)
    index = build_index(chunks, embeddings)

    question = "What is RAG and why is it used?"
    retrieved = retrieve(question, index, embed_model, top_k=2)
    prompt = build_prompt(question, retrieved)
    print(prompt)


if __name__ == "__main__":
    main()


####################################################################################################################################


"""
============================================================
scikit-learn — Standard Workflow
============================================================
Split -> ColumnTransformer (num/cat) -> Pipeline -> CV -> GridSearchCV
-> fit + evaluate once on test -> persist
"""

import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# 1. Load
df = pd.read_csv("data.csv")
X, y = df.drop(columns=["target"]), df["target"]

# 2. Quick EDA (before modeling)
# df.info(); df["target"].value_counts(normalize=True); df.isna().sum()

# 3. Split FIRST — before any fitting/statistics touch the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 4. Preprocessing, split by column type
numeric_features = X.select_dtypes(include="number").columns.tolist()
categorical_features = X.select_dtypes(exclude="number").columns.tolist()

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), numeric_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical_features),
])

# 5. Full pipeline: preprocessing + model bundled so CV/search refit both per fold
pipe = Pipeline([
    ("preprocess", preprocessor),
    ("clf", RandomForestClassifier(class_weight="balanced", random_state=42)),
])

# 6. Cross-validate on train only, before touching test
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1_macro", n_jobs=-1)
print(f"CV f1_macro: {scores.mean():.3f} +/- {scores.std():.3f}")

# 7. (Optional) hyperparameter search — same cv splitter as above for comparability
param_grid = {
    "clf__n_estimators": [200, 400],
    "clf__max_depth": [None, 10, 20],
}
search = GridSearchCV(pipe, param_grid, cv=cv, scoring="f1_macro", n_jobs=-1)
search.fit(X_train, y_train)
best_pipe = search.best_estimator_

# 8. Final fit + evaluate ONCE on held-out test set
best_pipe.fit(X_train, y_train)
preds = best_pipe.predict(X_test)
proba = best_pipe.predict_proba(X_test)[:, 1]

print(classification_report(y_test, preds))
print("ROC-AUC:", roc_auc_score(y_test, proba))

# 9. Persist
joblib.dump(best_pipe, "model.pkl")
# reload: joblib.load("model.pkl").predict(new_X)


####################################################################################################################################


"""
============================================================
PyTorch — Standard Workflow
============================================================
Data -> Model -> Loss/Optimizer/Scheduler -> Train/Val loop
-> checkpoint best -> reload for inference
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

num_classes = 10   # set to actual number of classes
num_epochs = 10    # set to desired epoch count

# 1. Data
train_tf = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
val_tf = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

train_ds = datasets.ImageFolder("data/train", transform=train_tf)
val_ds = datasets.ImageFolder("data/val", transform=val_tf)
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=4)

# 2. Model — replace final layer to match num_classes
model = models.resnet18(weights="DEFAULT")
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.to(device)

# 3. Loss / Optimizer / Scheduler
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

# 4. Train / validate loop
best_acc = 0.0
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        preds = model(xb)
        loss = criterion(preds, yb)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * xb.size(0)
    scheduler.step()
    train_loss = running_loss / len(train_ds)

    model.eval()
    correct = 0
    with torch.no_grad():
        for xb, yb in val_loader:
            xb, yb = xb.to(device), yb.to(device)
            preds = model(xb)
            correct += (preds.argmax(1) == yb).sum().item()
    val_acc = correct / len(val_ds)

    print(f"epoch {epoch}: train_loss={train_loss:.4f} val_acc={val_acc:.4f}")

    if val_acc > best_acc:
        best_acc = val_acc
        torch.save(model.state_dict(), "best_model.pt")

# 5. Inference
model.load_state_dict(torch.load("best_model.pt"))
model.eval()
single_image = val_ds[0][0]   # replace with real preprocessed image tensor [C, H, W]
with torch.no_grad():
    output = model(single_image.unsqueeze(0).to(device))
    pred_class = output.argmax(1).item()
