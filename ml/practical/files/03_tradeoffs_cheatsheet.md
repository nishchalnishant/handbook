# Tradeoff Cheatsheet — rehearse these OUT LOUD, with a recommendation

The brief literally says "make and justify tradeoffs." Never answer "it depends" and
stop — always: name both sides in one sentence each, pick one, give the reason.

## Sync vs async moderation
- Sync: hold message until scored. +No harmful content ever shown. −Adds latency to chat.
- Async: deliver, retract if flagged. +Zero perceived latency. −Harm window of seconds.
- **Pick:** sync for images with ~300ms budget (harm is severe, esp. minors);
  async is acceptable for text with a fast keyword pre-filter running sync.

## Fail-open vs fail-closed (model service is down)
- Fail-open: let content through. Protects UX, risks harm.
- Fail-closed: hold/queue content. Protects players, degrades chat.
- **Pick:** fail-closed for images (child safety trumps latency); fail-open with
  keyword-filter fallback for plain text. State that this is a POLICY decision
  you'd confirm with trust & safety, which itself scores points.

## Precision vs recall (threshold setting)
- High precision: few innocent players blocked, more bad images slip through.
- High recall: catch nearly everything, more false blocks → tickets, churn, appeals.
- **Pick:** bias toward recall, but route the uncertain band to HUMAN REVIEW instead
  of hard-blocking — the three-way threshold converts the tradeoff into a staffing
  cost rather than a player-harm cost.

## Batch vs streaming / CronJob vs always-on service
- Your Amdocs story: incident classification as an AKS CronJob — cheap, simple,
  freshness tolerance was minutes not milliseconds.
- Chat moderation: must be real-time → always-on service.
- **Line to say:** "I choose the cheapest architecture the freshness requirement
  allows — I've run ML as a CronJob in prod when minutes of staleness was fine."

## Small fast model vs big accurate model
- **Pick:** cascade. Tiny model answers the easy ~90% within budget; heavy model
  only sees the uncertain slice. Best of both; the cost is pipeline complexity
  and TWO models to monitor/version.

## Exact hash vs perceptual hash for the dedup cache
- SHA256: trivial to compute, defeated by a 1-pixel change.
- pHash: near-duplicates hit the cache, robust to re-encoding/crops; small
  false-collision risk.
- **Pick:** perceptual hash, because the adversary is players, and they adapt.

## Rule-based vs ML
- **Line to say:** "If a regex or threshold gets 95% of the value at 1% of the
  cost, ship the regex; the model earns its place only when rules stop scaling
  or the adversary adapts faster than we can write rules."

## Canary vs blue-green for model rollout
- Blue-green: instant full cutover, instant rollback, but 100% blast radius.
- Canary: 1–5% traffic, compare flag-rate/latency vs control, slow but safe.
- **Pick:** shadow mode first (score, don't act) → canary → full. Keep the old
  model warm for instant rollback. Model rollouts fail in DATA ways that unit
  tests don't catch, so exposure to a traffic slice is the only real test.

## CPU vs GPU inference
- CPU: cheap at low QPS, no batching complexity. GPU: 10–20x throughput but only
  when batched; idle GPU is burned money.
- **Pick:** GPU with server-side dynamic batching once past ~50–100 QPS of image
  inference; below that, CPU autoscaling is simpler and cheaper.

## Build vs buy
- Cloud moderation APIs (e.g., vendor content-safety APIs) vs in-house model.
- **Pick:** be honest — a vendor API is a great v1 (fast, handles CSAM legal
  requirements). In-house wins when: cost at EA scale, game-specific content
  (in-game screenshots get false-flagged by generic APIs), latency, data control.
  Naming BOTH shows judgment; the interviewer knows real teams start with buy.
