# EA SDE 2 (AI Engineer) — Round 3 Prep

**Brief from HR:** "Solve a real production problem end to end (with coding). Make and justify tradeoffs."

**Interviewer:** Senior Software Engineer at EA (backend/systems background — TCS network
management systems, ADP cloud platforms, Ericsson). Hands-on production/ops engineer,
not a research ML person. Cares about: reliability, failure modes, performance under load,
monitoring, pragmatic engineering.

## Pattern from earlier rounds

| Round | Content |
|-------|---------|
| 1 | Easy ML questions + DSA (Number of Islands) |
| 2 | RAG project discussion + Number of Islands again + **verbal** design of an image classifier that flags inappropriate images in EA player chat |
| 3 | "Real production problem end to end **with coding**" |

**Prediction:** Round 3 is very likely the *productionized, coded* version of the round 2
content-moderation problem. Round 2 tested "can you design the model", round 3 tests
"can you ship and operate it."

## Files in this folder

1. `01_likely_questions.md` — structured question bank, most→least likely
2. `02_moderation_service.py` — reference implementation to practice writing from scratch
3. `03_tradeoffs_cheatsheet.md` — the tradeoff one-liners to rehearse out loud
4. `04_dsa_islands_variants.py` — islands + all likely follow-up variants
5. `05_ml_lifecycle_and_monitoring.md` — lifecycle, drift, rollout, monitoring answers

## Session structure that lands well with this interviewer

1. Clarify requirements + scale (QPS, latency budget, sync vs async chat)
2. State assumptions explicitly
3. Propose 2 approaches with tradeoffs → pick one and justify
4. Code it (clean, with error handling, timeouts, logging — unprompted)
5. Failure modes + monitoring + "what changes at 10x scale"
6. Close with: "here's what I'd monitor and what alert I'd set"

## Personal stories to anchor answers

- **Amdocs incident classifier as AKS CronJob** → why batch/CronJob over always-on
  service (cost, simplicity, freshness tolerance). Direct analogue for auto-classifying
  production issues with ML.
- **DriftDetector** → drift detection + automated retraining on Azure ML/AKS. Use for
  any "how do you keep the model good over time" question.
- **MovieDB review controller** → content moderation + rate limiting. You have literally
  built a small moderation pipeline before.
