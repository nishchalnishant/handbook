---
tags: [coding, data-structures, design]
topic: design-a-data-structure
difficulty: mixed
---
# Design-a-Data-Structure Problems (L4 signature family)

## What this covers

> [!abstract] In this file
> **Covers:** Design-a-data-structure problems: support operations X/Y/Z in O(1) / O(log n) by composing maps, lists, heaps and sets.
> **You'll be able to:** Compose structures so each covers the other's weakness; state per-operation cost.
> **Prereqs:** Hashing, linked list, heap · **Pair with:** [Design ladder](../../05-review/02-ladders.md#ladder-12--design-a-data-structure-l4-signature) · **Time:** 2–3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Design Interview Checklist](#design-interview-checklist) · [Warm-up / Core](#logger-rate-limiter--warm-up) · [Stream and Event Systems](#design-underground-system--t1) · [Game and Grid State](#design-tic-tac-toe--t1) · [Heaps and Lazy Deletion](#design-a-food-rating-system--t2) · [Iterators](#zigzag-iterator--combination-iterator--t2) · [Concurrency and Advanced](#design-bounded-blocking-queue--t3)

> [!tip] If you only have 20 minutes
> **Do these first:** [Insert Delete GetRandom O(1)](#insert-delete-getrandom-o1--t1) · [LFU Cache](#lfu-cache--t1) · [Design Hit Counter](#design-hit-counter--t1) · [Design Underground System](#design-underground-system--t1) · [Design Browser History](#design-browser-history--t1) · [Design Tic-Tac-Toe](#design-tic-tac-toe--t1)
> **Template:** State the ops table with target complexities first, pick the two structures that cover each other's weak op, and say the sync invariant out loud.
> **Gotchas:** Lazy-deletion heaps need a source-of-truth map to validate the top · Snake: pop the tail before the collision test unless eating · Tic-Tac-Toe: counters, never the board · Time Based Key-Value Store lives in [Binary Search](../algorithms/04-binary-search.md#time-based-key-value-store-lc-981--t2).

---

> [!note] L4 signature family
> Derivation ladder for this family: [Pattern Ladders — Ladder 12](../../05-review/02-ladders.md#ladder-12--design-a-data-structure-l4-signature).
> Already covered elsewhere: **Min Stack** → [stack](05-stack.md), **LRU Cache** → [linked list](07-linked-list.md), **Kth Largest in Stream / Find Median** → [heap](10-heap.md).

## Design Interview Checklist

- **Start with the ops table**: list each required operation and its target complexity *before* choosing structures. The problem is the table.
- The universal move: **compose two structures so each covers the other's weak op**, then keep them in sync on every mutation.
- Swap-with-last turns "delete from middle of array" into O(1) — if order doesn't matter.
- When a heap must support arbitrary deletion: **lazy deletion** (validate top against a source of truth on pop).
- When history/versions are needed: append `(version, value)` pairs and binary-search them.
- Lazy deletion also fits when the container cannot delete arbitrary items (`heapq`): keep a source-of-truth map and discard stale tops on read.
- **Store aggregates, not events**: `[sum, count]` answers averages in O(1) and merges across shards.
- Always close with the follow-up trio: **thread safety** (one lock vs sharding), **persistence** (what is derived state and rebuildable), **scale** (what shards by key).
- Say the sync invariant out loud ("map and list always agree because…") — that sentence is what's graded.

---

### Logger Rate Limiter `💤 warm-up`

> [!example] Problem
> Design a logger that receives a stream of `(timestamp, message)` calls. `shouldPrintMessage` returns true only if the same message has not printed in the last 10 seconds.

> [!info] Approach
> A map `message → last printed timestamp`. Print iff the message is unseen or `timestamp - last >= 10`, updating the map only when you print. The trap: updating the timestamp on *rejected* messages, which lets a spammed message suppress itself forever.

> [!note]- Python Solution
> ```python
> class Logger:
>     def __init__(self):
>         self.last = {}
> >
>     def shouldPrintMessage(self, timestamp, message):
>         if message not in self.last or timestamp - self.last[message] >= 10:
>             self.last[message] = timestamp
>             return True
>         return False
> ```

> [!success] Complexity
> Time O(1) per call; Space O(#distinct messages).

> [!tip] Follow-up
> "Memory grows forever" → evict old entries lazily on each call, or keep a deque of (ts, msg) and purge entries older than 10s.

---

### Design Hit Counter `⚡ T1`

> [!example] Problem
> Count hits in the past 5 minutes (300 seconds). `hit(timestamp)` records a hit; `getHits(timestamp)` returns hits in `[timestamp-299, timestamp]`. Timestamps are non-decreasing.

> [!info] Approach
> A deque of timestamps. On `getHits`, pop from the left while the front is `<= timestamp - 300`. Because timestamps only increase, each hit enters and leaves the deque once — amortized O(1).

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> class HitCounter:
>     def __init__(self):
>         self.q = deque()
> >
>     def hit(self, timestamp):
>         self.q.append(timestamp)
> >
>     def getHits(self, timestamp):
>         while self.q and self.q[0] <= timestamp - 300:
>             self.q.popleft()
>         return len(self.q)
> ```

> [!success] Complexity
> Time amortized O(1); Space O(hits in window).

> [!tip] Follow-up
> "Millions of hits per second" — the deque explodes. Switch to a **300-slot circular buffer** of `(time, count)`: `idx = timestamp % 300`; if the stored time differs, reset the slot. Space becomes O(300) regardless of traffic. This follow-up is the reason the problem is asked.

---

### Insert Delete GetRandom O(1) `⚡ T1`

> [!example] Problem
> Implement a set supporting `insert(val)`, `remove(val)`, and `getRandom()` — each O(1) average, with every element equally likely for `getRandom`.

> [!info] Approach
> Ops table: hashset does insert/remove but can't do uniform random; array does random (`random.choice`) but O(n) remove. Compose: array of values + map `val → index`. Remove = **swap the target with the last element, then pop** — O(1), and only one map entry needs fixing. Order is destroyed, but nothing required order.

> [!note]- Python Solution
> ```python
> import random
> >
> class RandomizedSet:
>     def __init__(self):
>         self.arr = []
>         self.idx = {}
> >
>     def insert(self, val):
>         if val in self.idx:
>             return False
>         self.idx[val] = len(self.arr)
>         self.arr.append(val)
>         return True
> >
>     def remove(self, val):
>         if val not in self.idx:
>             return False
>         i, last = self.idx[val], self.arr[-1]
>         self.arr[i] = last
>         self.idx[last] = i
>         self.arr.pop()
>         del self.idx[val]
>         return True
> >
>     def getRandom(self):
>         return random.choice(self.arr)
> ```

> [!success] Complexity
> Time O(1) average per op; Space O(n).

> [!warning] Gotcha
> Update `idx[last]` **before** deleting `idx[val]` — when removing the last element itself they are the same key, and the order above handles that case for free (dry-run it).

> [!tip] Follow-up
> "Allow duplicates" (LC 381) → map value → *set of indices*; swap-with-last now must pick any index of `val` and update the moved element's index set.

---

### Random Pick with Weight `⚡ T1`

> [!example] Problem
> Given weights `w`, implement `pickIndex()` returning index `i` with probability `w[i] / sum(w)`.

> [!info] Approach
> Build the prefix-sum array once. Draw a uniform random integer in `[1, total]` and binary-search (`bisect_left`) for the first prefix ≥ it. Each index owns a segment of the number line proportional to its weight. This is two T1 patterns (prefix sums, binary search) composed — say that.

> [!note]- Python Solution
> ```python
> import random, bisect
> from itertools import accumulate
> >
> class Solution:
>     def __init__(self, w):
>         self.prefix = list(accumulate(w))
>         self.total = self.prefix[-1]
> >
>     def pickIndex(self):
>         target = random.randint(1, self.total)
>         return bisect.bisect_left(self.prefix, target)
> ```

> [!success] Complexity
> Time O(n) init, O(log n) per pick; Space O(n).

> [!tip] Follow-up
> "Weights get updated" → now you need O(log n) update + prefix query; *name* Fenwick/segment tree as the tool, don't implement ([skip policy](../../00-start-here/02-round-cheatsheet.md)).

---

### Snapshot Array `🎯 T2`

> [!example] Problem
> `set(index, val)`, `snap()` returns a snapshot id, `get(index, snap_id)` returns the value at that index as of that snapshot.

> [!info] Approach
> Copying the array per snapshot is the trap (O(n) per snap). Instead, each index keeps its own history list `[(snap_id, val)]`, appended only when written. `get` = binary search for the last entry with `snap_id <=` the requested one. Versioning by history + bisect is a reusable L4 idea.

> [!note]- Python Solution
> ```python
> import bisect
> >
> class SnapshotArray:
>     def __init__(self, length):
>         self.hist = [[(-1, 0)] for _ in range(length)]
>         self.snap_id = 0
> >
>     def set(self, index, val):
>         h = self.hist[index]
>         if h[-1][0] == self.snap_id:
>             h[-1] = (self.snap_id, val)
>         else:
>             h.append((self.snap_id, val))
> >
>     def snap(self):
>         self.snap_id += 1
>         return self.snap_id - 1
> >
>     def get(self, index, snap_id):
>         h = self.hist[index]
>         i = bisect.bisect_right(h, (snap_id, float('inf'))) - 1
>         return h[i][1]
> ```

> [!success] Complexity
> Time O(1) set/snap, O(log s) get (s = snapshots that wrote this index); Space O(total writes).

---

### Stock Price Fluctuation `🎯 T2`

> [!example] Problem
> A stream of `(timestamp, price)` records where a timestamp may be **corrected** by a later call. Support `current()` (price at latest timestamp), `maximum()`, `minimum()`.

> [!info] Approach
> Map `timestamp → price` is the source of truth (+ track latest timestamp). Max/min need heaps — but corrections invalidate heap entries. **Lazy deletion**: push `(price, timestamp)` on every update; on `maximum()`/`minimum()`, pop while the heap top's price disagrees with the map. Same trick as Sliding Window Median.

> [!note]- Python Solution
> ```python
> import heapq
> >
> class StockPrice:
>     def __init__(self):
>         self.price = {}
>         self.latest = 0
>         self.maxh, self.minh = [], []
> >
>     def update(self, timestamp, price):
>         self.price[timestamp] = price
>         self.latest = max(self.latest, timestamp)
>         heapq.heappush(self.maxh, (-price, timestamp))
>         heapq.heappush(self.minh, (price, timestamp))
> >
>     def current(self):
>         return self.price[self.latest]
> >
>     def maximum(self):
>         while -self.maxh[0][0] != self.price[self.maxh[0][1]]:
>             heapq.heappop(self.maxh)
>         return -self.maxh[0][0]
> >
>     def minimum(self):
>         while self.minh[0][0] != self.price[self.minh[0][1]]:
>             heapq.heappop(self.minh)
>         return self.minh[0][0]
> ```

> [!success] Complexity
> Time O(log n) update, amortized O(log n) max/min; Space O(n updates).

> [!tip] Alternatives
> A sorted container (`SortedList`) makes max/min O(1) with true O(log n) deletes — mention it, but lazy-delete heaps are the portable answer.

---

### LFU Cache `⚡ T1`

> [!example] Problem
> Like LRU, but evict the **least frequently used** key; break frequency ties by least *recently* used. `get` and `put` in O(1).

> [!tip] Recognize · Gotcha
> **Signal:** freq + LRU within freq · **Gotcha:** **Tie** LRU — **second** priority; **O(1)** requires careful structure.

> [!info] Approach
> Three synced parts: `key → (val, freq)`; `freq → OrderedDict of keys` (each an LRU list within that frequency); and `min_freq`. On any access, move the key from bucket `f` to `f+1`; if bucket `min_freq` emptied, `min_freq += 1`. On insert, evict the LRU key of bucket `min_freq` if full, then set `min_freq = 1`. It's LRU plus one more dimension — derive it from LRU, don't recall it.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, OrderedDict
> >
> class LFUCache:
>     def __init__(self, capacity):
>         self.cap = capacity
>         self.kv = {}                     # key -> (val, freq)
>         self.buckets = defaultdict(OrderedDict)  # freq -> keys (LRU order)
>         self.min_freq = 0
> >
>     def _touch(self, key):
>         val, f = self.kv[key]
>         del self.buckets[f][key]
>         if not self.buckets[f] and self.min_freq == f:
>             self.min_freq = f + 1
>         self.kv[key] = (val, f + 1)
>         self.buckets[f + 1][key] = None
> >
>     def get(self, key):
>         if key not in self.kv:
>             return -1
>         self._touch(key)
>         return self.kv[key][0]
> >
>     def put(self, key, value):
>         if self.cap == 0:
>             return
>         if key in self.kv:
>             self._touch(key)
>             self.kv[key] = (value, self.kv[key][1])
>             return
>         if len(self.kv) == self.cap:
>             old, _ = self.buckets[self.min_freq].popitem(last=False)
>             del self.kv[old]
>         self.kv[key] = (value, 1)
>         self.buckets[1][key] = None
>         self.min_freq = 1
> ```

> [!success] Complexity
> Time O(1) per op; Space O(capacity).

> [!warning] Gotcha
> `min_freq` only ever needs to increment by exactly 1 on a touch (the moved key was in the min bucket), and resets to 1 on every insert — if you find yourself scanning for the new min, the design is wrong.

---

### Peeking Iterator / Flatten Nested List Iterator `🎯 T2`

> [!example] Problem
> (a) Wrap an iterator to support `peek()`. (b) Given a nested list of integers and lists, implement an iterator returning integers in flattened order.

> [!info] Approach
> (a) Cache one element ahead; `peek` returns the cache, `next` returns it and refills.
> (b) The lazy version (what's graded): a stack holding the elements **reversed**; `hasNext` pops lists and pushes their reversed contents until the top is an integer. Flattening everything in the constructor works but fails the follow-up ("the list is huge / infinite").

> [!note]- Python Solution
> ```python
> class NestedIterator:
>     def __init__(self, nestedList):
>         self.stack = nestedList[::-1]
> >
>     def next(self):
>         return self.stack.pop().getInteger()
> >
>     def hasNext(self):
>         while self.stack:
>             top = self.stack[-1]
>             if top.isInteger():
>                 return True
>             self.stack.pop()
>             self.stack.extend(top.getList()[::-1])
>         return False
> ```

> [!success] Complexity
> Time amortized O(1) per element overall; Space O(depth + width).

> [!warning] Gotcha
> All the work lives in `hasNext`, and `next` must assume `hasNext` was called — say this contract out loud; it's the design point.

---

### Design Underground System `⚡ T1`

> [!example] Problem
> Implement `checkIn(id, station, t)`, `checkOut(id, station, t)` and `getAverageTime(start, end)` (average of all completed trips from `start` to `end`; the direction matters). A customer has at most one open trip at a time.

> [!info] API · Invariant
> `in_` holds only **open** trips (`id → (station, t)`). `agg` holds only **completed** trips (`(start, end) → [total_time, count]`). Check-out moves a trip from one to the other, so a trip is never counted before it finishes.

> [!abstract] Why this structure
> | Need | Choice | Why not the alternative |
> |---|---|---|
> | Open trip lookup by customer | `dict id → (station, t)` | Scanning a trip list is O(n) per check-out |
> | Average per route | store `[sum, count]`, divide on read | Storing every trip time makes the query O(trips) and memory unbounded |
> | Route key | tuple `(start, end)` | `"A->B"` string concat breaks if a station name contains the separator |

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> class UndergroundSystem:
>     def __init__(self):
>         self.in_ = {}                       # id -> (station, t)
>         self.agg = defaultdict(lambda: [0, 0])  # (a, b) -> [total, count]
>
>     def checkIn(self, id, stationName, t):
>         self.in_[id] = (stationName, t)
>
>     def checkOut(self, id, stationName, t):
>         start, t0 = self.in_.pop(id)
>         a = self.agg[(start, stationName)]
>         a[0] += t - t0
>         a[1] += 1
>
>     def getAverageTime(self, startStation, endStation):
>         total, cnt = self.agg[(startStation, endStation)]
>         return total / cnt
> ```

> [!success] Complexity
> Time O(1) per op; Space O(open trips + distinct routes).

> [!tip] Follow-up
> - "Same customer checks in twice" → LC guarantees it cannot; in production, overwrite or reject and say which.
> - "Thread safety" → per-customer ops are independent; a single lock is fine, or shard `agg` by route and make updates atomic.
> - "Average over the last hour only" → bucket `[sum, count]` per route per time window and expire old buckets.
> - "Persistence / scale" → `agg` is a commutative-merge aggregate (sum, count), so it shards by route and can be rebuilt from an event log.

---

### Design Browser History `⚡ T1`

> [!example] Problem
> `BrowserHistory(homepage)`, `visit(url)` (clears forward history), `back(steps)` and `forward(steps)` (move at most as far as possible, return the current URL).

> [!info] API · Invariant
> Two stacks: `back_s` (its top is the **current page**, never empty) and `fwd_s`. `back` moves pages from `back_s` to `fwd_s` but never pops the last one; `visit` pushes and clears `fwd_s`.

> [!abstract] Why this structure
> | Option | visit | back/forward k | Note |
> |---|---|---|---|
> | Two stacks (chosen) | O(1) | O(k) | Mirrors how a browser feels; trivially correct |
> | Array + cursor | O(1) amortized (truncate) | **O(1)** | Better if `steps` is large; `del arr[i+1:]` frees the tail |
> | Doubly linked list | O(1) | O(k) | Pointer bookkeeping with no benefit |
>
> The array-and-cursor version is the stronger answer when interviewers push on "steps can be 10^9".

> [!note]- Python Solution
> ```python
> class BrowserHistory:
>     def __init__(self, homepage):
>         self.back_s = [homepage]   # last element = current page
>         self.fwd_s = []
>
>     def visit(self, url):
>         self.back_s.append(url)
>         self.fwd_s.clear()
>
>     def back(self, steps):
>         while steps and len(self.back_s) > 1:
>             self.fwd_s.append(self.back_s.pop())
>             steps -= 1
>         return self.back_s[-1]
>
>     def forward(self, steps):
>         while steps and self.fwd_s:
>             self.back_s.append(self.fwd_s.pop())
>             steps -= 1
>         return self.back_s[-1]
> ```

> [!success] Complexity
> Time `visit` O(1) amortized, `back`/`forward` O(min(steps, history)); Space O(history).

> [!tip] Follow-up
> - "Make back/forward O(1)" → array + cursor `i`: `back` is `i = max(0, i - k)`, `visit` is `del a[i+1:]; a.append(url); i += 1`.
> - "Cap memory" → bound the history with a deque of max length (drops the oldest pages).
> - "Tabs" → one instance per tab; share nothing, so no locking is needed across tabs.

---

### Design Leaderboard `🎯 T2`

> [!example] Problem
> `addScore(playerId, score)` adds to a player's total (creating the player if new), `top(K)` returns the sum of the K highest totals, `reset(playerId)` sets the player's score to 0.

> [!info] API · Invariant
> `score[player]` is the single source of truth. `top` derives from it on demand, so there is no second structure to keep in sync.

> [!abstract] Why this structure
> | Option | add/reset | top(K) | Pick when |
> |---|---|---|---|
> | Dict + `heapq.nlargest` (chosen) | O(1) | O(n log K) | `top` is rare or K is tiny (the LC constraints) |
> | Dict + sorted container (`SortedList`, balanced BST) | O(log n) | O(K) (or O(log n) with subtree sums) | `top` is frequent / n is large |
> | Dict + max-heap with lazy deletion | O(log n) | O(K log n) | Mostly-increasing scores; stale entries are skipped |

Name the trade-off aloud: the simple version optimizes the update path, the sorted version optimizes the read path.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
>
> class Leaderboard:
>     def __init__(self):
>         self.score = defaultdict(int)
>
>     def addScore(self, playerId, score):
>         self.score[playerId] += score
>
>     def top(self, K):
>         return sum(heapq.nlargest(K, self.score.values()))
>
>     def reset(self, playerId):
>         self.score[playerId] = 0   # LC guarantees the player exists
> ```

> [!success] Complexity
> Time `add`/`reset` O(1), `top` O(n log K); Space O(n).

> [!tip] Follow-up
> - "top is called constantly" → keep a `SortedList` of `(score, id)`; on add/reset remove the old pair and insert the new one (O(log n)). `top(K)` sums the last K, or use an order-statistic tree with subtree sums for O(log n).
> - "Ties" → decide ordering by `(score desc, id asc)` and encode it in the key.
> - "Scale" → shard by player for writes; global top-K merges per-shard top-K lists (K-way merge).

---

### Design Tic-Tac-Toe `⚡ T1`

> [!example] Problem
> `TicTacToe(n)`; `move(row, col, player)` places a mark (moves are always valid) and returns the winner (`1` or `2`) if this move completes a row, column or diagonal, else `0`. Target: O(1) per move.

> [!info] API · Invariant
> Never store the board. Keep a signed counter per row, per column, and for each diagonal: player 1 adds +1, player 2 adds -1. A line is won exactly when a counter reaches +n or -n. A counter only changes for the lines the move touches, so only those need checking.

> [!abstract] Why this structure
> | Option | move | Space | Note |
> |---|---|---|---|
> | Counters (chosen) | O(1) | O(n) | Checks only the four lines through the cell |
> | Store board, rescan row/col/diags | O(n) | O(n^2) | The naive answer the question is designed to reject |

> [!note]- Python Solution
> ```python
> class TicTacToe:
>     def __init__(self, n):
>         self.n = n
>         self.rows = [0]*n
>         self.cols = [0]*n
>         self.diag = 0
>         self.anti = 0
>
>     def move(self, row, col, player):
>         d = 1 if player == 1 else -1
>         self.rows[row] += d
>         self.cols[col] += d
>         if row == col:
>             self.diag += d
>         if row + col == self.n - 1:
>             self.anti += d
>         t = self.n
>         if t in (abs(self.rows[row]), abs(self.cols[col]), abs(self.diag), abs(self.anti)):
>             return player
>         return 0
> ```

> [!success] Complexity
> Time O(1) per move; Space O(n).

> [!warning] Gotcha
> The anti-diagonal test is `row + col == n - 1`; for odd `n` the center belongs to both diagonals and must update both counters. Compare with `abs(counter) == n`; the game ends at the first win, so counters never exceed n.

> [!tip] Follow-up
> - "k-in-a-row on a large board" → counters no longer work (a win is a window, not a full line); keep per-line run lengths or check the four directions outward from the move in O(k).
> - "Undo" → store the move list and reverse the counter updates.

---

### Design Snake Game `🎯 T2`

> [!example] Problem
> Snake starts length 1 at `(0,0)` on a `height x width` grid with a food queue. `move(direction)` returns the score, or `-1` if the snake hits a wall or itself. Eating food grows the snake by one and spawns the next food only after the previous is eaten.

> [!info] API · Invariant
> `body` (deque, head at the right) is the ordered snake; `occ` (set) is the same cells for O(1) membership. They change together on every step: append head, and pop the tail unless food was eaten.

> [!abstract] Why this structure
> | Need | Choice | Why not the alternative |
> |---|---|---|
> | Ordered body, pop tail / push head | `deque` | `list.pop(0)` is O(n) |
> | Self-collision test | `set` of occupied cells | Scanning the deque is O(length) per move |
> | Food order | `deque` of food positions | Only the **front** food is ever on the board |

> [!note]- Python Solution
> ```python
> from collections import deque
>
> class SnakeGame:
>     DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
>
>     def __init__(self, width, height, food):
>         self.w, self.h = width, height
>         self.food = deque(map(tuple, food))
>         self.body = deque([(0, 0)])      # head = right end
>         self.occ = {(0, 0)}
>         self.score = 0
>
>     def move(self, direction):
>         dr, dc = self.DIRS[direction]
>         r, c = self.body[-1]
>         nr, nc = r + dr, c + dc
>         if not (0 <= nr < self.h and 0 <= nc < self.w):
>             return -1
>         eating = bool(self.food) and self.food[0] == (nr, nc)
>         if not eating:                   # tail moves away first, so head may enter old tail cell
>             self.occ.discard(self.body.popleft())
>         else:
>             self.food.popleft()
>             self.score += 1
>         if (nr, nc) in self.occ:
>             return -1
>         self.body.append((nr, nc))
>         self.occ.add((nr, nc))
>         return self.score
> ```

> [!success] Complexity
> Time O(1) per move; Space O(snake length + foods).

> [!warning] Gotcha
> Remove the tail **before** the collision test when not eating: the head is allowed to move into the cell the tail is vacating this very step. When eating, the tail stays, so that cell is still occupied. Getting this order wrong fails the "chase the tail" case.

> [!tip] Follow-up
> - "Random food placement" → keep a list of free cells and use swap-with-last removal (see Insert Delete GetRandom O(1)) so spawning is O(1).
> - "Wrap-around walls" → replace the bounds check with modulo arithmetic.

---

### All O(1) Data Structure `🎯 T2`

> [!example] Problem
> `inc(key)`, `dec(key)` (removes the key at 0), `getMaxKey()`, `getMinKey()` (any key with max/min count, `""` if empty), all in O(1).

> [!info] API · Invariant
> A doubly linked list of **buckets**, ordered by count ascending, each holding the set of keys with that count; `where[key]` points to the key's bucket. Counts change by exactly 1, so a key moves only to the **adjacent** bucket, creating it if needed. Invariant: no empty bucket stays in the list, so `head.next` is always the min bucket and `tail.prev` the max bucket.

> [!abstract] Why this structure
> | Option | inc/dec | getMax/Min | Why it fails |
> |---|---|---|---|
> | Dict of counts only | O(1) | O(n) | Max/min need a scan |
> | Heap + lazy deletion | O(log n) | O(log n) amortized | Not O(1) |
> | Bucket list + key sets (chosen) | O(1) | O(1) | `+1/-1` keeps neighbors adjacent, so no search is needed |

Sentinel head (count 0) and tail (count infinity) remove every edge-case branch: a brand-new key "comes from" the head bucket.

> [!note]- Python Solution
> ```python
> class _Bucket:
>     __slots__ = ("cnt", "keys", "prev", "next")
>     def __init__(self, cnt):
>         self.cnt, self.keys, self.prev, self.next = cnt, set(), None, None
>
> class AllOne:
>     def __init__(self):
>         self.head, self.tail = _Bucket(0), _Bucket(float('inf'))   # sentinels
>         self.head.next, self.tail.prev = self.tail, self.head
>         self.where = {}                 # key -> bucket
>
>     def _insert_after(self, node, cnt):
>         b = _Bucket(cnt)
>         b.prev, b.next = node, node.next
>         node.next.prev = b
>         node.next = b
>         return b
>
>     def _remove_if_empty(self, b):
>         if not b.keys:
>             b.prev.next, b.next.prev = b.next, b.prev
>
>     def inc(self, key):
>         cur = self.where.get(key, self.head)
>         nxt = cur.next
>         if nxt.cnt != cur.cnt + 1:
>             nxt = self._insert_after(cur, cur.cnt + 1)
>         nxt.keys.add(key)
>         self.where[key] = nxt
>         if cur is not self.head:
>             cur.keys.discard(key)
>             self._remove_if_empty(cur)
>
>     def dec(self, key):
>         cur = self.where[key]
>         if cur.cnt == 1:
>             del self.where[key]
>         else:
>             prv = cur.prev
>             if prv.cnt != cur.cnt - 1:
>                 prv = self._insert_after(prv, cur.cnt - 1)
>             prv.keys.add(key)
>             self.where[key] = prv
>         cur.keys.discard(key)
>         self._remove_if_empty(cur)
>
>     def getMaxKey(self):
>         return next(iter(self.tail.prev.keys)) if self.tail.prev is not self.head else ""
>
>     def getMinKey(self):
>         return next(iter(self.head.next.keys)) if self.head.next is not self.tail else ""
> ```

> [!success] Complexity
> Time O(1) per op; Space O(distinct keys).

> [!tip] Follow-up
> - "inc by arbitrary delta" → the target bucket may not be adjacent; O(1) is lost unless you walk from the current bucket (cost proportional to the gap).
> - "Thread safety" → one lock around each op; the list surgery touches several nodes and must be atomic.

---

### Design a Food Rating System `🎯 T2`

> [!example] Problem
> Given `foods`, `cuisines`, `ratings`: `changeRating(food, newRating)` and `highestRated(cuisine)` (highest rating; ties broken by lexicographically smaller name).

> [!info] API · Invariant
> `info[food] = [cuisine, current_rating]` is the **source of truth**. Each cuisine has a heap of `(-rating, name)` that may contain stale entries. Invariant: a heap entry is valid iff its rating equals `info[name]`'s current rating; the top is validated and discarded if stale before being returned.

> [!abstract] Why this structure
> | Option | change | highest | Note |
> |---|---|---|---|
> | Heap per cuisine + lazy deletion (chosen) | O(log n) | O(log n) amortized | Each stale entry is popped at most once |
> | `SortedList` per cuisine | O(log n) | O(1) | No stale entries, but not in the stdlib |
> | Re-scan the cuisine | O(1) | O(n) | Too slow when queries are frequent |
> | Heap with true delete | needs an index map | | `heapq` cannot delete arbitrary items |

Heap ordering `(-rating, name)` gives ties-by-name for free, because tuples compare name ascending.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
>
> class FoodRatings:
>     def __init__(self, foods, cuisines, ratings):
>         self.info = {}                          # food -> [cuisine, rating]
>         self.heaps = defaultdict(list)          # cuisine -> heap of (-rating, food)
>         for f, c, r in zip(foods, cuisines, ratings):
>             self.info[f] = [c, r]
>             heapq.heappush(self.heaps[c], (-r, f))
>
>     def changeRating(self, food, newRating):
>         c, _ = self.info[food]
>         self.info[food][1] = newRating
>         heapq.heappush(self.heaps[c], (-newRating, food))   # old entry stays; lazily dropped
>
>     def highestRated(self, cuisine):
>         h = self.heaps[cuisine]
>         while -h[0][0] != self.info[h[0][1]][1]:            # stale?
>             heapq.heappop(h)
>         return h[0][1]
> ```

> [!success] Complexity
> Time `changeRating` O(log n), `highestRated` O(log n) amortized; Space O(n + #changes) because stale entries linger until popped.

> [!warning] Gotcha
> A food re-set to a rating it had before still has an old entry with that same rating; the entry is then "valid" again, which is harmless because it represents the same `(rating, name)` pair.

> [!tip] Follow-up
> - "Stale entries blow up memory" → rebuild a cuisine's heap when `len(heap) > 2 * live_foods` (periodic compaction).
> - "Persistence" → ratings change log plus snapshot; heaps are derived state and can be rebuilt.

---

### Design Phone Directory / Seat Reservation Manager `🎯 T2`

> [!example] Problem
> (a) **Seat Reservation Manager**: seats `1..n`; `reserve()` returns the smallest unreserved seat, `unreserve(seat)` frees one. (b) **Phone Directory**: `get()` returns any free number or `-1`, `check(n)` tests availability, `release(n)` frees a number.

> [!info] API · Invariant
> (a) Seats `>= next_unused` have never been handed out; seats in the `freed` min-heap were handed out and returned. The smallest available seat is `min(heap top, next_unused)`, and the heap top is always smaller than `next_unused`, so check the heap first. (b) A queue of free numbers plus a set mirroring it: both always contain exactly the free numbers.

> [!abstract] Why this structure
> | Problem | Choice | Why not the alternative |
> |---|---|---|
> | (a) smallest free | `next_unused` counter + min-heap of released | Pre-filling a heap with `1..n` costs O(n) memory and time up front |
> | (b) any free | `deque` + `set` | "any" does not need ordering, so a heap is wasted work |
> | (b) `check` | set membership | Scanning the deque is O(n) |

> [!note]- Python Solution
> ```python
> import heapq
> from collections import deque
>
> class SeatManager:
>     def __init__(self, n):
>         self.next_unused = 1
>         self.n = n
>         self.freed = []                  # min-heap of released seats
>
>     def reserve(self):
>         if self.freed:
>             return heapq.heappop(self.freed)
>         s = self.next_unused
>         self.next_unused += 1
>         return s
>
>     def unreserve(self, seatNumber):
>         heapq.heappush(self.freed, seatNumber)
>
> class PhoneDirectory:
>     def __init__(self, maxNumbers):
>         self.free = deque(range(maxNumbers))
>         self.free_set = set(self.free)
>
>     def get(self):
>         if not self.free:
>             return -1
>         x = self.free.popleft()
>         self.free_set.remove(x)
>         return x
>
>     def check(self, number):
>         return number in self.free_set
>
>     def release(self, number):
>         if number not in self.free_set:      # idempotent: ignore double release
>             self.free_set.add(number)
>             self.free.append(number)
> ```

> [!success] Complexity
> (a) `reserve`/`unreserve` O(log n), O(1) when nothing was released; (b) all ops O(1). Space O(n) worst case.

> [!tip] Follow-up
> - "Release a seat that is not reserved" → guard with a `reserved` set, otherwise the heap fills with duplicates (the directory version above is idempotent for this reason).
> - "Smallest free seat with a huge n" → the counter approach already handles it; a segment tree is the alternative for range queries.
> - "Concurrency" → one lock; contention is on the shared heap, so shard by seat range if hot.

---

### Design Bounded Blocking Queue `💤 T3`

> [!example] Problem
> Thread-safe FIFO queue with fixed `capacity`: `enqueue` blocks while full, `dequeue` blocks while empty.

> [!info] API · Invariant
> One lock guarding `q`, and two condition variables **on that same lock**: `not_full` (producers wait) and `not_empty` (consumers wait). Invariant: `0 <= len(q) <= cap` whenever the lock is released. Every wait sits in a `while` loop that re-checks the predicate.

> [!abstract] Why this structure
> | Option | Why / why not |
> |---|---|
> | Two `Condition`s on one lock (chosen) | `notify()` wakes exactly the right kind of waiter |
> | One `Condition` + `notify_all()` | Correct but thundering herd; every wake-up re-checks |
> | `queue.Queue(maxsize)` | Production answer; the interview wants the mechanism |
> | Semaphores (`empty`/`full`) + mutex | Classic alternative; three primitives instead of one lock |

> [!note]- Python Solution
> ```python
> import threading
> from collections import deque
>
> class BoundedBlockingQueue:
>     def __init__(self, capacity):
>         self.cap = capacity
>         self.q = deque()
>         lock = threading.Lock()
>         self.not_full = threading.Condition(lock)    # two conditions, ONE shared lock
>         self.not_empty = threading.Condition(lock)
>
>     def enqueue(self, element):
>         with self.not_full:
>             while len(self.q) == self.cap:           # while, not if: spurious wakeups / stolen slot
>                 self.not_full.wait()
>             self.q.append(element)
>             self.not_empty.notify()
>
>     def dequeue(self):
>         with self.not_empty:
>             while not self.q:
>                 self.not_empty.wait()
>             x = self.q.popleft()
>             self.not_full.notify()
>             return x
>
>     def size(self):
>         with self.not_empty:
>             return len(self.q)
> ```

> [!success] Complexity
> Time O(1) per op plus blocking; Space O(capacity).

> [!warning] Gotcha
> Concurrency is a senior-level follow-up, not a core L3/L4 requirement: be ready to explain it, not to derive it cold. `while` (not `if`) around `wait()` is the line interviewers look for; `if` breaks when another thread steals the slot between notify and wake-up. Never `wait()` without holding the lock.

> [!tip] Follow-up
> - "Timeouts" → `cond.wait(timeout)` or `wait_for(predicate, timeout)`.
> - "Shutdown" → add a `closed` flag; wake everyone with `notify_all()` and have waiters re-check it.
> - "Scale" → single-process only; across machines this is a message broker with acks and backpressure.

---

### Zigzag Iterator / Combination Iterator `🎯 T2`

> [!example] Problem
> (a) **Zigzag Iterator**: alternate elements from two lists (generalize to `k` lists); skip lists as they run out. (b) **Combination Iterator**: given sorted distinct `characters` and a length `k`, `next()` returns the next combination in lexicographic order; `hasNext()` says whether one remains.

> [!info] API · Invariant
> (a) A queue of `(list, next_index)` pairs for lists that still have elements; `next` pops the front, re-enqueues it if it has more, so round-robin falls out for any `k`. (b) Keep the **current** combination as sorted indices; `_advance` finds the rightmost index not yet at its maximum `n-k+i`, increments it, and resets everything to its right to consecutive values. Generating lazily avoids materializing C(n, k) combinations.

> [!abstract] Why this structure
> | Problem | Choice | Why not the alternative |
> |---|---|---|
> | (a) | `deque` of `(list, idx)` | Two-pointer toggling works for 2 lists but needs rewriting for k |
> | (b) | Index odometer | Precomputing all combinations is O(C(n,k)) memory up front |
> | (b) | `itertools.combinations` | Fine in practice; the interview wants the incremental step |

> [!note]- Python Solution
> ```python
> from collections import deque
>
> class ZigzagIterator:
>     def __init__(self, *lists):
>         self.q = deque((l, 0) for l in lists if l)    # (list, next index)
>
>     def next(self):
>         l, i = self.q.popleft()
>         if i + 1 < len(l):
>             self.q.append((l, i + 1))
>         return l[i]
>
>     def hasNext(self):
>         return bool(self.q)
>
> class CombinationIterator:
>     def __init__(self, characters, combinationLength):
>         self.s, self.k = characters, combinationLength
>         self.idx = list(range(self.k))                 # current combination as indices
>         self.has = self.k <= len(self.s)
>
>     def next(self):
>         res = "".join(self.s[i] for i in self.idx)
>         self._advance()
>         return res
>
>     def hasNext(self):
>         return self.has
>
>     def _advance(self):
>         n, k, idx = len(self.s), self.k, self.idx
>         i = k - 1
>         while i >= 0 and idx[i] == n - k + i:          # rightmost index that can still move
>             i -= 1
>         if i < 0:
>             self.has = False
>             return
>         idx[i] += 1
>         for j in range(i + 1, k):
>             idx[j] = idx[j - 1] + 1
> ```

> [!success] Complexity
> (a) `next` O(1), `hasNext` O(1); Space O(k). (b) `next` O(k), `hasNext` O(1); Space O(k).

> [!warning] Gotcha
> In (a), drop empty input lists in the constructor, otherwise `hasNext` lies. In (b), `hasNext` is a stored flag computed after each advance, never by peeking at the generator.

> [!tip] Follow-up
> "Input lists are huge/streamed" → hold iterators instead of lists and prefetch one element each, like Peeking Iterator.

---

### Design Skiplist `💤 T3`

> [!example] Problem
> Implement `search`, `add`, `erase` (removes one occurrence) with O(log n) expected time, without built-in balanced trees. Duplicates are allowed.

> [!info] API · Invariant
> Layered sorted linked lists. Level 0 contains every node in order; each node is promoted to the next level with probability 1/2, so level `i` has about n/2^i nodes. Search starts at the top level and drops down when the next node is too large. `_find_preds` records the last node `< target` on every level, which both `add` (splice) and `erase` (unlink) reuse.

> [!abstract] Why this structure
> | Option | Ops | Note |
> |---|---|---|
> | Skiplist | O(log n) expected | Simple to write, easy lock-free/concurrent variants |
> | Balanced BST (AVL/red-black) | O(log n) worst | Rotations are painful to write live |
> | Sorted array + bisect | O(log n) search, O(n) insert | Memmove is fast in practice |

> [!note]- Python Solution
> ```python
> import random
>
> class _Node:
>     __slots__ = ("val", "nxt")
>     def __init__(self, val, level):
>         self.val = val
>         self.nxt = [None] * level
>
> class Skiplist:
>     MAX_LEVEL, P = 16, 0.5
>
>     def __init__(self):
>         self.head = _Node(-1, self.MAX_LEVEL)
>         self.level = 1
>
>     def _rand_level(self):
>         lv = 1
>         while lv < self.MAX_LEVEL and random.random() < self.P:
>             lv += 1
>         return lv
>
>     def _find_preds(self, target):
>         preds = [self.head] * self.MAX_LEVEL
>         cur = self.head
>         for i in range(self.level - 1, -1, -1):
>             while cur.nxt[i] and cur.nxt[i].val < target:
>                 cur = cur.nxt[i]
>             preds[i] = cur
>         return preds
>
>     def search(self, target):
>         cur = self._find_preds(target)[0].nxt[0]
>         return cur is not None and cur.val == target
>
>     def add(self, num):
>         preds = self._find_preds(num)
>         lv = self._rand_level()
>         self.level = max(self.level, lv)
>         node = _Node(num, lv)
>         for i in range(lv):
>             node.nxt[i] = preds[i].nxt[i]
>             preds[i].nxt[i] = node
>
>     def erase(self, num):
>         preds = self._find_preds(num)
>         node = preds[0].nxt[0]
>         if node is None or node.val != num:
>             return False
>         for i in range(len(node.nxt)):
>             if preds[i].nxt[i] is not node:
>                 break
>             preds[i].nxt[i] = node.nxt[i]
>         while self.level > 1 and self.head.nxt[self.level - 1] is None:
>             self.level -= 1
>         return True
> ```

> [!success] Complexity
> Time O(log n) expected per op; Space O(n) expected (about 2n pointers).

> [!tip] Follow-up
> Why skiplists over trees: concurrent updates only touch local pointers (Redis sorted sets and LevelDB memtables use them). It is a T3 problem; know the idea, do not memorize the code.

---

### Encode and Decode TinyURL `🎯 T2`

> [!example] Problem
> `encode(longUrl)` returns a short URL; `decode(shortUrl)` returns the original. Any scheme is allowed as long as decode inverts encode.

> [!info] API · Invariant
> Two maps kept in sync: `code → url` (for decode) and `url → code` (so encoding the same URL twice is idempotent). Invariant: every code maps to exactly one URL, so generation retries on collision.

> [!abstract] Why this structure
> | Scheme | Pros | Cons |
> |---|---|---|
> | Random 6-char base62 + collision retry (chosen) | Unguessable codes, no coordination | 62^6 is about 5.7e10; retries rise as the table fills |
> | Counter encoded in base62 | No collisions, shortest codes | Sequential, so enumerable; needs a distributed counter at scale |
> | Hash (MD5/SHA) truncated | Stateless dedup | Collisions need handling anyway |

Use `secrets` for the random scheme if codes must be unguessable (`random` is predictable).

> [!note]- Python Solution
> ```python
> import secrets
> import string
>
> class Codec:
>     ALPHABET = string.ascii_letters + string.digits
>     BASE = "http://tinyurl.com/"
>
>     def __init__(self):
>         self.code_to_url = {}
>         self.url_to_code = {}
>
>     def encode(self, longUrl):
>         if longUrl in self.url_to_code:                  # idempotent
>             return self.BASE + self.url_to_code[longUrl]
>         while True:
>             code = "".join(secrets.choice(self.ALPHABET) for _ in range(6))
>             if code not in self.code_to_url:             # retry on collision
>                 break
>         self.code_to_url[code] = longUrl
>         self.url_to_code[longUrl] = code
>         return self.BASE + code
>
>     def decode(self, shortUrl):
>         return self.code_to_url[shortUrl[len(self.BASE):]]
> ```

> [!success] Complexity
> Time O(1) expected per op; Space O(#URLs).

> [!tip] Follow-up (this is a mini system design)
> - "Scale / availability" → key-range allocation per app server (each grabs a block of counter values) so no per-request coordination; cache hot decodes; the read:write ratio is heavily read-biased.
> - "Expiry / custom aliases" → store TTL with the mapping; alias is a unique-key insert that can fail.
> - "Same URL, different users" → drop the `url → code` map, or key it by `(user, url)`.
> - "Analytics" → the redirect path emits an event asynchronously; never block the redirect on it.
