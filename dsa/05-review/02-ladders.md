---
module: 05-review
topic: Pattern Ladders
tags: [patterns, ladders, practice, google-l3, l4]
---
# Pattern Ladders — Graded Problem Sequences

## What this covers

> [!abstract] In this file
> **Covers:** Twelve graded ladders where each rung changes exactly one thing from the previous, plus the study protocol.
> **You'll be able to:** Solve an unseen problem by testing which invariant applies, not by recalling a lookalike.
> **Prereqs:** [How to think](../01-foundations/01-how-to-think.md) + the lecture for each pattern · **Pair with:** [Pattern sheet](01-pattern-sheet.md) · **Time:** 2–3 weeks

**Sections:** [The study protocol (non-negotiable)](#the-study-protocol-non-negotiable) · [Ladder 1 — Sliding Window](#ladder-1--sliding-window) · [Ladder 2 — Two Pointers (converging)](#ladder-2--two-pointers-converging) · [Ladder 3 — Binary Search (on index → on answer)](#ladder-3--binary-search-on-index--on-answer) · [Ladder 4 — Hashing for O(n) lookups](#ladder-4--hashing-for-on-lookups) · [Ladder 5 — BFS / DFS on grids & graphs](#ladder-5--bfs--dfs-on-grids--graphs) · [Ladder 6 — Monotonic Stack](#ladder-6--monotonic-stack) · [Ladder 7 — Heaps & Top-K](#ladder-7--heaps--top-k) · [Ladder 8 — Shortest Path Beyond BFS](#ladder-8--shortest-path-beyond-bfs) · [Ladder 9 — Recursion → Backtracking](#ladder-9--recursion--backtracking) · [Ladder 10 — Recursion → DP](#ladder-10--recursion--dp) · [Ladder 11 — Intervals & Sweep](#ladder-11--intervals--sweep) · [Ladder 12 — Design-a-Data-Structure (L4 signature)](#ladder-12--design-a-data-structure-l4-signature) · [After the ladders](#after-the-ladders) · [See Also](#see-also)

---

> **The problem this part solves:** the rest of the repo is organized topic-first with per-problem "key insights." That builds *recognition*, which fails on unseen problems. This part builds *derivation*: for each pattern you learn one **invariant** (the reason the pattern works), then climb a ladder of problems where each rung changes exactly **one thing** from the previous. When the interview problem is new, you don't search memory for a lookalike — you check which invariant applies.

## The study protocol (non-negotiable)

Same rules as [the training protocol](../01-foundations/01-how-to-think.md#the-training-protocol-how-to-study-this-file), specialized to ladders:

1. **Read only the invariant** at the top of a ladder. Not the rungs' annotations.
2. **Attempt each rung for 20 min** before reading anything. Struggling *is* the mechanism — an insight you derived is stored differently from one you read.
3. If stuck, read only the **"what changed"** line (the ladder's version of "key insight only"). Try 10 more minutes.
4. Log the miss by cause: *"the trigger I missed was ___."*
5. **Spaced repetition on triggers, not solutions.** Re-attempt failed rungs at +2 days and +7 days. Re-reading a solution you've seen is near-zero learning.
6. One ladder at a time — the single-delta ordering is the point.

Time per rung, not per ladder: if a rung falls in 5 minutes, move on immediately.

Tier tags (`⚡ T1` / `🎯 T2`) match the canonical tiers in `04-practice/`; a rung's tier says how likely it is to appear, not how hard the rung is.

---

## Ladder 1 — Sliding Window

**Invariant:** a window `[l, r]` maintains a property P. Grow `r` until P breaks; shrink `l` until P is restored. This is O(n) *because each pointer only moves forward* — every element enters and leaves the window at most once. The pattern applies iff **P is monotone**: extending a bad window keeps it bad (or extending a good one keeps it good). If adding an element can *fix* a violation (e.g., sums with negative numbers), the invariant is dead — use prefix sums instead.

| # | Problem | What changed from previous rung |
|---|---------|---------------------------------|
| 1 | Best Time to Buy/Sell Stock `🎯 T2` | Degenerate window: track min-so-far. The "window" is implicit. |
| 2 | Longest Substring Without Repeating Characters `⚡ T1` | P = "no duplicates," tracked with a set. First real grow/shrink loop. |
| 3 | Max Consecutive Ones III `⚡ T1` | P becomes a **budget** ("≤ k zeros") instead of a boolean property. |
| 4 | Longest Repeating Character Replacement `⚡ T1` | Budget is now *derived*: `window_len - max_freq ≤ k`. Bonus insight: `max_freq` never needs to shrink. |
| 5 | Permutation in String `⚡ T1` | Window becomes **fixed-size**; P = "counts match." Compare via a `matches` counter, not full dict compare. |
| 6 | Minimum Window Substring `⚡ T1` | Flip the objective: **shrink for the answer** (minimize) instead of grow. Record answer on valid, not on invalid. |
| 7 | Sliding Window Maximum `⚡ T1` | The tracked property needs a **monotonic deque** — window + mono-structure composition. Bridge to Ladder 6. |

**Failure drill:** "Subarray Sum Equals K" with negatives — explain in one sentence why the window breaks and what replaces it (prefix-sum hashmap).

---

## Ladder 2 — Two Pointers (converging)

**Invariant:** on a **sorted** (or otherwise monotone) structure, comparing the two ends lets you discard one element *with certainty* — the discarded element can't be in any better answer. O(n) because every step discards someone forever. If you can't state *why* the discard is safe, the pattern doesn't apply.

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Two Sum II (sorted) `⚡ T1` | The base move: sum too small → `l++` (nothing pairs with `a[l]` anymore), too big → `r--`. |
| 2 | Valid Palindrome `🎯 T2` | Same converging move; the "compare" is equality, not a sum. |
| 3 | Container With Most Water `⚡ T1` | The discard argument gets subtle: move the **shorter** wall — keeping it can never beat the current answer. Say the proof out loud. |
| 4 | 3Sum `⚡ T1` | Wrap the two-pointer scan in an outer loop; new sub-skill = **duplicate skipping** at both levels. |
| 5 | Trapping Rain Water `⚡ T1` | Discard argument on **maxes**: the side with smaller max is fully determined regardless of the other side. Hardest proof in the ladder. |

---

## Ladder 3 — Binary Search (on index → on answer)

**Invariant:** you need a **monotone predicate** `f(x)`: false…false,true…true. Binary search finds the boundary. The array being sorted is just the special case `f(x) = a[x] >= target`. The L4 move is inventing `f` when there's no array at all.

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Binary Search / First & Last Position `⚡ T1` | Boundary template: `while l < r`, bias mid correctly. Own ONE template. |
| 2 | Search in Rotated Sorted Array `⚡ T1` | Array not fully sorted — but **one half always is**; test which, then decide side. |
| 3 | Find Minimum in Rotated Sorted Array `⚡ T1` | Compare `mid` to `right` instead of to a target. Predicate = "am I in the right segment?" |
| 4 | Koko Eating Bananas `⚡ T1` | **The big leap:** search the *answer space* (speed k), predicate = "can finish in h hours?" No array anywhere. |
| 5 | Split Array Largest Sum `⚡ T1` | Same answer-space search; predicate is now a **greedy feasibility check**. Two patterns composed. |
| 6 | Median of Two Sorted Arrays `⚡ T1` | Search a **partition point**; predicate = "left maxes ≤ right mins." L4 stretch rung. |

**Trigger to burn in:** "minimize the maximum / maximize the minimum" ⇒ binary search on answer, almost always.

---

## Ladder 4 — Hashing for O(n) lookups

**Invariant:** you're scanning and repeatedly asking "have I seen X before?" where X is *computable from the current element* (complement, prefix sum, canonical form). The hashmap trades O(n) space to make that question O(1). The creative step is always **choosing the key**.

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Two Sum `⚡ T1` | Key = complement. The archetype. |
| 2 | Group Anagrams `⚡ T1` | Key = **canonical form** (sorted string / count tuple). |
| 3 | Subarray Sum Equals K `⚡ T1` | Key = **prefix sum**; count of `prefix - k` seen so far. The single most reusable trick in this repo. |
| 4 | Longest Consecutive Sequence `⚡ T1` | Set membership + "only start at sequence heads" — the key insight is *when not to start work*. |
| 5 | Contiguous Array / binary subarrays `⚡ T1` | Prefix-sum key with a **transform** (0 → -1). Recognize "equal counts of A and B" as prefix-sum-equals-zero. |

---

## Ladder 5 — BFS / DFS on grids & graphs

**Invariant:** BFS explores in rings ⇒ first arrival = shortest path **when all edges cost the same**. DFS explores exhaustively ⇒ use for reachability, components, and anything needing backtrack. The L4-level skill is spotting a graph where the problem gives you none: states are nodes, legal moves are edges.

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Number of Islands `⚡ T1` | Flood fill; visited-marking discipline. |
| 2 | Rotting Oranges `⚡ T1` | **Multi-source** BFS: seed the queue with all sources; level = time. |
| 3 | 01 Matrix / Walls and Gates `⚡ T1` | Invert the direction: BFS **from targets** to everything, not from each cell. |
| 4 | Word Ladder `⚡ T1` | **Implicit graph**: nodes = words, edges = one-letter change. Nobody hands you an adjacency list. |
| 5 | Snakes and Ladders `🎯 T2` | Implicit graph + an **encoding chore** (square → cell). The mapping is the problem. |
| 6 | Bus Routes `🎯 T2` | Choose the right **node type**: BFS over routes, not stops, because the answer counts buses. |
| 7 | Path With Minimum Effort `⚡ T1` | Edge weights differ ⇒ BFS breaks ⇒ **Dijkstra**. Understand exactly which invariant died. Bridge to Ladder 8. |

---

## Ladder 6 — Monotonic Stack

**Invariant:** scanning left→right, the stack holds "elements still waiting for their answer," kept sorted so that the current element **resolves** everyone it beats, in one pop-burst. O(n) because each element is pushed and popped once. Trigger: "next/previous greater/smaller" or "how far until…".

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Next Greater Element `🎯 T2` | The archetype: pop-and-resolve. |
| 2 | Daily Temperatures `🎯 T2` | Store **indices**; answer = distance, not value. |
| 3 | Car Fleet `🎯 T2` | The "elements" are cars sorted by position; the monotone quantity is arrival time. |
| 4 | Largest Rectangle in Histogram `🎯 T2` | Pop computes an **area** using prev-smaller as boundary. The classic hard rung. |
| 5 | Sum of Subarray Minimums `🎯 T2` | From "find" to **counting contribution**: `left[i] * right[i] * a[i]`. Strict/non-strict asymmetry for duplicates. |

---

## Ladder 7 — Heaps & Top-K

**Invariant:** you repeatedly need the current min/max of a *changing* collection — and nothing else. A heap gives that in O(log n) per op. Top-K trick: to keep the K largest, use a **min**-heap of size K (the root is the bouncer). If the collection never changes, just sort.

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Kth Largest Element in a Stream `⚡ T1` | Min-heap of size k. The bouncer idea. |
| 2 | K Closest Points / Top K Frequent `⚡ T1` | Same, keyed by a derived value. (Mention quickselect as the O(n) alternative.) |
| 3 | Merge K Sorted Lists `⚡ T1` | Heap as a **k-way frontier**: always extend the smallest head. |
| 4 | Task Scheduler / Reorganize String `⚡ T1` | **Greedy + heap**: always spend the most constrained resource first. Bridge to greedy. |
| 5 | Find Median from Data Stream `⚡ T1` | **Two heaps** balanced around the median. Composition of the invariant with itself. |
| 6 | Stock Price Fluctuation `🎯 T2` | Two heaps + **lazy deletion** (validate on pop). The L4 rung. |

---

## Ladder 8 — Shortest Path Beyond BFS

**Invariant:** Dijkstra = BFS where the queue becomes a min-heap keyed by distance, valid because with non-negative weights, the closest unvisited node's distance can never improve. Negative edges kill that proof → Bellman-Ford (relax all edges V-1 times).

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Network Delay Time `🎯 T2` | Textbook Dijkstra. Implement cold: heap of `(dist, node)`, skip stale pops. |
| 2 | Path With Minimum Effort `⚡ T1` | Dijkstra on a **grid**, and "distance" = max edge on path, not sum. The relax rule changes; the proof survives. |
| 3 | Swim in Rising Water `⚡ T1` | Same shape; distance = max cell value. (Also solvable by BS-on-answer + BFS — say both.) |
| 4 | Cheapest Flights Within K Stops `⚡ T1` | The **constraint (≤ k stops)** breaks Dijkstra's "final when popped" → Bellman-Ford with **k+1 rounds** (k stops = k+1 edges), relaxing from a copy of the previous round. |

---

## Ladder 9 — Recursion → Backtracking

**Invariant:** every backtracking problem is one template — `choose → recurse → unchoose` over a decision tree. The three design questions: (1) what is a *state*? (2) what are the *choices* at each state? (3) what *prunes* a branch early? Complexity = branching^depth; say it before coding.

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Subsets `🎯 T2` | The pure template: include/exclude each element. |
| 2 | Permutations `🎯 T2` | Choices shrink as you pick — `used` set. |
| 3 | Combination Sum `🎯 T2` | Reuse allowed → recurse with same index; dedup by never going backward. |
| 4 | Subsets II / Permutations II `🎯 T2` | **Duplicate input**: sort + "skip equal siblings at the same level." The rule to internalize, not memorize. |
| 5 | Word Search `⚡ T1` | Backtracking on a **grid** — unchoose = unmark cell. |
| 6 | Palindrome Partitioning `🎯 T2` | Choices = cut points; pruning via a validity check. |
| 7 | N-Queens `🎯 T2` | All three design questions get nontrivial answers (cols/diagonals sets = pruning). |

---

## Ladder 10 — Recursion → DP

**Invariant:** DP is *not* a new technique. It's Ladder 9's recursion where (a) subproblems **repeat** and (b) you only need the *value* of a subtree, not its members ⇒ cache it. Derivation order, always: brute recursion → identify state → memoize → (optionally) tabulate → (optionally) compress space. Never start at the table.

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Climbing Stairs `🎯 T2` | State = index. Watch recursion → memo → two variables happen. |
| 2 | House Robber `🎯 T2` | Add a **decision** to the state transition: rob or skip. |
| 3 | Coin Change `🎯 T2` | State = amount; answer = min over choices. First "unbounded" feel. |
| 4 | Longest Increasing Subsequence `⚡ T1` | State = "ending at i" — the first *non-obvious* state definition. (Mention the O(n log n) patience upgrade.) |
| 5 | Unique Paths → Minimum Path Sum `⚡ T1` | State becomes **2-D (grid)**; transitions from top/left only. |
| 6 | Longest Common Subsequence `🎯 T2` | 2-D over **two sequences** — the template behind edit distance and friends. |
| 7 | Edit Distance `🎯 T2` | LCS shape + three-way choice. If LCS is solid this is one delta. |
| 8 | Longest Increasing Path in a Matrix `⚡ T1` | DP on an **implicit DAG** (memoized DFS on a grid). Where Ladders 5 and 10 meet — the L4 capstone. |

**Failure drill:** for any DP you solve, state in one sentence what the state *means* in English. If you can't, you memorized the table.

---

## Ladder 11 — Intervals & Sweep

**Invariant:** two intervals overlap iff `start_A < end_B and start_B < end_A` (half-open; use `≤` if touching endpoints count — confirm with the interviewer). Learn this symmetric form; it kills off-by-one debates. Almost every interval problem = sort by one endpoint + one linear pass; "max simultaneous" problems = sweep line (sort event points, +1/−1).

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Merge Intervals `🎯 T2` | Sort by start; extend or emit. |
| 2 | Insert Interval `🎯 T2` | Input pre-sorted → three-phase pass, no sort. |
| 3 | Non-overlapping Intervals `🎯 T2` | Flip to **greedy**: sort by *end*, keep earliest-ending. Proof: earliest end leaves max room. |
| 4 | Meeting Rooms II `🎯 T2` | **Sweep line** debut: +1/−1 events, track running max. (Equivalent: min-heap of end times.) |
| 5 | Interval List Intersections `⚡ T1` | Two sorted lists + two pointers; intersection = `[max(starts), min(ends)]`. |
| 6 | My Calendar I → II `⚡ T1` → `🎯 T2` | The **online** version: intervals arrive one at a time. II = store overlaps separately. The L4 rung. |
| 7 | Employee Free Time `🎯 T2` | Merge k interval lists; the answer is the *gaps*. |

---

## Ladder 12 — Design-a-Data-Structure (L4 signature)

**Invariant:** every one of these is "support ops X, Y, Z, each in O(1) or O(log n)" — and no single structure does all of them. The move: **compose two structures so each covers the other's weak op**, then keep them in sync. Always draw the ops-vs-structure table first, out loud.

| # | Problem | What changed |
|---|---------|--------------|
| 1 | Min Stack `🎯 T2` | The archetype: second stack shadows the first with running mins. |
| 2 | Logger Rate Limiter → Hit Counter `💤 warm-up` → `⚡ T1` | Map / deque with time-based eviction. Follow-up: bounded memory via circular buffer. |
| 3 | Insert Delete GetRandom O(1) `⚡ T1` | Array (random) + map (locate); **swap-with-last** delete keeps both O(1). |
| 4 | LRU Cache `🎯 T2` | Map (locate) + **doubly linked list** (order). Sync on every touch. |
| 5 | LFU Cache `⚡ T1` | LRU + one more dimension: freq → DLL buckets + `min_freq`. Hardest sync in the family. |
| 6 | Snapshot Array / Stock Price Fluctuation `🎯 T2` | Add **time/versioning**: binary search over history, or heaps with lazy deletion. |
| 7 | Flatten Nested List Iterator `🎯 T2` | **Laziness** as the requirement: stack of iterators, work in `hasNext`. |

---

## After the ladders

- Breadth pass: topic indexes [`02-data-structures/README.md`](../02-data-structures/README.md), [`03-algorithms/README.md`](../03-algorithms/README.md) — everything there should now feel like "rung 2 of a ladder I know."
- Integration: [Mock rounds](03-interview-judgment.md#part-d--mock-rounds) timed, plus the follow-up drill table in [`00-start-here/03-l4-sde2-delta.md`](../00-start-here/03-l4-sde2-delta.md#4-l4-6-week-schedule).
- If a mock problem stumps you, the postmortem question is never "which problem was this like?" — it's "**which invariant did I fail to test for?**" Log it.

---

## See Also

- [How to think](../01-foundations/01-how-to-think.md) — the derivation behind each invariant
- [Pattern sheet](01-pattern-sheet.md) — trigger-phrase lookup
- [Interview judgment](03-interview-judgment.md) — mocks and senior follow-up chains
