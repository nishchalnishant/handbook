# 04 LRU Cache — THE SCRIPT, run end to end

Procedure: `notes/THE_SCRIPT.md`. Decision tree: `notes/TEXT_TO_CODE.md`.

> **Read this AFTER your own attempt.** Phases 1–4 on paper first.

This is the one problem in the set where **the data structure is the design**. Phase 3
is short; Phase 5 is where the difficulty lives. Budget your time accordingly — that
adjustment is itself a skill.

---

## PHASE 1 — SCOPE (0:00–5:00)

> "So we're building a fixed-capacity cache: `get`, `put`, and eviction when full.
>
> Scoping to in-memory, single process, no persistence. I'll do it generic in K and V.
>
> Two things drive the design: **get and put must both be O(1)**, which forces a
> specific data structure; and the **eviction policy should be swappable** — LRU, LFU,
> FIFO. I'll build LRU by hand rather than using `LinkedHashMap`, since the hand-built
> version is the point. Sound right?"

Naming the O(1) constraint yourself in Phase 1 shows you know where the problem is.

**The three questions:**

| Ask | What you're really doing |
|---|---|
| "Should eviction be pluggable, or just LRU?" | fishing for the **interface** |
| "Is `null` a legal value, or only 'absent'?" | a real API-design question most skip |
| "Thread-safe, or single-threaded?" | pre-loading the concurrency follow-up |

The `null` question is a genuine differentiator: if `null` is a legal value, `get`
returning `null` is ambiguous and you need `Optional` or a `containsKey` check.

---

## PHASE 2 — NOUNS (5:00–10:00)

```
Cache   Key   Value   Entry   Node   EvictionPolicy   Capacity
```

**Merge and defer:**
- *"`Key` and `Value` are type parameters, not classes."*
- *"`Capacity` is an int field."*
- *"`Node` is **internal** to the linked list — it should be a private static nested
  class, not part of the public API."*

Leaves: **Cache, EvictionPolicy** (+ a private `Node`).

Saying "`Node` is private, it's an implementation detail" is encapsulation in action.

---

## PHASE 3 — DECIDE (10:00–15:00)

| Noun | Question asked | Answer |
|---|---|---|
| `Cache<K,V>` | owns the map, mutable | **class**, generic |
| `EvictionPolicy<K>` | Q3 — "LRU, LFU, FIFO" | **interface** |
| `LruPolicy` / `LfuPolicy` / `FifoPolicy` | implementations | **class** each |
| `Node` | internal plumbing | **private static nested class** |

### The design decision worth stating

> *"The subtle part is what the eviction interface should expose. If it's just
> `K evict()`, the policy can't track usage. The policy needs to be **told about every
> access** — so the interface is four methods: `recordAccess`, `recordInsert`,
> `remove`, and `evictCandidate`. The cache owns the data; the policy owns the ordering."*

That separation — cache owns storage, policy owns ordering — is the whole design.

---

## PHASE 4 — API (15:00–20:00)

```java
interface EvictionPolicy<K> {
    void recordAccess(K key);     // get() hit
    void recordInsert(K key);     // new key added
    void remove(K key);           // explicitly removed
    K evictCandidate();           // who dies next
}

class Cache<K, V> {
    private final int capacity;
    private final Map<K, V> map;
    private final EvictionPolicy<K> policy;   // injected -> DIP

    Cache(int capacity, EvictionPolicy<K> policy);
    V get(K key);                 // null if absent
    void put(K key, V value);     // evicts when over capacity
    int size();
}
```

**Ownership, stated:** *"`Cache` never knows what LRU means. It asks the policy who to
evict. That's why adding LFU costs one class."*

**Checkpoint:** *"Shape agreed? Then let me draw the linked list before I code it."*

---

## PHASE 5 — CODE (20:00–35:00)

**Draw first.** This is the one problem where the README explicitly says drawing helps:

```
head (most recent)                       tail (evict here)
  [a] <-> [b] <-> [c] <-> [d]
```

`get(c)`: unlink `c`, push to front. `evict`: take `tail`. Both O(1).

The two primitives everything else is built from:

```java
private void unlink(Node<K> n) {
    if (n.prev != null) n.prev.next = n.next; else head = n.next;
    if (n.next != null) n.next.prev = n.prev; else tail = n.prev;
    n.prev = n.next = null;
}
private void pushFront(Node<K> n) {
    n.next = head; if (head != null) head.prev = n; head = n;
    if (tail == null) tail = n;
}
```

