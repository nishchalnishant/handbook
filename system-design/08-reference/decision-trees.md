# Decision Trees — "Which One Do I Pick?"

> [!NOTE]
> **📋 5-Minute Summary**
>
> **What this covers:** Technology-selection decision trees for the moments in an interview where you must *choose* — SQL vs NoSQL, which consistency model, which cache strategy, push vs pull, sync vs async, and more. Each tree ends at a concrete choice with the one-line justification you'd say out loud.
>
> **Key concepts:**
> - These are *selection* trees (pick a technology/approach), not concept-recall maps — for topic recall see [../FLOWCHARTS.md](../FLOWCHARTS.md).
> - Every leaf names a default and the trigger that would change it — interviewers reward "I'd pick X, but switch to Y if Z."
> - Read a leaf as a starting position, not dogma; state your assumption, then commit.
>
> **Key takeaway:** In an interview, don't enumerate options — traverse the tree out loud to a decision, then justify. Indecision reads as junior; a defended default reads as senior.

---

## How to use these

Interviewers don't want a survey of every database. They want you to **pick one and defend it**. Each tree below encodes the discriminating questions in the order that actually matters, so you converge fast and can say *why*. The pattern to voice: **"Default X because [property]; I'd switch to Y if [trigger]."**

---

## 1. SQL vs NoSQL

```mermaid
flowchart TD
    A[Storing what?] --> B{Strong relational<br/>integrity + multi-row<br/>transactions needed?}
    B -->|Yes| C{Scale beyond<br/>one primary's<br/>write capacity?}
    C -->|No| SQL[Relational: PostgreSQL/MySQL<br/>ACID, joins, mature]
    C -->|Yes| NewSQL[NewSQL: CockroachDB/Spanner/Vitess<br/>distributed ACID, horizontal writes]
    B -->|No| D{Access pattern?}
    D -->|Key lookups,<br/>massive write throughput| KV[Key-Value / Wide-column:<br/>DynamoDB, Cassandra]
    D -->|Flexible/nested docs| DOC[Document: MongoDB]
    D -->|Full-text / relevance| SEARCH[Search: Elasticsearch]
    D -->|Relationships-as-first-class| GRAPH[Graph: Neo4j]
    D -->|Time-series metrics| TS[Time-series: InfluxDB, TimescaleDB]
```

**Say it:** "Start relational — ACID, joins, and it scales further than people think with read replicas + partitioning. Only leave SQL when a *specific* pressure forces it: write throughput past one primary (→ Cassandra/DynamoDB), schema flexibility (→ document), or a query shape SQL is bad at (full-text → ES, traversals → graph)."

---

## 2. Consistency model

```mermaid
flowchart TD
    A[What breaks if a read<br/>is stale?] --> B{Money / inventory /<br/>correctness-critical?}
    B -->|Yes| C{Single region<br/>or global?}
    C -->|Single| SC[Strong consistency<br/>single-leader, synchronous]
    C -->|Global| CP[Consensus: Raft/Paxos<br/>Spanner-style; accept latency]
    B -->|No| D{Must reads reflect<br/>THIS client's own writes?}
    D -->|Yes| RYW[Read-your-writes /<br/>session consistency<br/>sticky routing or read-from-leader]
    D -->|No| E{Tolerable staleness?}
    E -->|Seconds OK| EC[Eventual consistency<br/>async replicas, Dynamo-style]
    E -->|Causal order matters| CC[Causal consistency<br/>vector clocks / version vectors]
```

**Say it:** "Consistency is per-operation, not per-system. Checkout and balance reads need strong/linearizable; a like-count or feed can be eventually consistent. The common middle ground is session consistency — a user must see their own writes even if others see them a beat later."

---

## 3. Caching strategy (read path)

```mermaid
flowchart TD
    A[Read-heavy data?] --> B{Can tolerate<br/>brief staleness?}
    B -->|No, must be fresh| WT[Write-through +<br/>read cache<br/>cache updated on every write]
    B -->|Yes| C{Write volume?}
    C -->|Write-heavy,<br/>reads may lag| WB[Write-back / write-behind<br/>async flush; risk loss on crash]
    C -->|Read-heavy| CA[Cache-aside lazy<br/>app loads on miss, sets TTL]
    CA --> D{Thundering herd<br/>on hot key?}
    D -->|Yes| LOCK[Add request coalescing +<br/>stale-while-revalidate]
    D -->|No| DONE[Cache-aside + TTL is enough]
```

