# End-to-End ML Lifecycle for the Moderation Model

If they zoom out from the service to the full lifecycle, this is the map.
Anchor with DriftDetector (drift detection + automated retraining, Azure ML/AKS)
and the Amdocs incident-classifier CronJob.

## 1. Data & labels
- Sources: player reports (free but noisy, biased — trolls mass-report innocents),
  human review-queue decisions (high quality, low volume), vendor datasets for v1.
- Class imbalance: inappropriate images are rare (<1%). Use weighted loss / focal
  loss / oversampling; evaluate with PR-AUC, NOT accuracy ("99% accurate" is
  meaningless when 99% of images are fine).
- Label hygiene: double-label a sample to measure reviewer agreement; disagreement
  rate bounds your achievable model quality.

## 2. Validation before trusting it in prod
- Split by TIME, not randomly — meme culture shifts; random split leaks the future.
- Per-segment metrics: game title, region, image type (screenshots vs photos vs
  memes). A model great on average can be terrible on one game's community.
- Shadow mode: run on live traffic, score everything, act on nothing; compare
  against human decisions for 1–2 weeks.

## 3. Rollout
shadow → canary (1–5% of traffic) → full, old model kept warm for instant rollback.
Compare on the canary: flag rate, latency p99, review-queue inflow, appeal rate.
Say: "model rollouts fail in data ways unit tests don't catch — a traffic slice is
the only real test."

## 4. Monitoring in production (the ops-interviewer magnet)
- **Flag rate over time** — the single best signal:
  - sudden DROP → players found an evasion (adversarial drift)
  - sudden SPIKE → data drift or a broken preprocessing step upstream
- Latency p50/p99, timeout rate, cache hit rate, review-queue depth vs staffing SLA.
- Input-distribution drift: image size/format stats, embedding-distance drift
  (mean embedding vs training set), % unknown formats.
- Feedback metrics: appeal rate and appeal-overturn rate = live precision estimate;
  post-hoc report rate on ALLOWED images = live recall estimate.
- Alerts: flag rate outside rolling 7-day band; overturn rate > X%; queue depth > SLA.

## 5. Retraining loop
- Triggers: drift metric threshold, scheduled (e.g., monthly), or flag-rate anomaly.
- Training data refresh: review-queue decisions are your continuous labeling engine —
  the human-in-the-loop band pays for itself with labels.
- Automate: pipeline retrains → evaluates against a frozen benchmark AND the
  latest month's data → auto-deploys to shadow, human approves promotion.
  (This is DriftDetector's architecture — say so.)

## 6. "Model degrading in prod, can't repro locally" playbook
1. Compare prod vs local INPUT distributions first (it's almost always the data).
2. Check preprocessing/feature skew: is prod resizing/encoding images differently
   than the training pipeline did? (training-serving skew is the classic culprit)
3. Replay logged prod inputs through the local model — if it reproduces, it's data;
   if not, it's environment: library versions, model file hash, hardware (GPU fp16
   vs CPU fp32 numeric differences).
4. Segment the degradation: one region/game/client version? → points at an
   upstream change, not the model.
5. Mitigate first (rollback / raise review band), root-cause second.

## 7. Cost levers (if they push on cost)
- Dedup cache (perceptual hash) — biggest lever on meme-heavy traffic
- Two-stage cascade: cheap model handles the easy 90%
- Dynamic batching on GPU; autoscale on queue depth, scale to zero off-peak per region
- Downscale images before inference (224x224 is standard; don't ship 4K to the GPU)
