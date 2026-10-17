# HLD / System Design — 60 Minute Playbook

## Timeline

| Time | Phase | What you produce | Say out loud |
|---|---|---|---|
| **0–05** | Functional reqs | 3–5 user-facing features | "Let me scope to the core flows." |
| **05–10** | Non-functional + scale | QPS, storage, latency SLO | "This is what drives the architecture." |
| **10–15** | API contract | 4–6 endpoints with params | "Here's what clients call." |
| **15–20** | Data model | Tables/collections + DB choice | "Access pattern is X, so I'd pick Y." |
| **20–28** | High-level diagram | Boxes + arrows, request path | "Let me walk one write and one read." |
| **28–45** | **Deep dive** | The 1–2 hard components | "Which piece do you want me to go deep on?" |
| **45–53** | Scale & failure | Bottlenecks, replication, degradation | "At 10x, this breaks first." |
| **53–60** | Trade-offs & wrap | What you'd do differently | — |

**Hard rule:** don't draw a single box before minute 15. Requirements first, architecture second.

---

## Stage 1 — Functional (0–05)
Pick **3 features max** and get agreement. For a URL shortener: create short link, redirect, analytics. Everything else is out.
Ask: *"Should I treat this as read-heavy or write-heavy?"* — the single most useful question you can ask.

## Stage 2 — Non-functional + estimation (05–10)
Cover these five, always:
**Scale · Latency · Availability · Consistency · Durability**

Estimate in round numbers, out loud:
```
100M DAU × 10 reads/day  = 1B reads/day ≈ 12K QPS avg, ~40K peak
Writes 1/100 of reads    ≈ 120 write QPS
Row 1KB × 100M writes/day = 100 GB/day ≈ 36 TB/year
```
Then state the consequence: *"40K QPS on reads means a cache tier and read replicas, not a single primary."*
Round aggressively — the number matters less than the conclusion you draw from it.

## Stage 3 — API (10–15)
```
POST /v1/orders          {items, idempotency_key} -> 201 {order_id}
GET  /v1/orders/{id}                              -> 200 {order}
GET  /v1/orders?cursor=&limit=                    -> 200 {items, next_cursor}
```
Always: **cursor pagination** (not offset), **idempotency key** on writes, **versioned path**.

## Stage 4 — Data model (15–20)
Show the schema, then justify the store by **access pattern**:

| Pattern | Store |
|---|---|
| Transactions, joins, strong consistency | Postgres / MySQL |
| High write volume, known key, no joins | DynamoDB / Cassandra |
| Full-text / faceted search | Elasticsearch |
| Hot key-value, sessions, counters | Redis |
| Append-only event stream | Kafka |
| Blobs, media | S3 + CDN |

State the **partition key** and why it avoids hotspots. Interviewers probe this.

## Stage 5 — High-level diagram (20–28)
Standard skeleton, then delete what you don't need:
```
Client → CDN → LB → API Gateway → Service(s) → Cache → DB
                                      ↓
                              Queue → Workers → Blob store
```
Then **trace one write and one read end to end**. This is the moment that separates strong from average candidates — most people draw the diagram and stop.

## Stage 6 — Deep dive (28–45)
Ask which component. If they defer, pick the one with the hardest constraint. Usual suspects:
- **ID generation** — Snowflake vs UUIDv7 vs DB sequence
- **Cache strategy** — cache-aside, TTL, invalidation, stampede protection
- **Fanout** — write-fanout vs read-fanout, and the celebrity problem
- **Consistency** — where you accept eventual, where you must not
- **Idempotency & exactly-once** — dedupe key + outbox pattern
- **Rate limiting** — token bucket at the gateway
- **Search / ranking** — index pipeline, freshness lag

Go 3 levels deep on one thing rather than 1 level on six.

## Stage 7 — Scale & failure (45–53)
Walk the path and name what breaks first:
- **DB** → read replicas → shard (state the shard key) → CQRS
- **App tier** → stateless + autoscale
- **Hot keys** → local cache + consistent hashing
- **Traffic spikes** → queue and shed load
- **Failure** → what happens when the cache dies? The region dies? Answer with *graceful degradation*, not "it's fine."

Then: monitoring (p99 latency, error rate, queue depth), and the one alert you'd page on.

## Stage 8 — Trade-offs (53–60)
Close with two or three explicit ones:
*"I chose eventual consistency on the feed for write throughput; if the product needed read-your-writes I'd pin the author to the primary for 30 seconds."*

---

## Scoring signals

| Green | Red |
|---|---|
| Estimated, then used the number | Estimated, then ignored it |
| Justified every DB choice | "I'd use Kafka" with no reason |
| Traced a request end to end | Drew boxes, never connected them |
| Named the bottleneck unprompted | Waited for the interviewer to find it |
| Stated trade-offs both ways | Presented one design as obviously correct |
| Managed the clock | Spent 25 minutes on requirements |

## Recovery lines
- Unfamiliar domain: *"I haven't built this exact system — let me reason from the access patterns."*
- Challenged: *"That's fair. The alternative is X, which trades A for B. Given the requirement, I'd switch."*
- Behind: *"I'll keep the remaining components at one line each so we have time for the deep dive."*
