# 03 Rate Limiter — THE SCRIPT, run end to end

Procedure: `notes/THE_SCRIPT.md`. Decision tree: `notes/TEXT_TO_CODE.md`.

> **Read this AFTER your own attempt.** Phases 1–4 on paper first, 20 minutes.

This is the **cleanest strategy-pattern problem** in the set — three algorithms, one
interface, one call site. It is also where you learn the single most useful testing
trick in LLD: **inject the clock**.

---

## PHASE 1 — SCOPE (0:00–5:00)

> "So we're building a rate limiter: `allow(clientId)` returns true if the request may
> proceed, false if the client is over their limit.
>
> I'm scoping to a single process, in-memory — I'll talk about the distributed version
> at the end because that's where it gets interesting. No persistence.
>
> The key design decision is that there are several standard algorithms with genuinely
> different trade-offs, so I'll put them behind one interface. And I'll **inject the
> clock** rather than calling `System.currentTimeMillis()`, so it's testable without
> real sleeps. Sound good?"

Saying "inject the clock" in Phase 1 is a strong opening — most candidates discover
that problem 30 minutes in, when their test needs a `Thread.sleep(1000)`.

**The three questions:**

| Ask | What you're really doing |
|---|---|
| "Which algorithm — or should I show the trade-offs?" | fishing for the **interface** |
| "Per-client, or global?" | drives the `Map<String, State>` |
| "Single server or a fleet behind a load balancer?" | pre-loading the **distributed** follow-up |

---

## PHASE 2 — NOUNS (5:00–10:00)

```
Request   Client   Limit   Window   Bucket   Token   Clock   RateLimiter
```

**Merge and defer:**
- *"`Request` never materialises as an object — I only need the client id."*
- *"`Window`, `Bucket`, `Token` aren't entities; they're **internal state of the
  algorithms**. They'll live as fields inside the implementations, not as top-level
  classes."*

That second one matters. Beginners make `class Token` and it buys nothing.

Leaves: **RateLimiter, Clock, and per-client state.**

---

## PHASE 3 — DECIDE (10:00–15:00)

| Noun | Question asked | Answer |
|---|---|---|
| `RateLimiter` | Q3 — "three algorithms, same call" | **interface** |
| `FixedWindow` / `SlidingWindowLog` / `TokenBucket` | implementations | **class** each |
| clock | a function, not an entity | **`LongSupplier`** injected |
| per-client state | small mutable holder | field inside each impl |

### Why interface, not abstract class — say this

> *"The three algorithms share **no state** — a fixed window keeps a counter, a sliding
> log keeps timestamps, a token bucket keeps a fractional token count. Nothing to lift
> into a parent. Q2 is a clear NO, so interface."*

### Why `LongSupplier` and not a `Clock` class

> *"I only need 'what time is it' — one method returning a long. A whole `Clock`
> abstraction would be more than the problem needs. In tests I pass `() -> fakeTime`."*

Choosing the *smallest* abstraction that works is YAGNI applied correctly.

---

## PHASE 4 — API (15:00–20:00)

```java
interface RateLimiter {
    boolean allow(String clientId);
}

class FixedWindow implements RateLimiter {
    FixedWindow(int limit, long windowMs, LongSupplier now);
    public boolean allow(String clientId);
}

class SlidingWindowLog implements RateLimiter {
    SlidingWindowLog(int limit, long windowMs, LongSupplier now);
    public boolean allow(String clientId);
}

class TokenBucket implements RateLimiter {
    TokenBucket(long capacity, double refillPerMs, LongSupplier now);
    public boolean allow(String clientId);
}
```

**Say this:** *"The interface is one method. That's a good sign — it means the
abstraction is real, not invented. All the difference is in the state each
implementation keeps."*

**Checkpoint:** *"Want me to implement all three, or the two most different?"*
Asking is better than silently running out of time.

---

## PHASE 5 — CODE (20:00–35:00)

Do **TokenBucket** first if you only do one — it's the one that forces real reasoning
about time, and interviewers know it.