**Say it:** "Default cache-aside with a TTL — simplest, app controls it, cache failure just means a slower read not a wrong one. Add write-through only when staleness is unacceptable, and guard hot keys with request coalescing so a cache miss doesn't stampede the DB."

---

## 4. Push vs Pull (feeds, notifications, fan-out)

```mermaid
flowchart TD
    A[Delivering updates<br/>to many consumers?] --> B{Fan-out size<br/>per producer?}
    B -->|Small/uniform followers| PUSH[Fan-out on write push<br/>precompute each timeline<br/>fast reads, cheap fan-out]
    B -->|Celebrity / huge fan-out| PULL[Fan-out on read pull<br/>merge at query time<br/>avoids write amplification]
    B -->|Mixed| HYBRID[Hybrid<br/>push for normal users,<br/>pull-merge for celebrities]
    A --> C{Latency need?}
    C -->|Real-time| SSE[Server push:<br/>WebSocket / SSE]
    C -->|Near-real-time| POLL[Long-polling / periodic pull]
```

**Say it:** "Push (fan-out on write) makes reads O(1) but explodes for celebrities — one write becomes 100M inserts. So the real answer is hybrid: push for the median user, pull-and-merge for high-fan-out accounts, decided by a follower-count threshold."

---

## 5. Sync vs Async (request handling)

```mermaid
flowchart TD
    A[Does the caller need<br/>the result to proceed?] --> B{Yes?}
    B -->|Yes, immediately| SYNC[Synchronous request/response<br/>keep it fast, set timeouts]
    B -->|No, fire-and-forget| C{Ordering / durability<br/>required?}
    C -->|Yes| MQ[Async via durable queue<br/>Kafka / SQS; consumer processes]
    C -->|Best-effort| EVENT[Event bus / pub-sub<br/>decoupled subscribers]
    A --> D{Operation slow<br/>or spiky?}
    D -->|Yes| ASYNC2[Accept-202 + async worker<br/>return job id, poll/callback]
```

**Say it:** "If the user is blocked on the answer, sync. If it's slow (email, video encode, ML scoring) or spiky, return 202 Accepted with a job id and process on a durable queue — this decouples the burst from the workers and lets you retry."

---

## 6. Load balancing layer

```mermaid
flowchart TD
    A[Balancing what?] --> B{Need to route on<br/>URL/host/headers?}
    B -->|Yes| L7[Layer 7 app LB<br/>content-based routing, TLS term,<br/>sticky sessions]
    B -->|No, raw speed| L4[Layer 4 network LB<br/>connection-level, lower latency,<br/>very high throughput]
    A --> C{Stateful connections<br/>e.g. WebSocket?}
    C -->|Yes| STICKY[Consistent hashing /<br/>session affinity]
    A --> D{Global users?}
    D -->|Yes| GEO[GeoDNS / Anycast +<br/>regional LBs]
```

**Say it:** "L7 when I need to route by path/host or terminate TLS; L4 when I just need to spray connections at max throughput with minimal latency. Globally, GeoDNS or Anycast picks the nearest region, then a regional LB fans out."

---

## 7. Message delivery guarantee

```mermaid
flowchart TD
    A[What's the cost<br/>of a lost / duplicate<br/>message?] --> B{Loss acceptable?}
    B -->|Yes, e.g. metrics| ALO0[At-most-once<br/>fire and forget, no retries]
    B -->|No| C{Duplicates acceptable?}
    C -->|Yes if handled| ALO[At-least-once +<br/>idempotent consumer<br/>THE common default]
    C -->|No, must be exactly-once| EO[Effectively-once:<br/>idempotency keys OR<br/>transactional outbox +<br/>dedup on consumer]
```

**Say it:** "There's no free exactly-once over a network. The practical answer is at-least-once delivery plus an idempotent consumer — dedup on a message/idempotency key — which *behaves* exactly-once. True transactional exactly-once (Kafka transactions) exists but costs throughput and scope."

---

## 8. Which partitioning / sharding key

```mermaid
flowchart TD
    A[Picking a shard key] --> B{Queries mostly<br/>by one entity id?}
    B -->|Yes| HASH[Hash-partition on that id<br/>even spread, no hotspots]
    B -->|No, range scans<br/>by time/order| RANGE[Range-partition<br/>good for scans, watch<br/>for hot latest partition]
    A --> C{Risk of a hot key<br/>celebrity/popular item?}
    C -->|Yes| SALT[Add salt/composite key<br/>or split the hot entity]
    A --> D{Need related rows<br/>co-located for joins?}
    D -->|Yes| ENTITY[Entity-group / directory<br/>partition by tenant/user]
```

