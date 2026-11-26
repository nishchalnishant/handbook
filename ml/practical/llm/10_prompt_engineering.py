"""
LLM USE CASE: Prompt Engineering patterns
Use when: no fine-tuning budget, quick prototype, or augmenting RAG/agents
"""

from dataclasses import dataclass


@dataclass
class PromptTemplate:
    system: str
    user: str


# --- 1. Zero-shot ---
ZERO_SHOT = PromptTemplate(
    system="You are a helpful assistant.",
    user="Classify this review as Positive or Negative:\n\n{review}",
)


# --- 2. Few-shot (in-context learning) ---
FEW_SHOT = """Classify sentiment as Positive or Negative.

Review: The food was amazing!
Sentiment: Positive

Review: Terrible service, never coming back.
Sentiment: Negative

Review: {review}
Sentiment:"""


# --- 3. Chain-of-Thought (CoT) ---
# WHY: forces step-by-step reasoning → better on math, logic, multi-hop QA
COT_PROMPT = """Solve step by step.

Question: {question}

Let's think step by step:"""


# --- 4. Structured output (JSON mode) ---
STRUCTURED_OUTPUT = """Extract entities from the text. Return ONLY valid JSON.

Text: {text}

JSON schema:
{{"persons": [], "organizations": [], "dates": []}}"""


# --- 5. Role-based system prompt ---
SYSTEM_PROMPTS = {
    "coder": "You are an expert Python developer. Write clean, tested code. Explain trade-offs.",
    "analyst": "You are a data analyst. Use numbers and cite sources. Flag uncertainty.",
    "support": "You are a customer support agent. Be empathetic, concise, and escalate when needed.",
}


# --- 6. Self-consistency (mention in interview) ---
def self_consistency(question: str, llm, n_samples: int = 5) -> str:
    """
    WHY: sample multiple reasoning paths, take majority vote → reduces errors.
    Cost: n_samples × inference cost.
    """
    answers = [llm.generate(COT_PROMPT.format(question=question), temperature=0.7) for _ in range(n_samples)]
    from collections import Counter
    return Counter(answers).most_common(1)[0][0]


# --- 7. Prompt chaining ---
def prompt_chain(document: str, llm) -> dict:
    """
    WHY chain: complex task → break into steps (summarize → extract → classify).
    Each step gets focused prompt → higher quality than one giant prompt.
    """
    summary = llm.generate(f"Summarize:\n{document}")
    entities = llm.generate(f"Extract key entities from:\n{summary}")
    category = llm.generate(f"Classify this summary into [Legal, Technical, Financial]:\n{summary}")
    return {"summary": summary, "entities": entities, "category": category}
