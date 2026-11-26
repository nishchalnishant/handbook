"""
Reference implementation: image moderation service for player chat.

This is the ~most likely thing you'll be asked to code in round 3.
Practice writing this FROM SCRATCH in under 30 minutes while narrating tradeoffs.

Design decisions baked in (say these out loud in the interview):
  1. SYNC moderation for images (hold delivery until scored) — a harmful image
     visible even briefly is real harm; budget ~300ms p99.
  2. Dedup cache keyed on image hash — same meme sent thousands of times,
     cache kills most inference cost. (Mention: perceptual hash > SHA256 in
     production, since 1-pixel change defeats exact hashing.)
  3. Three-way threshold: allow / human-review / block. Uncertainty goes to
     humans, not to a coin flip.
  4. FAIL-CLOSED on model timeout/outage: hold the image, return "review".
     Justify: child-safety > latency for this content type.
  5. Log every decision — moderation needs an audit trail.

Run: pip install fastapi uvicorn && uvicorn 02_moderation_service:app --reload
(rename file to moderation_service.py first; module names can't start with a digit)
"""

import hashlib
import logging
import time
from enum import Enum

from fastapi import FastAPI, UploadFile, HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("moderation")

app = FastAPI(title="Chat Image Moderation")

# ---------------------------------------------------------------------------
# Config — in prod these come from a config service / env, and thresholds are
# tunable WITHOUT redeploy (you retune as the model or abuse patterns shift).
# ---------------------------------------------------------------------------
BLOCK_THRESHOLD = 0.90   # >= this confidence of "inappropriate" -> auto-block
REVIEW_THRESHOLD = 0.60  # between review and block -> human review queue
MODEL_TIMEOUT_S = 0.25   # p99 latency budget for the model call


class Verdict(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"   # held + sent to human review queue
    BLOCK = "block"


# ---------------------------------------------------------------------------
# Dedup cache. In prod: Redis with TTL. Interview point: exact hash (SHA256)
# is defeated by changing one pixel -> use a perceptual hash (pHash) so
# near-duplicates also hit the cache.
# ---------------------------------------------------------------------------
_verdict_cache: dict[str, tuple[Verdict, float]] = {}

# In prod: Kafka topic / SQS queue consumed by the review-tool backend.
_review_queue: list[dict] = []


def image_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def model_predict(data: bytes) -> float:
    """
    Stub for the trained classifier. Returns P(inappropriate).
    In prod this is a call to a model server (Triton / TorchServe / ONNX runtime
    behind an internal endpoint), batched on the server side for GPU efficiency.
    """
    time.sleep(0.02)  # simulate inference
    # Deterministic fake score from the hash so the demo is reproducible:
    return int(image_hash(data)[:2], 16) / 255.0


def score_with_timeout(data: bytes) -> float:
    """
    Enforce the latency budget. In real code: asyncio.wait_for around an async
    HTTP call to the model server, plus retries with jitter for transient errors.
    """
    start = time.monotonic()
    score = model_predict(data)
    if time.monotonic() - start > MODEL_TIMEOUT_S:
        raise TimeoutError("model exceeded latency budget")
    return score


def decide(score: float) -> Verdict:
    if score >= BLOCK_THRESHOLD:
        return Verdict.BLOCK
    if score >= REVIEW_THRESHOLD:
        return Verdict.REVIEW
    return Verdict.ALLOW


@app.post("/moderate")
async def moderate(file: UploadFile, player_id: str, channel_id: str):
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="empty image")
    if len(data) > 10 * 1024 * 1024:  # dirty-input guard: 10MB cap
        raise HTTPException(status_code=413, detail="image too large")

    h = image_hash(data)

    # 1) Cache hit -> skip inference entirely
    if h in _verdict_cache:
        verdict, score = _verdict_cache[h]
        log.info("decision=%s score=%.2f cached=1 player=%s", verdict, score, player_id)
        return {"verdict": verdict, "cached": True}

    # 2) Score with timeout; FAIL CLOSED on failure
    try:
        score = score_with_timeout(data)
    except Exception as exc:  # timeout, model down, malformed image, ...
        log.error("model_failure player=%s err=%s -> fail-closed", player_id, exc)
        _review_queue.append({"hash": h, "player": player_id, "reason": "model_failure"})
        return {"verdict": Verdict.REVIEW, "cached": False, "degraded": True}

    # 3) Threshold -> verdict
    verdict = decide(score)
    _verdict_cache[h] = (verdict, score)

    if verdict is Verdict.REVIEW:
        _review_queue.append(
            {"hash": h, "player": player_id, "channel": channel_id, "score": score}
        )

    # 4) Audit log every decision
    log.info(
        "decision=%s score=%.2f cached=0 player=%s channel=%s",
        verdict, score, player_id, channel_id,
    )
    return {"verdict": verdict, "score": round(score, 3), "cached": False}


@app.get("/health")
def health():
    return {"status": "ok", "cache_size": len(_verdict_cache),
            "review_queue_depth": len(_review_queue)}


# ---------------------------------------------------------------------------
# "What would you monitor?"  (say this unprompted — it wins the round)
#   - flag rate over time: sudden DROP = players found an evasion trick;
#     sudden SPIKE = drift or broken preprocessing
#   - p50/p99 latency of /moderate; timeout rate
#   - cache hit rate (capacity planning) and review-queue depth (staffing/SLA)
#   - per-verdict counts by game title / region (segment-level drift)
# Alerts: flag-rate outside rolling 7-day band; review-queue depth > SLA;
#         timeout rate > 1%.
#
# "What changes at 10x scale?"
#   - move inference behind a batching model server on GPU, autoscale on queue depth
#   - Redis cluster for the cache, perceptual-hash sharding
#   - two-stage cascade: tiny cheap model sync (allows ~90% instantly),
#     heavy model only on the uncertain slice
#   - regional deployments to keep p99 down for chat UX
# ---------------------------------------------------------------------------
