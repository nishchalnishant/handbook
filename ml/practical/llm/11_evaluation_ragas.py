"""
LLM USE CASE: Evaluation (RAGAS + custom metrics)
Examples: evaluate RAG quality, compare prompts, benchmark before deploy

WHY evaluate: LLM outputs are non-deterministic; need systematic quality checks.
WHY RAGAS: standard metrics for RAG (faithfulness, relevancy, context precision).
"""

import json
from dataclasses import dataclass

# pip install ragas datasets


@dataclass
class EvalSample:
    question: str
    answer: str
    contexts: list[str]
    ground_truth: str | None = None


# --- 1. RAGAS metrics (for RAG pipelines) ---
def evaluate_rag(samples: list[EvalSample]):
    """
    Metrics:
    - faithfulness: is answer grounded in retrieved context? (no hallucination)
    - answer_relevancy: does answer address the question?
    - context_precision: are retrieved chunks actually relevant?
    - context_recall: did we retrieve all needed info?
    """
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

    dataset = Dataset.from_dict({
        "question": [s.question for s in samples],
        "answer": [s.answer for s in samples],
        "contexts": [s.contexts for s in samples],
        "ground_truth": [s.ground_truth or "" for s in samples],
    })

    return evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])


# --- 2. Classification metrics (after fine-tuning) ---
def evaluate_classifier(y_true, y_pred, y_proba=None):
    from sklearn.metrics import classification_report, f1_score, roc_auc_score
    print(classification_report(y_true, y_pred))
    if y_proba is not None:
        print("ROC-AUC:", roc_auc_score(y_true, y_proba))


# --- 3. LLM-as-judge (common in interviews) ---
JUDGE_PROMPT = """Rate the answer on a scale of 1-5 for correctness and helpfulness.

Question: {question}
Ground truth: {ground_truth}
Answer: {answer}

Return JSON: {{"score": <1-5>, "reasoning": "<brief explanation>"}}"""


def llm_judge(question: str, answer: str, ground_truth: str, llm) -> dict:
    """WHY LLM judge: automatic eval when no exact match (open-ended generation)."""
    response = llm.generate(JUDGE_PROMPT.format(
        question=question, ground_truth=ground_truth, answer=answer
    ))
    return json.loads(response)


# --- 4. A/B test two prompts ---
def ab_test_prompt(prompt_a: str, prompt_b: str, test_cases: list[str], llm, judge_llm):
    results = {"a": [], "b": []}
    for case in test_cases:
        ans_a = llm.generate(prompt_a.format(input=case))
        ans_b = llm.generate(prompt_b.format(input=case))
        results["a"].append(llm_judge(case, ans_a, "", judge_llm)["score"])
        results["b"].append(llm_judge(case, ans_b, "", judge_llm)["score"])
    print(f"Prompt A avg: {sum(results['a'])/len(results['a']):.2f}")
    print(f"Prompt B avg: {sum(results['b'])/len(results['b']):.2f}")
