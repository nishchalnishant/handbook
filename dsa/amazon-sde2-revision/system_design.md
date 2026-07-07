# System Design — Amazon SDE-2 Reference

> Amazon SDE-2 system design round: ~45 min, one medium-scale distributed system.
> Scope: URL shortener, Twitter Feed, Rate Limiter, Distributed Cache, Notification Service.
> You will NOT be asked about ML systems, GPU clusters, or compiler design.

---

## The 6-Step Framework (use this order every time)

```
1. Clarify requirements      (~3 min)
2. Capacity estimation       (~5 min)
3. API design                (~3 min)
4. Data model                (~5 min)
5. Core components           (~15 min)
6. Scale & bottlenecks       (~10 min)
```

---

## Step 1 — Clarify Requirements

Ask these before touching the whiteboard:

- **Scale:** DAU, QPS (reads vs writes), data size
- **Latency:** Is this read-heavy? Write-heavy? What's the SLA?
- **Consistency:** Strong or eventual? (Amazon defaults to eventual for scale)
- **Availability:** 99.9% or 99.99%? Single region or multi-region?
- **Features to exclude:** "Should I handle analytics? Auth? Admin panel?" — narrow scope

---

## Step 2 — Capacity Estimation

**Quick math rules:**
- 1 million DAU × 10 actions/day = ~10M events/day = ~115 QPS
- 1 KB per record × 1M records = 1 GB
- SSD read: ~0.1ms, RAM read: ~0.0001ms, network round-trip: ~1-5ms
- 1 day = 86,400 s ≈ 10^5 s (useful for back-of-envelope)

**Template:**
```
Read QPS  = DAU × avg reads/day / 86,400
Write QPS = DAU × avg writes/day / 86,400
Storage   = writes/day × record_size × retention_days
Bandwidth = QPS × avg_response_size
```

---

## Step 3 — API Design

Define 2-3 core endpoints. Use REST.

```
POST /api/v1/<resource>          → create
GET  /api/v1/<resource>/{id}     → read
GET  /api/v1/<resource>?cursor=X → paginated list
DELETE /api/v1/<resource>/{id}   → delete
```

State pagination strategy: cursor-based (infinite scroll) vs offset (known page count).

---

## Step 4 — Data Model

Pick storage type first, then schema:

| Need | Use |
|------|-----|
| Structured data, ACID, relations | PostgreSQL / MySQL |
| High-throughput KV / wide-column | Cassandra / DynamoDB |
| Search / full-text | Elasticsearch |
| Cache / session | Redis |
| Blob / media | S3 |
| Graph relationships | Neo4j (rare at Amazon) |

**SQL vs NoSQL decision:**
- SQL: when you need joins, strong consistency, complex queries
- NoSQL: when you need horizontal write scale, schema flexibility, or simple KV access patterns

---

## Step 5 — Core Components

Draw these boxes and explain data flow between them:

```
Client → Load Balancer → API Servers → Cache (Redis)
                                     ↘ DB (Primary/Replica)
                                     ↘ Message Queue → Workers
                                     ↘ Object Store (S3)
```

**Components to know cold:**

### Load Balancer
- L4 (TCP) vs L7 (HTTP/path-based routing)
- Sticky sessions when needed; round-robin default

### Cache (Redis)
- Cache-aside pattern (most common): app reads cache first, falls back to DB, writes to cache on miss
- Write-through: write to cache + DB together (consistency > performance)
- Cache eviction: LRU default; TTL for time-sensitive data
- Cache stampede: use locks or probabilistic early expiry

### Database
- Primary-replica replication: primary handles writes, replicas handle reads
- Sharding: partition by user_id (hash) or by geography (range)
- Index on high-cardinality columns queried frequently

### Message Queue (SQS / Kafka)
- Use when: write spikes, async processing, decoupling services
- At-least-once delivery → make consumers idempotent
- Dead letter queue for failed messages

### CDN
- Static assets (images, JS, CSS) → serve from CDN edge
- Dynamic content → API gateway, not CDN

---

## Step 6 — Scale & Bottlenecks

Walk through each component and ask "what breaks at 10x load?":