**Say it:** "Hash-partition on the id you filter by most — it spreads load evenly. Range-partitioning helps time-ordered scans but concentrates writes on the newest partition. The failure mode to preempt is a hot key: a celebrity or viral item, fixed by salting or splitting that entity."

---

## 9. Rate limiting algorithm

```mermaid
flowchart TD
    A[Rate limiting need] --> B{Need smooth,<br/>burst-tolerant limiting?}
    B -->|Yes, allow bursts| TB[Token bucket<br/>refill rate + burst capacity<br/>the usual default]
    B -->|No, strict constant rate| LB[Leaky bucket<br/>fixed drain rate, queues excess]
    A --> C{Simple per-window count?}
    C -->|Yes, accept edge bursts| FW[Fixed window counter<br/>simplest, boundary spike risk]
    C -->|Need accuracy at edges| SW[Sliding window log/counter<br/>accurate, more memory]
```

**Say it:** "Token bucket is the default — it enforces an average rate while permitting short bursts, which matches real traffic. Fixed-window is simplest but lets 2× the limit through at the window boundary; sliding window fixes that at the cost of more state."

---

## 10. Storage for a blob / file

```mermaid
flowchart TD
    A[Storing large binary?] --> B{Serve to end users<br/>at scale?}
    B -->|Yes| OBJ[Object store + CDN<br/>S3/GCS + CloudFront<br/>never blobs in the DB]
    B -->|No, internal| C{Access pattern?}
    C -->|Random read/write| BLOCK[Block storage / EBS<br/>attach to a compute node]
    C -->|Shared POSIX FS| FILE[File storage / EFS/NFS]
    A --> D{Metadata + search<br/>over files?}
    D -->|Yes| META[Blob in object store,<br/>metadata + pointer in DB]
```

**Say it:** "Blobs go in object storage fronted by a CDN; the database holds only metadata and the object key. Putting large binaries in the DB bloats it, wrecks backups, and blows the cache — the classic anti-pattern."

---

## 11. Message broker / queue

```mermaid
flowchart TD
    A[Need async messaging] --> B{Need replay of<br/>past messages?}
    B -->|Yes, log semantics| K[Kafka / Pulsar<br/>retention by time or size<br/>consumers own their offset]
    B -->|No, work queue| C{Need per-message<br/>ack, retry, DLQ,<br/>complex routing?}
    C -->|Yes| R[RabbitMQ<br/>flexible routing, priorities<br/>per-message TTL]
    C -->|No, just decouple| D{Want to run<br/>zero infrastructure?}
    D -->|Yes| SQS[SQS / managed queue<br/>near-infinite scale<br/>at-least-once, no ordering*]
    D -->|No| R
    K --> E{Need per-message ack<br/>AND replay together?}
    E -->|Yes| P[Pulsar<br/>both models in one system<br/>higher operational cost]
```

\* SQS FIFO queues give ordering and exactly-once processing, capped at 300 TPS per message group.

| | Kafka | RabbitMQ | SQS | Pulsar |
|---|---|---|---|---|
| Model | Distributed log | Broker/queue | Managed queue | Log + queue |
| Replay | Yes | No | No | Yes |
| Ordering | Per partition | Per queue | FIFO queues only | Per partition |
| Throughput | Very high | Moderate | High | Very high |
| Ops burden | High | Moderate | None | Highest |
| Best for | Event streaming, CDC | Task routing | Simple decoupling | Both, at cost |

**Say it:** "I'd use Kafka when consumers need to replay — event sourcing, CDC, or a new consumer that must read history. I'd use RabbitMQ or SQS for work queues where a message is consumed once and discarded. The deciding question isn't throughput, it's whether the message is an *event* others may re-read or a *task* someone performs once."

---

## 12. Search store

```mermaid
flowchart TD
    A[Need search] --> B{Semantic /<br/>similarity search?}
    B -->|Yes| VEC[Vector DB<br/>pgvector, Pinecone, Milvus<br/>embeddings + ANN index]
    B -->|No, keyword| C{Already in Postgres<br/>and under ~1M docs?}
    C -->|Yes| PG[Postgres full-text search<br/>tsvector + GIN index<br/>no new system to run]
    C -->|No| D{Need relevance tuning,<br/>facets, aggregations,<br/>fuzzy matching?}
    D -->|Yes| ES[Elasticsearch / OpenSearch<br/>inverted index, BM25<br/>separate cluster + sync]
    D -->|No| PG
    VEC --> E{Also need keyword<br/>precision?}
    E -->|Yes| HYB[Hybrid: BM25 + vector,<br/>fuse with RRF]
```

