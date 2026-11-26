# Round 3 — Likely Questions (most → least likely)

## Tier 1: Productionize the round-2 image moderation model (~most likely)

**The prompt will look like:**
> "You have a trained classifier that flags inappropriate images. Millions of EA players
> send images in chat. Build the production system around it. Code the core service."

Expect to actually code:
- An inference API (FastAPI) or queue consumer: image in → allow / block / review out
- Confidence-threshold logic with three outcomes (allow, block, human-review queue)
- Hash-based dedup cache (same meme sent 1000s of times — kills most inference cost)
- Timeouts + fallback behavior when the model service is down
- Structured logging of every decision (audit trail matters for moderation)

Follow-up questions they will layer on:
1. Sync (block delivery until scored) vs async (deliver then retract)? Pick sync for
   images with a ~200–300ms budget: a harmful image visible even for 2 seconds is a
   real harm, esp. with minors on the platform. Two-stage: fast cheap filter sync,
   heavy model async for borderline cases.
2. Fail-open or fail-closed if the model is unreachable? For images: fail-closed
   (queue and hold) is defensible on child-safety grounds; state the latency cost.
3. Where does the human-review queue go? Priority by confidence + reporter count.
4. "Now it's 100k images/sec" → batching on GPU, autoscaling on queue depth,
   dedup cache hit-rate, regional deployment.
5. "Players adversarially evade the model" → perceptual hashing (not just SHA — trivial
   pixel change beats exact hash), retrain loop from review-queue labels, flag-rate
   monitoring (sudden DROP in flag rate = evasion working).

## Tier 2: Text-chat toxicity variant (same problem, cheaper to live-code)

- Real-time toxicity scoring on chat messages
- Extra angles: multilingual players, l33tspeak/spacing evasion, streaming pipeline,
  per-user reputation as a feature, rate limiting abusive senders

## Tier 3: End-to-end ML lifecycle walkthrough (code parts of it)

> "Take this model from data to production and keep it healthy."

- Labels: player reports = free but noisy/biased labels; review-queue decisions =
  high-quality labels; class imbalance (inappropriate images are rare) → weighted
  loss / focal loss / oversampling, and PR-AUC over accuracy
- Validation before trusting in prod: holdout by time (not random), shadow mode
  against live traffic, per-segment metrics (region, game title, image type)
- Rollout: shadow → canary (1–5%) → full, old model warm for instant rollback
- Retraining trigger: drift metric threshold OR scheduled OR flag-rate anomaly
- (Anchor with DriftDetector project)

## Tier 4: DSA — islands, again

They asked Number of Islands in BOTH rounds. Be ready for a third pass with twists:
- Solve with BFS, DFS, and Union-Find fluently
- "Grid doesn't fit in memory" → row-by-row streaming union-find (production twist)
- Cousins: Max Area of Island, Surrounded Regions, Rotting Oranges (BFS time steps),
  Number of Distinct Islands (shape hashing)
See `04_dsa_islands_variants.py`.

## Tier 5: Behavioral/production-scar questions

- "Tell me about a production issue you debugged end to end" — have ONE story with a
  timeline: detection → hypothesis → root cause → fix → prevention (+ numbers)
- "Model degrading in prod, can't reproduce locally — what do you do?" →
  compare input distributions prod vs local, check preprocessing/feature skew,
  replay logged prod inputs, check library/model version mismatch, canary diff
- "When would you NOT use ML?" → when a regex/threshold rule hits 95% of the value
  at 1% of the cost; ML earns its keep only when rules stop scaling. Interviewers
  with ops backgrounds love this answer.
- "How do you use AI tools when coding?" (round 1 evaluated this) → narrate prompts,
  and emphasize you VERIFY generated code: read it, test edge cases, never paste blind.

## Numbers to have in your pocket

- Latency budget for sync chat moderation: ~100–300ms p99
- A ResNet-ish classifier on GPU: ~5–20ms/image batched; CPU: ~50–200ms
- Dedup cache hit rates on meme-heavy chat traffic: often 30–60%+
- Canary size: 1–5% of traffic, watch for hours–days before full rollout