```java
public boolean allow(String id) {
    long t = now.getAsLong();
    double[] s = state.computeIfAbsent(id, k -> new double[]{capacity, t});
    s[0] = Math.min(capacity, s[0] + (t - s[1]) * refillPerMs);   // refill by elapsed time
    s[1] = t;
    if (s[0] >= 1) { s[0] -= 1; return true; }
    return false;
}
```

> *"The trick is that I don't run a background refill thread. I compute tokens lazily
> from elapsed time on each call — that's O(1), needs no scheduler, and works with a
> fake clock."*

Fixed window, for contrast — note how much simpler the state is:

```java
public boolean allow(String id) {
    long t = now.getAsLong();
    long[] s = state.computeIfAbsent(id, k -> new long[]{t, 0});   // [windowStart, count]
    if (t - s[0] >= windowMs) { s[0] = t; s[1] = 0; }              // new window, reset
    if (s[1] < limit) { s[1]++; return true; }
    return false;
}
```

---

## PHASE 6 — EXTEND (35:00–45:00)

### The proof, with a fake clock and zero sleeps — **verified**

```
FixedWindow: 3 per 1000ms
  burst of 5 -> YYYnn          (3 allowed, then blocked)
  after clock +1000ms -> Y     (allowed again)

TokenBucket: capacity 3, refill 1 per 500ms
  burst of 5 -> YYYnn          (burst up to capacity)
  after +500ms -> Yn           (exactly one token refilled)
```

> *"Same call site, same test harness, two completely different behaviours — and no
> `Thread.sleep` anywhere, so the whole suite runs in microseconds."*

### Follow-up #1 — "What's wrong with FixedWindow?"

The classic. Know it cold:

> *"The boundary burst. With 3 per second, a client can send 3 at 0.999s and 3 more at
> 1.001s — 6 requests in 2 milliseconds, while technically never breaking the limit.
> Sliding window log fixes it by keeping actual timestamps; token bucket softens it
> because the bucket doesn't reset, it refills."*

### Follow-up #2 — "Memory?"

> *"Sliding window log is the expensive one — it stores a timestamp per request, so
> a client sending 10k/sec costs 10k entries. Fixed window is two longs per client.
> Token bucket is two doubles. That's the real trade-off: sliding log is the most
> accurate and the most expensive."*

Accuracy-vs-memory is the axis the interviewer wants named.

### Follow-up #3 — "Per-client tiers, free vs paid" (README stretch)

> *"One new class, zero edits — a `TieredLimiter implements RateLimiter` that holds a
> `Map<Tier, RateLimiter>` and delegates. It's a rate limiter **made of** rate limiters,
> which works precisely because the interface is one method."*

Composition over configuration — a genuinely strong answer.

### Follow-up #4 — "Make it thread-safe; where's the contention?" (README stretch)

Three layers:

1. **In-process:** the read-modify-write on the per-client state is a race. Cheapest
   correct fix is locking per client — `ConcurrentHashMap` plus a lock on the state
   object — **not** `synchronized` on the whole limiter.
2. **Contention:** *"a global lock serialises every client through one monitor.
   Per-client striping means client A never blocks client B — the only contention
   left is a hot single client."*
3. **Multi-machine:** *"per-JVM counters mean N servers allow N× the limit. You move
   the counter to Redis — `INCR` with a TTL for fixed window, or a Lua script for
   token bucket to keep it atomic. Then you're trading accuracy for a network hop, and
   many systems accept approximate limiting per node instead."*

---

## Done when (from the README)

A `main()` proving for each implementation: burst allowed to the limit, then blocked,
then allowed after time advances — **fake clock, no `Thread.sleep` anywhere.**

---

## Self-check

- [ ] Said "inject the clock" in Phase 1, not after getting stuck
- [ ] Justified interface over abstract class (no shared state)
- [ ] Chose `LongSupplier` over a `Clock` class, and said why
- [ ] Explained the fixed-window boundary burst unprompted
- [ ] Named the accuracy-vs-memory trade-off across all three
- [ ] Gave all three concurrency layers, ending at Redis

Verified backing: `notes/oop_proofs/LldInterviewProofs.java` — class `Section3RateLimiterAndCache`, the rate-limiter half.