**Say it:** "I'd start with Postgres full-text search — it's free, transactional, and there's no sync lag. I'd move to Elasticsearch when I need relevance tuning, faceting, or fuzzy matching, and I'd accept the cost that comes with it: a second system, a CDC pipeline, and eventual consistency between the DB and the index. For semantic search I'd add vectors, and in practice hybrid retrieval beats either alone."

---

## 13. Distributed transaction strategy

```mermaid
flowchart TD
    A[Write spans multiple<br/>services or databases] --> B{Can you avoid it?<br/>Co-locate the data}
    B -->|Yes| ONE[Single ACID transaction<br/>always prefer this]
    B -->|No| C{Do you control all<br/>participants AND need<br/>strict atomicity?}
    C -->|Yes, short-lived| TPC[2PC / XA<br/>blocks on coordinator failure<br/>rarely worth it]
    C -->|No| D{Is it: local write +<br/>publish an event?}
    D -->|Yes| OBX[Transactional outbox<br/>write row + event in one txn,<br/>relay publishes after commit]
    D -->|No, multi-step<br/>business flow| SAGA[Saga<br/>local txn per step +<br/>compensating action]
    SAGA --> E{Many steps or<br/>complex branching?}
    E -->|Yes| ORCH[Orchestrated saga<br/>central state machine<br/>easy to observe]
    E -->|No| CHOR[Choreographed saga<br/>services react to events<br/>fewer deps, harder to trace]
```

**Say it:** "First I'd try to make the transaction unnecessary by putting the data that must change together in one place. When I can't, I use the outbox pattern for the common case — write the row and the event in one local transaction so they can't diverge — and a saga for genuine multi-step flows, accepting that intermediate states are visible and every step needs a compensating action. I'd avoid 2PC: it holds locks across the network and blocks if the coordinator dies."

---

## 14. Stream vs batch processing

```mermaid
flowchart TD
    A[Processing data] --> B{Does a result that's<br/>hours old still<br/>create value?}
    B -->|Yes| BAT[Batch<br/>Spark, dbt, scheduled jobs<br/>cheaper, simpler, replayable]
    B -->|No, need seconds| C{Is it per-event, or<br/>aggregates over windows?}
    C -->|Per-event| SS[Stream: stateless<br/>Kafka consumer, Flink map<br/>trivial to scale]
    C -->|Windowed aggregates| ST[Stream: stateful<br/>Flink/Kafka Streams<br/>watermarks + late data policy]
    ST --> D{Must historical<br/>results match live?}
    D -->|Yes| KAP[Kappa: one stream engine,<br/>replay the log to backfill]
    D -->|Separate paths OK| LAM[Lambda: batch for truth,<br/>stream for speed<br/>two codebases to maintain]
```

**Say it:** "The question I'd ask is what latency the business actually needs — batch is cheaper, easier to test, and trivially replayable, so I'd only pay for streaming when a result that's an hour old is worthless. If I do go streaming, I'd prefer a Kappa-style single pipeline and replay the log for backfills, because Lambda's two codebases inevitably drift and produce two different answers to the same question."

---

## 15. Monolith vs service split (where to draw the boundary)

```mermaid
flowchart TD
    A[Considering a split] --> B{Is the pain<br/>technical or<br/>organizational?}
    B -->|Neither yet| MOD[Modular monolith<br/>enforce module boundaries<br/>one deploy, one database]
    B -->|Independent scaling<br/>of one component| SCALE[Extract that component only<br/>e.g. image processing]
    B -->|Teams blocking<br/>each other on deploys| C{Can the candidate own<br/>its data exclusively?}
    C -->|No, needs joins<br/>with everything| STOP[Do not split<br/>you'd create a distributed<br/>monolith: worst of both]
    C -->|Yes| D{Is the interface<br/>stable and narrow?}
    D -->|Yes| SVC[Extract as a service<br/>own database, versioned API]
    D -->|No, still churning| MOD
```

**Say it:** "I'd draw service boundaries around data ownership and team ownership, not around nouns. The test is whether the candidate service can own its data outright — if extracting it means chatty synchronous calls back for every join, I've built a distributed monolith and taken on network failure modes without gaining independence. I'd start as a modular monolith with enforced internal boundaries, because that makes the eventual extraction cheap while keeping deploys simple."

---

## 16. Multi-region topology