Then the policy is trivial:

```java
public void recordAccess(K key) {
    Node<K> n = nodes.get(key);
    if (n != null) { unlink(n); pushFront(n); }     // touch = move to front
}
public K evictCandidate() { return tail == null ? null : tail.key; }
```

And `put` in the cache:

```java
void put(K key, V value) {
    if (map.containsKey(key)) { map.put(key, value); policy.recordAccess(key); return; }
    if (map.size() >= capacity) {
        K victim = policy.evictCandidate();
        map.remove(victim); policy.remove(victim);
    }
    map.put(key, value); policy.recordInsert(key);
}
```

---

## PHASE 6 — EXTEND (35:00–45:00)

### The proof — same operations, two policies, different survivors — **verified**

```
Cache capacity 2, operations: put a, put b, get a, put c

LruPolicy   -> a=1     b=null  c=3      (kept 'a' — recently used)
FifoPolicy  -> a=null  b=2     c=3      (evicted 'a' — oldest)
```

> *"Identical call site, identical operations, different victim. The cache class was
> never edited — that's the strategy pattern doing its job."*

### Follow-up #1 — "Why isn't a singly linked list enough?" (README asks this)

Have this ready verbatim:

> *"Because eviction and access both need **removal from the middle** in O(1). With a
> singly linked list, once the map gives me the node I still can't unlink it — I don't
> have its predecessor, so I'd have to walk the list, which is O(n). The `prev` pointer
> is exactly what buys O(1)."*

This is the question the problem exists to ask.

### Follow-up #2 — "Prove it's correct"— **verified**

```
200 random ops vs LinkedHashMap(access-order) reference:
  mismatches: 0
  max size observed: 8 (capacity 8) -> never exceeded
```

> *"I differential-tested against `LinkedHashMap` with the access-order flag, which is
> Java's built-in LRU. 200 random ops, zero divergence, and the capacity invariant
> held throughout."*

Bringing your own oracle is a very strong move.

### Follow-up #3 — "Now make it LFU"

> *"One new class. LFU needs frequency counts, so `recordAccess` increments a counter
> and `evictCandidate` returns the minimum. Naively that's O(n) for the min — to keep
> it O(1) you keep buckets by frequency in a doubly linked list of lists. Same
> interface either way; `Cache` doesn't change."*

Knowing the O(1) LFU exists — and that it's harder — is worth saying even if you
don't implement it.

### Follow-up #4 — "Add TTL expiry" (README stretch)

> *"Store an expiry timestamp with each entry and treat expired entries as absent on
> read — lazy expiry, no background thread. If memory matters you add a periodic sweep.
> And **inject the clock**, same as the rate limiter, so it's testable."*

Reusing a technique across problems shows the toolkit is real.

### Follow-up #5 — "Fire a listener on eviction" (README stretch)

> *"That's the observer pattern — `List<EvictionListener<K,V>>`, notified in the evict
> path. Worth noting it should fire **after** the entry is removed, and that a
> misbehaving listener shouldn't be able to break the cache."*

### Follow-up #6 — "Thread safety?"

1. **In-process:** every op is a read-modify-write over map **and** list — both must
   move together, so a plain `ConcurrentHashMap` is not enough.
2. **Contention:** *"one lock serialises everything, and `get` becomes a writer because
   it reorders the list. That's the ugly part of concurrent LRU."*
3. **At scale:** *"real systems shard — N independent caches keyed by hash, so
   contention drops by N. Caffeine goes further and buffers reads, replaying them
   asynchronously, so reads don't block."*

---

## Done when (from the README)

- 200 random ops agree with a naive reference
- capacity never exceeded
- you can explain out loud why a singly linked list is not enough

---

## Self-check

- [ ] Named the O(1) constraint in Phase 1
- [ ] Kept `Node` private — encapsulation stated
- [ ] Designed the policy interface around `recordAccess`, not just `evict`
- [ ] Drew the pointers before coding
- [ ] Answered the singly-vs-doubly question crisply
- [ ] Differential-tested against `LinkedHashMap`

Verified backing: `notes/oop_proofs/LldInterviewProofs.java` — class `Section3RateLimiterAndCache`, the cache half.
