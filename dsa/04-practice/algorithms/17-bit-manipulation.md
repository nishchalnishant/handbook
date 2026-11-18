---
tags: [coding, algorithms, bit-manipulation]
topic: Bit Manipulation
difficulty: mixed
---
# Bit Manipulation — Problem Deep Dives

## What this covers

> [!abstract] In this file
> **Covers:** Worked bit problems: XOR cancellation, popcount, bit DP, two's-complement tricks, bitmask enumeration, Gray code, per-bit case analysis, XOR trie.
> **You'll be able to:** Recognise the XOR / `n & (n-1)` / `n & -n` / mask-enumeration click moments and code each in under 5 minutes, including Python's infinite-width negative-int traps.
> **Prereqs:** Bit Manipulation lecture · **Pair with:** [Bit Manipulation lecture](../../02-algorithms/17-bit-manipulation.md) · **Time:** 2 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [XOR Cancellation & Single Occurrence](#xor-cancellation--single-occurrence) · [Counting & Testing Bits](#counting--testing-bits) · [Two's Complement, Masks & Arithmetic](#twos-complement-masks--arithmetic) · [Bitmask Enumeration & Construction](#bitmask-enumeration--construction) · [Per-Bit Case Analysis & XOR Trie](#per-bit-case-analysis--xor-trie)

> [!tip] If you only have 20 minutes
> **Do these first:** [Single Number](#single-number--t1) · [Number of 1 Bits](#number-of-1-bits--t1) · [Counting Bits](#counting-bits--t1) · [Missing Number](#missing-number--t1) · [Power of Two / Power of Four](#power-of-two--power-of-four--t1) · [Subsets via Bitmask Enumeration](#subsets-via-bitmask-enumeration--t1) · [Maximum XOR of Two Numbers in an Array](#maximum-xor-of-two-numbers-in-an-array--t1)
> **Template:** `n & (n-1)` clears the lowest set bit · `n & -n` isolates it · `x ^ x = 0`, `x ^ 0 = x` · subset `i` of `n` items = bits of `mask` in `range(1 << n)`.
> **Gotchas:** Python ints are unbounded — mask with `0xFFFFFFFF` whenever the problem is 32-bit (Reverse Bits, Sum of Two Integers) · `>>` on a negative int never reaches 0 (loops forever) · `n > 0` guard on power-of-two checks · precedence: `+`/`-` bind tighter than `<<`/`&` (`1 << n - 1` is `1 << (n-1)`), so parenthesize mixed expressions.
> **Lecture refs:** [XOR cancellation](../../02-algorithms/17-bit-manipulation.md#trick-1-xor-cancellation--find-the-single-number) · [Kernighan popcount](../../02-algorithms/17-bit-manipulation.md#trick-3-count-set-bits-hamming-weight--popcount) · [Two's complement / lowest set bit](../../02-algorithms/17-bit-manipulation.md#trick-5-twos-complement--lowest-set-bit) · [Subsets via bitmask](../../02-algorithms/17-bit-manipulation.md#trick-8-subsets-via-bitmask)

---

## XOR Cancellation & Single Occurrence

---

### Single Number `⚡ T1`

> [!example] Problem
> `nums` where every element appears exactly twice except one. Return the single one. O(n) time, O(1) extra space.
> Example: `[4,1,2,1,2]` → `4`.

> [!info] Approach
> **Key insight:** `a ^ a = 0`, `a ^ 0 = a`, XOR is commutative/associative, so pairs cancel regardless of order.
> XOR-fold the whole array; the survivor is the answer. See [lecture deep dive](../../02-algorithms/17-bit-manipulation.md#single-number--t1).

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
>
> def single_number(nums):
>     return reduce(xor, nums, 0)
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!warning] Edge Cases & Gotchas
> Works for negatives unchanged (Python XOR on infinite two's complement is consistent) · single-element array returns itself · fails if "twice" becomes "three times" → Single Number II.

> [!question] Follow-ups
> Elements appear 3x except one (next problem) · Two singles (Single Number III) · Hash set / sum trick `2*sum(set) - sum` is O(n) space — mention then reject.

---

### Single Number II `🎯 T2`

> [!example] Problem
> Every element appears three times except one which appears once. Return it with O(n) time, O(1) space.
> Example: `[0,1,0,1,0,1,99]` → `99`.

> [!info] Approach
> **Key insight:** per bit position, the count of 1s across all numbers is `3k` or `3k+1`; the answer's bit is `count % 3`.
> Two-register state machine `(twos, ones)` cycling `00 → 01 → 10 → 00` per bit: `ones` takes bit `x` only if `twos` isn't set; `twos` takes it only if `ones` isn't. After all numbers `ones` holds bits seen once (mod 3).
> General version (`k` copies): count bits in 32 slots, `% k`, rebuild — then fix sign for negatives (`if res >= 1<<31: res -= 1<<32`).

> [!note]- Python Solution
> ```python
> def single_number_ii(nums):
>     ones = twos = 0
>     for x in nums:
>         ones = (ones ^ x) & ~twos
>         twos = (twos ^ x) & ~ones
>     return ones
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!warning] Edge Cases & Gotchas
> The `ones/twos` form needs no sign fix in Python (ops are on infinite sign-extended ints) — verified with negatives · the 32-slot counting version DOES need the sign fix · order of the two updates matters: `ones` first using old `twos`, then `twos` using new `ones`.

> [!tip] Alternatives
> 32-slot per-bit counter: `for b in range(32): cnt = sum(x >> b & 1 for x in nums) % 3` — easier to derive on a whiteboard, O(32n).

> [!question] Follow-ups
> Every element appears `m` times except one that appears once (`% m`) · except one that appears `p` times with `p % m != 0`.

---

### Single Number III `🎯 T2`

> [!example] Problem
> Exactly two elements appear once, all others twice. Return both (any order). O(n) time, O(1) space.
> Example: `[1,2,1,3,2,5]` → `[3,5]`.

> [!info] Approach
> **Key insight:** XOR of all = `a ^ b` (nonzero since `a != b`). Any set bit of `a ^ b` is a bit where `a` and `b` differ, so it partitions the array into two groups each containing exactly one of them (pairs stay together).
> 1. `t = XOR(all)`. 2. `low = t & -t` (lowest set bit). 3. XOR only elements with `x & low` → `a`. 4. `b = t ^ a`.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
>
> def single_number_iii(nums):
>     t = reduce(xor, nums, 0)
>     low = t & -t
>     a = 0
>     for x in nums:
>         if x & low:
>             a ^= x
>     return [a, t ^ a]
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!warning] Edge Cases & Gotchas
> `t & -t` is safe for negative `t` in Python · do not use `t & (t-1)` (that clears the bit, wrong tool) · any set bit works, lowest is just the cheapest to get · output order is arbitrary.

> [!question] Follow-ups
> What if `a` could equal `b`? (then `t == 0`; problem is ill-posed) · Three singles → no clean O(1) bit trick.

---

### Missing Number `⚡ T1`

> [!example] Problem
> `nums` has `n` distinct values in `[0, n]`. Return the one missing. O(n) time, O(1) space.
> Example: `[3,0,1]` → `2`.

> [!info] Approach
> **Key insight:** XOR the full range `0..n` against the array — every present value cancels, the missing one survives. Seed with `n` and XOR `i ^ nums[i]` in one loop.
> Alternative: Gauss `n(n+1)/2 - sum(nums)` (no overflow in Python).

> [!note]- Python Solution
> ```python
> def missing_number(nums):
>     x = len(nums)
>     for i, v in enumerate(nums):
>         x ^= i ^ v
>     return x
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!warning] Edge Cases & Gotchas
> Seed with `len(nums)` — the range has `n+1` values but only `n` indices · `[0]` → `1`, `[1]` → `0`.

> [!tip] Alternatives
> Sum formula (shortest) · cyclic sort / index-as-hash (LC 41 family) · binary search on sorted input.

> [!question] Follow-ups
> Two numbers missing (XOR + partition, like Single Number III) · Array not 0-based range (First Missing Positive).

---

## Counting & Testing Bits

---

### Number of 1 Bits `⚡ T1`

> [!example] Problem
> Return the number of `1` bits in the binary representation of non-negative `n`.
> Example: `11` (`1011`) → `3`.

> [!info] Approach
> **Key insight (Kernighan):** `n &= n - 1` clears the lowest set bit, so the loop runs exactly `popcount(n)` times, not 32. See [lecture](../../02-algorithms/17-bit-manipulation.md#number-of-1-bits-hamming-weight--t1).

> [!note]- Python Solution
> ```python
> def hamming_weight(n):
>     c = 0
>     while n:
>         n &= n - 1
>         c += 1
>     return c
> ```

> [!success] Complexity
> Time O(popcount) ≤ O(32), Space O(1).

> [!warning] Edge Cases & Gotchas
> Only terminates for `n >= 0` — a negative Python int never reaches 0 under `&= n-1`; mask first (`n & 0xFFFFFFFF`) if negatives are possible · `n = 0` → `0`.

> [!tip] Alternatives
> `bin(n).count("1")` · `n.bit_count()` (3.10+) · shift-and-test loop (32 iterations, works with mask).

> [!question] Follow-ups
> Hamming distance of two ints → `popcount(a ^ b)` · Total Hamming distance → per-bit `ones * zeros`.

---

### Counting Bits `⚡ T1`

> [!example] Problem
> Return `ans[0..n]` where `ans[i]` is the number of 1 bits in `i`. Do it in O(n), not O(n log n).
> Example: `n = 5` → `[0,1,1,2,1,2]`.

> [!info] Approach
> **Key insight:** `i` = (`i >> 1`) plus its last bit, and `i >> 1 < i` is already computed: `dp[i] = dp[i >> 1] + (i & 1)`.
> Equivalent: `dp[i] = dp[i & (i-1)] + 1` (drop lowest set bit).

> [!note]- Python Solution
> ```python
> def count_bits(n):
>     dp = [0] * (n + 1)
>     for i in range(1, n + 1):
>         dp[i] = dp[i >> 1] + (i & 1)
>     return dp
> ```

> [!success] Complexity
> Time O(n), Space O(n) (output).

> [!warning] Edge Cases & Gotchas
> `n = 0` → `[0]` · allocate `n + 1` slots · the `i & (i-1)` form is the same idea via Kernighan.

> [!question] Follow-ups
> Sum of popcounts for 1..n in O(log n) (per-bit period counting) · Hamming distance variants.

---

### Power of Two / Power of Four `⚡ T1`

> [!example] Problem
> Return whether `n` is `2^k` (Power of Two) or `4^k` (Power of Four), for integer `n` (may be ≤ 0).

> [!info] Approach
> **Key insight:** a power of two has exactly one set bit → `n > 0 and n & (n-1) == 0`. Power of four additionally has that bit at an even index → AND with `0x55555555` (`0101...01`) is non-zero. See [lecture](../../02-algorithms/17-bit-manipulation.md#trick-2-power-of-two-check).
> Alternatives for four: `n % 3 == 1` (since `4^k ≡ 1 mod 3`, while `2·4^k ≡ 2`).

> [!note]- Python Solution
> ```python
> def is_power_of_two(n):
>     return n > 0 and n & (n - 1) == 0
>
> def is_power_of_four(n):
>     return n > 0 and n & (n - 1) == 0 and n & 0x55555555 != 0
> ```

> [!success] Complexity
> Time O(1), Space O(1).

> [!warning] Edge Cases & Gotchas
> `n > 0` guard is mandatory: `0 & -1 == 0` and negatives would pass otherwise · `1` is `2^0` and `4^0` → True · `0x55555555` covers bit positions 0..30, enough for 32-bit signed input.

> [!question] Follow-ups
> Power of Three without loops → `3^19 % n == 0` for `n > 0` · Next power of two ≥ n → `1 << (n-1).bit_length()`.

---

### Reverse Bits `🎯 T2`

> [!example] Problem
> Reverse the bits of a 32-bit unsigned integer.
> Example: `43261596` (`00000010100101000001111010011100`) → `964176192`.

> [!info] Approach
> **Key insight:** pop the LSB of `n`, push it onto the LSB of `r` after shifting `r` left; do exactly 32 iterations (not `while n`) so leading zeros of `n` become trailing zeros of the result. See [lecture](../../02-algorithms/17-bit-manipulation.md#reverse-bits--t2).

> [!note]- Python Solution
> ```python
> def reverse_bits(n):
>     r = 0
>     for _ in range(32):
>         r = (r << 1) | (n & 1)
>         n >>= 1
>     return r
> ```

> [!success] Complexity
> Time O(32) = O(1), Space O(1).

> [!warning] Edge Cases & Gotchas
> Loop a fixed 32 times — `while n` drops leading zeros and gives the wrong answer for small `n` (e.g. `1` must become `2^31`) · input assumed non-negative (pass `n & 0xFFFFFFFF` if given signed).

> [!tip] Alternatives
> `int(f"{n:032b}"[::-1], 2)` · divide-and-conquer swap (16/8/4/2/1-bit halves with masks) for the follow-up.

> [!question] Follow-ups
> Called many times → cache by byte (256-entry table, reverse 4 bytes and swap) · Reverse bits of a 64-bit value.

---

## Two's Complement, Masks & Arithmetic

---

### Sum of Two Integers `🎯 T2`

> [!example] Problem
> Return `a + b` without using `+` or `-`. Inputs in `[-1000, 1000]`.
> Example: `a=-2, b=3` → `1`.

> [!info] Approach
> **Key insight:** `a ^ b` is the sum ignoring carries; `(a & b) << 1` is the carries. Repeat until carry is 0.
> **Python trap:** ints have infinite sign extension, so a negative carry would shift forever. Mask both values to 32 bits each iteration, and at the end reinterpret: if result `> 0x7FFFFFFF` it is a negative 32-bit number → `~(a ^ MASK)` (flip upper bits back to ones). See [lecture](../../02-algorithms/17-bit-manipulation.md#sum-of-two-integers--t2).

> [!note]- Python Solution
> ```python
> def get_sum(a, b):
>     MASK, MAXI = 0xFFFFFFFF, 0x7FFFFFFF
>     while b:
>         a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
>     return a if a <= MAXI else ~(a ^ MASK)
> ```

> [!success] Complexity
> Time O(32) = O(1), Space O(1).

> [!warning] Edge Cases & Gotchas
> Mask the XOR too, not just the carry · `get_sum(-1, 1) == 0` and `get_sum(-5, 3) == -2` are the sanity checks · `~(a ^ MASK)` is equivalent to `a - 2**32`.

> [!question] Follow-ups
> Subtract without `-` (add `~b + 1`) · Multiply without `*` (shift-add) · Why 32-bit (C++/Java ints wrap natively; Python does not).

---

### Bitwise AND of Numbers Range `🎯 T2`

> [!example] Problem
> Return the bitwise AND of all integers in `[left, right]`.
> Example: `[5, 7]` → `4`.

> [!info] Approach
> **Key insight:** as the range sweeps from `left` to `right`, every bit below the highest differing bit takes both 0 and 1 and so ANDs to 0. The result is the **common binary prefix** of `left` and `right`, padded with zeros.
> Shift both right until equal, counting shifts; shift the prefix back. See [lecture](../../02-algorithms/17-bit-manipulation.md#bitwise-and-of-numbers-range--t2).

> [!note]- Python Solution
> ```python
> def range_bitwise_and(left, right):
>     shift = 0
>     while left != right:
>         left >>= 1; right >>= 1; shift += 1
>     return left << shift
> ```

> [!success] Complexity
> Time O(log right), Space O(1).

> [!warning] Edge Cases & Gotchas
> `left == right` → returns itself · `left = 0` → 0 · alt loop: `while right > left: right &= right - 1` (clear lowest bit of `right` until it drops to ≤ `left`).

> [!tip] Alternatives
> Kernighan form: `while right > left: right &= right - 1; return right`.

---

## Bitmask Enumeration & Construction

---

### Subsets via Bitmask Enumeration `⚡ T1`

> [!example] Problem
> Given distinct `nums`, return all subsets (the power set), e.g. LC 78.
> Example: `[1,2,3]` → 8 subsets including `[]` and `[1,2,3]`.

> [!info] Approach
> **Key insight:** each mask in `range(1 << n)` is one subset; bit `i` set ⇔ `nums[i]` included. Gives a bijection with no recursion. See [lecture](../../02-algorithms/17-bit-manipulation.md#trick-8-subsets-via-bitmask).
> Sub-mask enumeration of a mask `m` (all subsets of its set bits): `s = m; while s: ...; s = (s-1) & m` — sums to `3^n` over all masks, the basis of bitmask DP.

> [!note]- Python Solution
> ```python
> def subsets(nums):
>     n = len(nums)
>     return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]
> ```

> [!success] Complexity
> Time O(n · 2^n), Space O(n · 2^n) for output.

> [!warning] Edge Cases & Gotchas
> Empty input → `[[]]` · only valid for `n` up to ~20 · duplicates (Subsets II) → sort first and dedupe, bitmask gets awkward — use backtracking · order differs from DFS order; most checkers accept any order.

> [!tip] Alternatives
> Backtracking/include-exclude (see [Backtracking](../../02-algorithms/12-backtracking.md)) — preferred when pruning is possible.

> [!question] Follow-ups
> Bitmask DP: TSP, assign tasks, partition into k equal sums, `dp[mask]` with `mask & -mask` to peel the lowest element · Subsets of size k via `mask.bit_count() == k`.

---

### Gray Code `💤 T3`

> [!example] Problem
> Return any valid n-bit Gray code sequence starting at 0: `2^n` integers, each in `[0, 2^n)`, distinct, consecutive (and first/last) differ in exactly one bit.
> Example: `n = 2` → `[0,1,3,2]`.

> [!info] Approach
> **Key insight (closed form):** `gray(i) = i ^ (i >> 1)`. Incrementing `i` flips a trailing run of bits; XOR with the shifted copy turns that into exactly one flip.
> Reflect-and-prefix construction: `G(n) = G(n-1) + [x | 1<<(n-1) for x in reversed(G(n-1))]` — same sequence.
> Inverse (Gray → binary): `b = g; while g := g >> 1: b ^= g`.

> [!note]- Python Solution
> ```python
> def gray_code(n):
>     return [i ^ (i >> 1) for i in range(1 << n)]
> ```

> [!success] Complexity
> Time O(2^n), Space O(2^n) for output.

> [!warning] Edge Cases & Gotchas
> `n = 0` → `[0]` · first and last also differ by one bit (cyclic) — asserted · skip at L3 unless you finish the T1/T2 set; the formula is cheap to memorize.

> [!question] Follow-ups
> Circular permutation in binary representation (LC 1238): rotate Gray code so it starts at `start`.

---

## Per-Bit Case Analysis & XOR Trie

---

### Minimum Flips to Make a OR b Equal to c `🎯 T2`

> [!example] Problem
> Given positive ints `a, b, c`, return the minimum number of single-bit flips in `a` and/or `b` so that `a | b == c`.
> Example: `a=2, b=6, c=5` → `3`.

> [!info] Approach
> **Key insight:** bits are independent — handle each of 32 positions.
> - `c` bit = 1: need `x | y = 1`; cost `1` only if both are 0.
> - `c` bit = 0: need `x = y = 0`; cost `x + y` (flip each that is 1).
> Sum the costs.

> [!note]- Python Solution
> ```python
> def min_flips(a, b, c):
>     flips = 0
>     for i in range(32):
>         x, y, z = a >> i & 1, b >> i & 1, c >> i & 1
>         if z:
>             flips += (x | y) == 0
>         else:
>             flips += x + y
>     return flips
> ```

> [!success] Complexity
> Time O(32), Space O(1).

> [!warning] Edge Cases & Gotchas
> `c` bit 0 with both `a`, `b` bits 1 costs **2**, not 1 · loop to 32 (or `max(a,b,c).bit_length()`) so high bits of `a`/`b` beyond `c` are counted · `(a|b)==c` already → 0.

> [!tip] Alternatives
> Single expression: `((a | b) ^ c).bit_count() + (a & b & ~c).bit_count()` — XOR counts mismatches, the second term adds the extra flip when both are 1 and `c` is 0.

---

### Maximum XOR of Two Numbers in an Array `⚡ T1`

> [!example] Problem
> Given `nums`, return the maximum `nums[i] ^ nums[j]`.
> Example: `[3,10,5,25,2,8]` → `28` (`5 ^ 25`).

> [!info] Approach
> Full bitwise-trie walkthrough lives in [Trie practice](../data-structures/09-trie.md#maximum-xor-of-two-numbers-in-an-array--t1) (insert bits 31→0, greedily take the opposite bit). Don't duplicate it — know the trie version cold.
> Trie-free variant (shown): build the answer one bit at a time from the MSB. At each bit, take the set of all prefixes; candidate = `ans | 1`; it is achievable iff some prefix `p` has `candidate ^ p` also in the set (since `a ^ b = cand` ⇔ `a ^ cand = b`).

> [!note]- Python Solution
> ```python
> def find_maximum_xor(nums):
>     ans = 0
>     for bit in range(max(nums).bit_length() - 1, -1, -1):
>         ans <<= 1
>         prefixes = {x >> bit for x in nums}
>         if any((ans | 1) ^ p in prefixes for p in prefixes):
>             ans |= 1
>     return ans
> ```

> [!success] Complexity
> Time O(32 · n), Space O(n) (prefix set) — trie is O(32 · n) time, O(32 · n) space.

> [!warning] Edge Cases & Gotchas
> `[0]` and `[5,5]` → `0` · loop from `max(nums).bit_length() - 1`, not a hardcoded 31, for speed · negatives not in the original constraints.

> [!question] Follow-ups
> Max XOR with an element ≤ limit per query (offline sort + trie) · Count pairs with XOR < k (trie with subtree counts).

---

## See Also

- [Bit Manipulation lecture](../../02-algorithms/17-bit-manipulation.md) — tricks reference and quick revision triggers
- [Trie practice — XOR Trie](../data-structures/09-trie.md#xor-trie) — bitwise trie for maximum XOR
- [Union-Find practice](14-union-find.md) — bitmask/DSU often paired in graph problems
- [Math & Number Theory practice](18-math-and-number-theory.md) — Reverse Integer, GCD, modular arithmetic
- [Dynamic Programming](../../02-algorithms/15-dynamic-programming.md) — bitmask DP (TSP, assignment)
- [Backtracking](../../02-algorithms/12-backtracking.md) — recursive subset enumeration

---

## Flashcards

**What are the three XOR identities that solve most 'find the odd one out' problems?** #flashcard
`a ^ a = 0`, `a ^ 0 = a`, XOR is commutative and associative. XOR-folding an array cancels every value that appears an even number of times.

**How do you find the two singletons when every other element appears twice?** #flashcard
XOR all → `t = a ^ b`. Take `low = t & -t` (any set bit where a and b differ). XOR only the elements with that bit set → `a`; `b = t ^ a`. O(n) time, O(1) space.

**What does `n & (n - 1)` do and what are its two uses?** #flashcard
Clears the lowest set bit. (1) `n > 0 and n & (n-1) == 0` tests power of two. (2) Loop `n &= n-1` counts set bits in exactly popcount(n) iterations (Kernighan).

**What does `n & -n` return?** #flashcard
The lowest set bit isolated (e.g. `12 & -12 = 4`). Works because `-n = ~n + 1` flips everything above the lowest 1. Used to split groups in Single Number III and in Fenwick trees.

**How do you add two ints without `+` in Python, and what is the Python-specific trap?** #flashcard
Loop: `a, b = a ^ b, (a & b) << 1` until `b == 0`. Python ints are infinite-width so negative carries never vanish — mask each step with `0xFFFFFFFF`, then if the result > `0x7FFFFFFF` return `~(a ^ 0xFFFFFFFF)`.

**Bitwise AND of all numbers in [left, right] — what is the answer structurally?** #flashcard
The common binary prefix of `left` and `right`, followed by zeros. Shift both right until equal (count shifts), then shift back. O(log n).

**What is the closed form for the i-th Gray code, and why does it work?** #flashcard
`i ^ (i >> 1)`. Incrementing `i` flips a trailing run of bits; XOR with the right-shifted copy cancels all but one of those flips, so neighbours differ in exactly one bit.

**How do you enumerate all subsets (and all sub-masks of a mask)?** #flashcard
All subsets of n items: `for mask in range(1 << n)`, bit i set ⇔ item i included. All sub-masks of `m`: `s = m; while s: use(s); s = (s-1) & m` (then handle empty). Total over all masks is 3^n.

**Why must Reverse Bits loop exactly 32 times rather than `while n`?** #flashcard
Leading zeros of `n` must become trailing zeros of the result. `while n` stops early and loses them (e.g. input 1 must give 2^31).

**In Min Flips to Make a OR b == c, what is the per-bit cost rule?** #flashcard
If c-bit = 1: cost 1 iff both a-bit and b-bit are 0. If c-bit = 0: cost = a-bit + b-bit (each 1 must be flipped, so both set costs 2).