```mermaid
flowchart TD
    A[Going multi-region] --> B{Why? Name the driver}
    B -->|Read latency<br/>for global users| RR[Read replicas per region<br/>writes still go to primary<br/>simplest, replica lag on reads]
    B -->|Disaster recovery| C{What RTO/RPO<br/>does the business need?}
    C -->|Hours / some loss OK| BACKUP[Backup + restore<br/>cheapest]
    C -->|Minutes| AP[Active-passive<br/>warm standby + failover<br/>test the failover regularly]
    B -->|Write availability<br/>+ data residency| D{Can you partition users<br/>so each row has<br/>one home region?}
    D -->|Yes| PIN[Active-active, partitioned<br/>each user pinned to a region<br/>no write conflicts]
    D -->|No, same row written<br/>in two regions| CONF[Active-active, conflict resolution<br/>CRDTs or last-write-wins<br/>hardest option]
```

**Say it:** "I'd push hard on *why* before *how* — most 'multi-region' requirements are really read-latency requirements, and read replicas solve those at a fraction of the complexity. True active-active is only tractable when you can partition users so each record has a single home region that owns its writes. If the same row can be written in two regions at once, you've signed up for conflict resolution, and that's a business decision about which write wins, not a technical one."

---

## 17. Time-series storage

```mermaid
flowchart TD
    A[Time-stamped data] --> B{Is it metrics for<br/>dashboards/alerts?}
    B -->|Yes| C{Scale?}
    C -->|Single cluster| PROM[Prometheus<br/>pull model, PromQL<br/>local disk, short retention]
    C -->|Long retention,<br/>many clusters| LTS[Thanos / Mimir / VictoriaMetrics<br/>object storage backend]
    B -->|No, business events<br/>to query later| D{Need SQL joins with<br/>relational data?}
    D -->|Yes| TS[TimescaleDB<br/>Postgres + hypertables<br/>keeps SQL and transactions]
    D -->|No, analytics<br/>over huge volume| OLAP[ClickHouse / Druid<br/>columnar, blazing aggregates<br/>append-oriented]
    A --> E{Retention policy<br/>defined?}
    E -->|Always| DS[Downsample: raw 7d,<br/>1m rollup 90d, 1h rollup 2y]
```

**Say it:** "Time-series data is append-heavy, queried by range, and almost never updated — which is why a columnar store with time partitioning beats a row store here. The design decision people forget is retention: I'd downsample aggressively, keeping raw data for days and rollups for years, because storing raw high-cardinality metrics forever is what actually blows the budget."

---

## 18. ID generation

```mermaid
flowchart TD
    A[Need unique IDs] --> B{Single database?}
    B -->|Yes| SEQ[DB sequence / AUTO_INCREMENT<br/>compact, ordered, simple<br/>but a single point of coordination]
    B -->|No, distributed| C{Must IDs be<br/>time-sortable?}
    C -->|No| U4[UUIDv4<br/>zero coordination<br/>random: poor index locality]
    C -->|Yes| D{Need small IDs and<br/>can run a service /<br/>assign worker IDs?}
    D -->|Yes| SNOW[Snowflake<br/>64-bit: time + worker + seq<br/>needs worker-ID assignment + clock care]
    D -->|No| U7[UUIDv7<br/>128-bit, time-ordered prefix<br/>no coordination at all]
    A --> E{Exposed in URLs?}
    E -->|Yes| HASH[Don't leak volume:<br/>use a random or hashed public ID<br/>sequential IDs enumerate your data]
```

**Say it:** "My default in a distributed system is UUIDv7 — it needs no coordination and its time-ordered prefix keeps B-tree inserts local, which is exactly what UUIDv4 gets wrong: random IDs scatter writes across the index and destroy cache locality. I'd reach for Snowflake when 64 bits matters for index size at scale, accepting that I now have to assign worker IDs and handle clock skew. And I'd never expose a sequential ID publicly — it tells competitors my order volume and lets anyone enumerate my records."

---

## Related

- Concept-recall flowcharts for every topic: [../FLOWCHARTS.md](../FLOWCHARTS.md)
- The numbers behind these tradeoffs: [numbers-to-know.md](numbers-to-know.md)
- Cloud-service equivalents for each leaf: [cloud-services-cheat-sheet.md](cloud-services-cheat-sheet.md)
- How to roll out the choice you just made: [../04-advanced-topics/02-system-reliability/04-deployment-safety.md](../04-advanced-topics/02-system-reliability/04-deployment-safety.md)
- Bounding the damage when the choice is wrong: [../04-advanced-topics/02-system-reliability/05-blast-radius-isolation.md](../04-advanced-topics/02-system-reliability/05-blast-radius-isolation.md)