| Bottleneck | Fix |
|------------|-----|
| Single DB primary | Read replicas, then shard |
| Cache miss storm | Pre-warm cache, consistent hashing |
| Slow writes | Async via queue, batch writes |
| Single region failure | Multi-region active-passive or active-active |
| Hot partition (shard) | Add random suffix to key, repartition |
| URL shortener collision | Pre-generate keys offline |

**CAP Theorem (mention it once):**
- CP: bank transfers, inventory (can't show wrong count)
- AP: social feeds, likes, view counts (eventual consistency OK)

---

## Common Systems — Key Points

### URL Shortener
- Generate short key: base62(counter) or MD5 first 7 chars
- KV store: `short_key → original_url`
- Redirect: 301 (cached by browser) vs 302 (every request hits server for analytics)
- Scale: pre-generate key range per server to avoid counter contention

### Twitter Feed / News Feed
- Two approaches: **fan-out on write** (push to followers' timelines on post) vs **fan-out on read** (pull + merge on read)
- Fan-out on write: fast reads, slow writes for celebrities (10M followers = 10M writes)
- Hybrid: fan-out on write for regular users, fan-out on read for celebrities
- Timeline stored in Redis sorted set: `ZADD user:{id}:feed timestamp tweet_id`

### Rate Limiter
- Token bucket (bursty allowed) vs sliding window log (precise) vs fixed window counter (simple, edge case at boundary)
- Redis + Lua script for atomic `INCR + EXPIRE`
- Return `429 Too Many Requests` with `Retry-After` header
- Distribute: per-server counter (fast, less accurate) vs centralized Redis (accurate, one more hop)

### Distributed Cache (Memcached / Redis cluster)
- Consistent hashing: add/remove nodes with minimal key remapping
- Cache invalidation strategies: TTL, event-driven invalidation, write-through
- Replication: Redis Sentinel (HA) or Redis Cluster (HA + sharding)

### Notification Service (Push / Email / SMS)
- Fan-out via queue: `notification_service → SQS → worker_per_channel`
- Deduplication: idempotency key in DB, `INSERT ... ON CONFLICT DO NOTHING`
- Priority queue: critical alerts (payment failure) vs marketing (separate queues, separate consumers)
- Rate limit per user to avoid spam

### Design Twitter (LRU/LFU Cache — coding round version)
- LRU: doubly-linked list + hashmap, O(1) get/put
- LFU: hashmap of freq → DLL of nodes, O(1) get/put
- Both are P2 problems — know the implementation cold

---

## Amazon Leadership Principles in System Design

Amazon interviewers score design for LP signals too:

| LP | What to demonstrate |
|----|-------------------|
| **Customer Obsession** | Clarify user needs first; optimize for their latency/reliability |
| **Dive Deep** | Know the data model, not just the boxes |
| **Invent and Simplify** | Pick the simplest design that meets requirements; justify trade-offs |
| **Ownership** | Proactively identify failure modes; don't wait to be asked |
| **Frugality** | Justify each component — don't add a Kafka if a simple DB queue works |

---

## Complexity Quick-Reference

| Operation | Latency |
|-----------|---------|
| Redis GET/SET | ~0.1ms |
| SQL query (indexed) | ~1ms |
| SQL query (full scan) | ~100ms |
| S3 read | ~10-50ms |
| Network (same DC) | ~0.5ms |
| Network (cross-region) | ~50-150ms |
| SSD sequential read | ~0.1ms |
| HDD random read | ~10ms |

---

## Week-Before Checklist (System Design)

- [ ] Can you draw a URL shortener end-to-end in < 5 min?
- [ ] Can you explain fan-out on write vs fan-out on read for a news feed?
- [ ] Can you implement rate limiting with Redis in pseudocode?
- [ ] Do you know when to shard vs when to add replicas?
- [ ] Can you explain CAP theorem with a concrete Amazon example?
- [ ] Do you have back-of-envelope math ready for QPS/storage estimates?
- [ ] Can you implement LRU Cache from scratch in < 10 min (LC 146)?
- [ ] Can you implement LFU Cache from scratch in < 15 min (LC 460)?
