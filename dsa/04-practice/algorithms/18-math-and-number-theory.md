---
tags: [coding, algorithms, math, number-theory]
topic: Math & Number Theory
difficulty: mixed
---
# Math & Number Theory — Problem Deep Dives

## What this covers

> [!abstract] In this file
> **Covers:** Worked math problems: digit/string arithmetic, sieve, fast exponentiation, modular inverse and nCr, GCD and recurring decimals, rectangle geometry, designs with math, rejection sampling, slope hashing, integer sqrt.
> **You'll be able to:** Do digit-by-digit arithmetic without big ints, write square-and-halve exponentiation and a sieve from memory, and pick the right overflow/normalization trick (gcd, sign, mod) per problem.
> **Prereqs:** Math & Number Theory lecture · **Pair with:** [Math & Number Theory lecture](../../02-algorithms/18-math-and-number-theory.md) · **Time:** 2.5 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [Digits, Strings & Base Conversion](#digits-strings--base-conversion) · [Primes & Factors](#primes--factors) · [GCD, LCM & Fractions](#gcd-lcm--fractions) · [Fast Exponentiation & Modular Arithmetic](#fast-exponentiation--modular-arithmetic) · [Geometry & Designs With Math](#geometry--designs-with-math) · [Random Sampling](#random-sampling) · [Integer Square Root](#integer-square-root)

> [!tip] If you only have 20 minutes
> **Do these first:** [Plus One](#plus-one--t1) · [Add Binary](#add-binary--t1) · [Pow(x, n)](#powx-n--t1) · [Multiply Strings](#multiply-strings--t1) · [Detect Squares](#detect-squares--t1)
> **Template:** fast power `while n: if n & 1: r *= x; x *= x; n >>= 1` · sieve inner loop starts at `i*i` · `gcd(a, b)` is `math.gcd`; `lcm = a // g * b` · modular inverse of `b` mod prime `p` is `pow(b, p-2, p)` (or `pow(b, -1, p)` on 3.8+).
> **Gotchas:** Python never overflows, so "32-bit" checks are explicit and post-hoc · `int / int` is float — use `//` and `divmod` · normalize (sign, gcd) before using a pair as a dict key · base-26 Excel titles are **bijective** (no zero digit) → subtract 1 before each `% 26`.
> **Lecture refs:** [Digit tricks](../../02-algorithms/18-math-and-number-theory.md#1-integer--digit-tricks) · [GCD/LCM](../../02-algorithms/18-math-and-number-theory.md#3-gcd-lcm-and-euclidean-algorithm) · [Sieve](../../02-algorithms/18-math-and-number-theory.md#4-prime-testing--sieve) · [Fast power](../../02-algorithms/18-math-and-number-theory.md#5-fast-power-modular-exponentiation) · [Modular arithmetic](../../02-algorithms/18-math-and-number-theory.md#6-modular-arithmetic) · [Overflow in Python](../../02-algorithms/18-math-and-number-theory.md#9-overflow--edge-cases-in-python)

---

## Digits, Strings & Base Conversion

---

### Reverse Integer `🎯 T2`

> [!example] Problem
> Reverse the digits of a signed 32-bit integer `x`. If the result is outside `[-2^31, 2^31 - 1]` return `0`.
> Example: `-123` → `-321`; `1534236469` → `0`.

> [!info] Approach
> **Key insight:** peel digits with `x % 10` / `x // 10` on `abs(x)`; before appending digit `d`, detect overflow: `r > MAX//10` or (`r == MAX//10` and `d` exceeds the last digit of the bound — 7 for positive, 8 for negative). Re-apply sign at the end.
> Python shortcut: reverse freely (no overflow), then range-check once at the end. Interviewers want the pre-check to show you understand fixed-width ints. See [lecture](../../02-algorithms/18-math-and-number-theory.md#1-integer--digit-tricks).

> [!note]- Python Solution
> ```python
> def reverse_int_nobig(x):
>     INT_MAX = 2**31 - 1
>     sign = -1 if x < 0 else 1
>     x = abs(x)
>     r = 0
>     while x:
>         d = x % 10
>         x //= 10
>         if r > INT_MAX // 10 or (r == INT_MAX // 10 and d > (7 if sign > 0 else 8)):
>             return 0
>         r = r * 10 + d
>     return sign * r
> ```

> [!success] Complexity
> Time O(log |x|) (digits), Space O(1).

> [!warning] Edge Cases & Gotchas
> Use `abs` + explicit sign — `%` and `//` on negatives floor toward -inf in Python (`-123 % 10 == 7`) · `-2^31` itself reverses to a value > bound → `0` · trailing zeros vanish (`120` → `21`) · `0` → `0`.

> [!tip] Alternatives
> String: `int(str(abs(x))[::-1])` then sign and range check.

---

### Plus One `⚡ T1`

> [!example] Problem
> `digits` is a big-endian decimal number with no leading zeros. Return `digits + 1` as a digit array.
> Example: `[9,9]` → `[1,0,0]`.

> [!info] Approach
> **Key insight:** scan from the right. A digit `< 9` just increments and you are done. A `9` becomes `0` and the carry continues. If the loop finishes, every digit was 9 → prepend `1`.

> [!note]- Python Solution
> ```python
> def plus_one(digits):
>     for i in range(len(digits) - 1, -1, -1):
>         if digits[i] < 9:
>             digits[i] += 1
>             return digits
>         digits[i] = 0
>     return [1] + digits
> ```

> [!success] Complexity
> Time O(n), Space O(1) (O(n) only in the all-9s case).

> [!warning] Edge Cases & Gotchas
> All 9s is the only case that changes length · `[0]` → `[1]` · early return on first non-9 avoids touching the rest · mutating input is fine in LC; copy if asked not to.

> [!question] Follow-ups
> Add two digit arrays (Add Two Numbers pattern) · Plus One on a linked list (stack or recursion).

---

### Multiply Strings `⚡ T1`

> [!example] Problem
> Given non-negative integers `num1`, `num2` as strings, return their product as a string. No `int()` on whole strings, no BigInteger.
> Example: `"123" × "456"` → `"56088"`.

> [!info] Approach
> **Key insight:** digit `a[i] * b[j]` lands in result positions `i + j` (carry) and `i + j + 1` (units). Allocate `len(a) + len(b)` slots, iterate both strings from the right, add into `res[i+j+1]`, push `s // 10` to `res[i+j]`. Strip leading zeros at the end.

> [!note]- Python Solution
> ```python
> def multiply(a, b):
>     if a == "0" or b == "0":
>         return "0"
>     res = [0] * (len(a) + len(b))
>     for i in range(len(a) - 1, -1, -1):
>         for j in range(len(b) - 1, -1, -1):
>             s = int(a[i]) * int(b[j]) + res[i + j + 1]
>             res[i + j + 1] = s % 10
>             res[i + j] += s // 10
>     return "".join(map(str, res)).lstrip("0")
> ```

> [!success] Complexity
> Time O(m · n), Space O(m + n).

> [!warning] Edge Cases & Gotchas
> Early return `"0"` if either is `"0"` (else you return `"000"` stripped to `""`) · `lstrip("0")` is safe after the zero check · result length is `m + n` or `m + n - 1` · carry in `res[i+j]` may exceed 9 temporarily; it is normalized when that cell is processed as `i+j+1` of the next outer step (verified on `999 × 999`).

> [!question] Follow-ups
> Karatsuba for O(n^1.58) · Add Strings / Add Binary / Add Two Numbers as the carry primitives.

---

### Add Binary `⚡ T1`

> [!example] Problem
> Given binary strings `a` and `b`, return their sum as a binary string.
> Example: `"1010" + "1011"` → `"10101"`.

> [!info] Approach
> **Key insight:** two pointers from the right plus a carry; loop `while i >= 0 or j >= 0 or carry`. Digit `s = carry + a_i + b_j`; output bit `s & 1`, new carry `s >> 1`. Reverse at the end.

> [!note]- Python Solution
> ```python
> def add_binary(a, b):
>     i, j, carry, out = len(a) - 1, len(b) - 1, 0, []
>     while i >= 0 or j >= 0 or carry:
>         s = carry
>         if i >= 0: s += int(a[i]); i -= 1
>         if j >= 0: s += int(b[j]); j -= 1
>         out.append(str(s & 1))
>         carry = s >> 1
>     return "".join(reversed(out))
> ```

> [!success] Complexity
> Time O(max(m, n)), Space O(max(m, n)).

> [!warning] Edge Cases & Gotchas
> The `or carry` in the loop condition handles the final extra digit · different lengths · `"0" + "0"` → `"0"` · same skeleton works for Add Strings (base 10) and any base.

> [!tip] Alternatives
> `bin(int(a, 2) + int(b, 2))[2:]` — one line; say it, then write the loop if asked to avoid big ints.

> [!question] Follow-ups
> Add K-base numbers · Subtract binary strings · Add two linked-list numbers.

---

### Excel Sheet Column Number and Title `🎯 T2`

> [!example] Problem
> `titleToNumber("AB")` → `28`; `convertToTitle(701)` → `"ZY"`.

> [!info] Approach
> **Number:** Horner in base 26 with digits `A=1..Z=26`: `r = r * 26 + (ord(c) - 64)`.
> **Title:** bijective base-26 has no zero digit, so shift to 0-based each step: `n -= 1; digit = n % 26; n //= 26`, then reverse.

> [!note]- Python Solution
> ```python
> def title_to_number(s):
>     r = 0
>     for c in s:
>         r = r * 26 + ord(c) - 64
>     return r
>
> def number_to_title(n):
>     out = []
>     while n:
>         n -= 1
>         out.append(chr(65 + n % 26))
>         n //= 26
>     return "".join(reversed(out))
> ```

> [!success] Complexity
> Time O(len) / O(log₂₆ n), Space O(1) / O(log n).

> [!warning] Edge Cases & Gotchas
> Forgetting `n -= 1` yields `"@"` for multiples of 26 (26 must be `"Z"`, 52 `"AZ"`) · `FXSHRXW` = 2147483647 is the max-int check · round-trip property `title(number(t)) == t` is a good self-test.

> [!question] Follow-ups
> Convert to any bijective base · Excel column letters to 0-based index for spreadsheet design.

---

## Primes & Factors

---

### Count Primes `🎯 T2`

> [!example] Problem
> Return the number of primes strictly less than `n` (`0 <= n <= 5·10^6`).
> Example: `n = 10` → `4` (2, 3, 5, 7).

> [!info] Approach
> **Key insight:** for each prime `i ≤ √n`, every multiple below `i*i` was already crossed out by a smaller prime, so start at `i*i` and step by `i`. Use a `bytearray` and slice assignment so the inner loop is C-speed. See [lecture](../../02-algorithms/18-math-and-number-theory.md#4-prime-testing--sieve).

> [!note]- Python Solution
> ```python
> def count_primes(n):
>     if n < 3:
>         return 0
>     sieve = bytearray([1]) * n
>     sieve[0] = sieve[1] = 0
>     for i in range(2, int(n ** 0.5) + 1):
>         if sieve[i]:
>             sieve[i*i::i] = bytearray(len(range(i*i, n, i)))
>     return sum(sieve)
> ```

> [!success] Complexity
> Time O(n log log n), Space O(n).

> [!warning] Edge Cases & Gotchas
> "Strictly less than" → array size `n`, not `n + 1` · `n < 3` → 0 · mark 0 and 1 non-prime · `bytearray(len(range(i*i, n, i)))` gets the slice length right · `count_primes(100) == 25`.

> [!tip] Alternatives
> Single `is_prime(n)` by trial division up to `√n` (O(√n)) for one query; segmented sieve for a range `[L, R]` with large `R`; linear sieve for smallest-prime-factor tables.

> [!question] Follow-ups
> Smallest prime factor table → factorize in O(log n) · Prime Factors / Largest Component Size by Common Factor (DSU on primes).

---

### Factorial Trailing Zeroes `🎯 T2`

> [!example] Problem
> Return the number of trailing zeroes in `n!`.
> Example: `n = 25` → `6`.

> [!info] Approach
> **Key insight:** each zero needs a factor 10 = 2·5; factors of 2 are abundant, so count factors of 5 in `1..n`: `n//5 + n//25 + n//125 + ...` (multiples of 25 contribute a second 5, etc.). Loop `n //= 5; c += n`.

> [!note]- Python Solution
> ```python
> def trailing_zeroes(n):
>     c = 0
>     while n:
>         n //= 5
>         c += n
>     return c
> ```

> [!success] Complexity
> Time O(log₅ n), Space O(1).

> [!warning] Edge Cases & Gotchas
> Do not compute `n!` — it is huge · `n = 0` → 0 · `25 → 6`, `100 → 24` (not 20 — the 25s and 100s count extra).

> [!question] Follow-ups
> Smallest n with exactly k trailing zeros (binary search on this function; answer is 5 or 0 values) · Trailing zeros in base b (min over prime factors of b).

---

## GCD, LCM & Fractions

---

### Fraction to Recurring Decimal (with GCD/LCM) `🎯 T2`

> [!example] Problem
> Given `numerator`, `denominator`, return the fraction as a string; wrap a repeating part in parentheses.
> Examples: `1/2` → `"0.5"`; `4/333` → `"0.(012)"`; `1/6` → `"0.1(6)"`.
> **GCD/LCM toolkit:** `gcd(a,b)` via Euclid (`while b: a, b = b, a % b`), `lcm(a,b) = a // gcd(a,b) * b` (divide first to keep numbers small).

> [!info] Approach
> **Key insight:** long division; the state after each step is the **remainder**. If a remainder repeats, the digits between its first occurrence and now repeat forever (at most `den - 1` distinct remainders, so termination is guaranteed).
> Store `remainder → index in output list`; on repeat, insert `"("` at that index and append `")"`. Handle sign separately and work with absolute values. See [lecture GCD](../../02-algorithms/18-math-and-number-theory.md#3-gcd-lcm-and-euclidean-algorithm).

> [!note]- Python Solution
> ```python
> from math import gcd
>
> def lcm(a, b):
>     return a // gcd(a, b) * b
>
> def fraction_to_decimal(num, den):
>     if num == 0:
>         return "0"
>     sign = "-" if (num < 0) != (den < 0) else ""
>     num, den = abs(num), abs(den)
>     q, rem = divmod(num, den)
>     out = [sign, str(q)]
>     if rem == 0:
>         return "".join(out)
>     out.append(".")
>     seen = {}
>     while rem:
>         if rem in seen:
>             out.insert(seen[rem], "(")
>             out.append(")")
>             break
>         seen[rem] = len(out)
>         rem *= 10
>         d, rem = divmod(rem, den)
>         out.append(str(d))
>     return "".join(out)
> ```

> [!success] Complexity
> Time O(den) worst case (length of output), Space O(den).

> [!warning] Edge Cases & Gotchas
> Sign = XOR of signs; `0 / -5` → `"0"` (no `-0`) · integer-valued results have no `.` · record the index **before** appending the digit · `-1 / -2147483648` produces a 31-digit terminating decimal (tested) · no gcd reduction is needed for correctness, only for pretty `a/b` output.

> [!question] Follow-ups
> Add two fractions (lcm of denominators, reduce by gcd) · Count distinct rational values · LC 1071 GCD of Strings (`s+t == t+s`).

---

## Fast Exponentiation & Modular Arithmetic

---

### Pow(x, n) `⚡ T1`

> [!example] Problem
> Implement `pow(x, n)` for float `x` and integer `n` (may be negative, up to `-2^31`).
> Example: `2.0^10` → `1024.0`; `2.0^-2` → `0.25`.

> [!info] Approach
> **Key insight:** write `n` in binary; `x^n` is the product of `x^(2^k)` for each set bit `k`. Iterate: if low bit set, `res *= x`; always `x *= x`; `n >>= 1`. For negative `n` invert `x` and negate `n` first. See [lecture](../../02-algorithms/18-math-and-number-theory.md#5-fast-power-modular-exponentiation).

> [!note]- Python Solution
> ```python
> def my_pow(x, n):
>     if n < 0:
>         x, n = 1 / x, -n
>     res = 1.0
>     while n:
>         if n & 1:
>             res *= x
>         x *= x
>         n >>= 1
>     return res
> ```

> [!success] Complexity
> Time O(log |n|), Space O(1).

> [!warning] Edge Cases & Gotchas
> Negating `n = -2^31` is safe in Python (unbounded) but overflows in C/Java — use `long` there · `x = 0` with `n < 0` → division by zero (LC says it will not occur) · `n = 0` → `1.0` · iterative beats recursive (no stack).

> [!question] Follow-ups
> Recursive form `half = pow(x, n//2)` · Super Pow (exponent as digit array) · Matrix exponentiation for Fibonacci in O(log n).

---

### Modular Exponentiation and nCr mod p `🎯 T2`

> [!example] Problem
> Compute `b^e mod m` quickly, and answer many queries `nCr mod p` for prime `p = 10^9 + 7`.

> [!info] Approach
> **Mod-pow:** same square-and-halve, reducing `% m` after every multiply. Python built-in: `pow(b, e, m)`.
> **Inverse:** for prime `p`, Fermat gives `a^(p-1) ≡ 1`, so `a^-1 ≡ a^(p-2) (mod p)` (also `pow(a, -1, p)` on 3.8+).
> **nCr:** precompute `fact[i]`, then `inv_fact[n] = pow(fact[n], p-2, p)` **once** and walk down `inv_fact[i-1] = inv_fact[i] * i` — O(n) preprocessing, O(1) per query: `fact[n] * inv_fact[r] * inv_fact[n-r]`. See [lecture modular](../../02-algorithms/18-math-and-number-theory.md#6-modular-arithmetic) and [combinatorics](../../02-algorithms/18-math-and-number-theory.md#7-factorial--combinatorics).

> [!note]- Python Solution
> ```python
> def mod_pow(b, e, m):
>     r, b = 1, b % m
>     while e:
>         if e & 1:
>             r = r * b % m
>         b = b * b % m
>         e >>= 1
>     return r % m
>
> class Comb:
>     def __init__(self, n, p=10**9 + 7):
>         self.p = p
>         self.f = [1] * (n + 1)
>         for i in range(1, n + 1):
>             self.f[i] = self.f[i - 1] * i % p
>         self.inv = [1] * (n + 1)
>         self.inv[n] = pow(self.f[n], p - 2, p)
>         for i in range(n, 0, -1):
>             self.inv[i - 1] = self.inv[i] * i % p
>     def nCr(self, n, r):
>         if r < 0 or r > n:
>             return 0
>         return self.f[n] * self.inv[r] % self.p * self.inv[n - r] % self.p
> ```

> [!success] Complexity
> mod_pow O(log e); Comb build O(n + log p), query O(1); Space O(n).

> [!warning] Edge Cases & Gotchas
> Fermat inverse only works for **prime** modulus and `a % p != 0`; for composite `m` use extended Euclid · reduce after each multiply — `a * b * c % p` can hit huge ints (correct but slow) · subtraction: `(a - b) % p` (Python `%` is already non-negative) · `r < 0 or r > n` → 0 · `mod_pow(x, e, 1)` → 0.

> [!tip] Alternatives
> Pascal's triangle DP `C[n][r] = C[n-1][r-1] + C[n-1][r]` — O(n·r), no primes needed · `math.comb(n, r) % p` for a few queries.

> [!question] Follow-ups
> Lucas theorem when `n > p` · Count paths in grid (`C(m+n-2, m-1)`) · Number of ways with divisions modulo p.

---

## Geometry & Designs With Math

---

### Rectangle Overlap and Rectangle Area `🎯 T2`

> [!example] Problem
> **Overlap (LC 836):** rectangles `[x1,y1,x2,y2]`; return true iff they overlap with **positive area** (touching edges/corners = false).
> **Area (LC 223):** return the total area covered by two rectangles.

> [!info] Approach
> **Key insight:** two intervals on each axis overlap iff `max(starts) < min(ends)`. Rectangles overlap iff both axes do: `r1.x1 < r2.x2 and r2.x1 < r1.x2` and the same for y (use strict `<`).
> **Area:** `A + B - overlap`, where `w = min(x2s) - max(x1s)`, `h = min(y2s) - max(y1s)`, overlap = `w * h` only if both `> 0`.

> [!note]- Python Solution
> ```python
> def is_rectangle_overlap(r1, r2):
>     return r1[0] < r2[2] and r2[0] < r1[2] and r1[1] < r2[3] and r2[1] < r1[3]
>
> def compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
>     a = (ax2 - ax1) * (ay2 - ay1)
>     b = (bx2 - bx1) * (by2 - by1)
>     w = min(ax2, bx2) - max(ax1, bx1)
>     h = min(ay2, by2) - max(ay1, by1)
>     return a + b - (w * h if w > 0 and h > 0 else 0)
> ```

> [!success] Complexity
> Time O(1), Space O(1).

> [!warning] Edge Cases & Gotchas
> Strict vs non-strict inequality is the whole problem (shared edge → no overlap) · clamp negative `w`/`h` to 0 **before** multiplying (two negatives would multiply to a positive) · containment and identical rectangles handled by the same formula.

> [!question] Follow-ups
> Rectangle Area II (union of N rectangles, sweep line + segment tree) · Perfect Rectangle · Is point inside rotated rectangle (cross products).

---

### Detect Squares `⚡ T1`

> [!example] Problem
> `add(point)` adds a point (duplicates allowed). `count(point)` returns the number of ways to pick three stored points that together with the query form an axis-aligned square with positive area.
> Example: add `(3,10),(11,2),(3,2)`; `count((11,10))` → `1`.

> [!info] Approach
> **Key insight:** the query is one corner; a **diagonal** corner `(x2, y2)` fixes the square (side `d = |x2 - x|`, with `|y2 - y| == d`). Cheaper: fix a point `(x, y2)` in the same column (side `d = y2 - y`, `d != 0`); the other two corners are `(x ± d, y)` and `(x ± d, y2)`. Answer = Σ `cnt[(x,y2)] · cnt[(x2,y)] · cnt[(x2,y2)]` over both signs of `d`.
> Store a `Counter` of points (multiplicity multiplies) plus `by_x` list of **distinct** ys for each x to iterate candidates.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> class DetectSquares:
>     def __init__(self):
>         self.cnt = defaultdict(int)
>         self.by_x = defaultdict(list)   # x -> list of y (with multiplicity not needed)
>     def add(self, point):
>         x, y = point
>         if self.cnt[(x, y)] == 0:
>             self.by_x[x].append(y)
>         self.cnt[(x, y)] += 1
>     def count(self, point):
>         x, y = point
>         res = 0
>         for y2 in self.by_x[x]:
>             d = y2 - y
>             if d == 0:
>                 continue
>             for x2 in (x + d, x - d):
>                 res += self.cnt[(x, y2)] * self.cnt[(x2, y)] * self.cnt[(x2, y2)]
>         return res
> ```

> [!success] Complexity
> `add` O(1); `count` O(k) where k = distinct points sharing the query's x; Space O(n).

> [!warning] Edge Cases & Gotchas
> Multiplicities multiply — duplicates of any corner count separately · `d == 0` (the query's own point) must be skipped · only append to `by_x` the first time a point is seen (else the same y is iterated twice and the answer double counts) · `defaultdict` lookups insert zero entries; harmless here, use `.get` if memory matters.

> [!tip] Alternatives
> Iterate all stored points as diagonal candidates: O(n) per count, simpler to explain; the column-based loop is the optimization.

> [!question] Follow-ups
> Allow axis-aligned rectangles (not just squares) · Count squares in a static point set (O(n²) pairs of diagonals) · Remove-point support.

---

### Max Points on a Line `🎯 T2`

> [!example] Problem
> Given distinct 2D `points`, return the maximum number that lie on one straight line.
> Example: `[[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]` → `4`.

> [!info] Approach
> **Key insight:** for each anchor `i`, bucket later points `j` by the **direction** `(dx, dy)`; points in the same bucket are collinear with `i`. Avoid floats: reduce by `g = gcd(dx, dy)` and canonicalize sign (`dx > 0`, or `dx == 0 and dy > 0`) so `(1,2)` and `(-1,-2)` match. Best = max bucket + 1 (the anchor).

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> from math import gcd
>
> def max_points(points):
>     n = len(points)
>     best = min(n, 2)
>     for i in range(n):
>         slopes = defaultdict(int)
>         x1, y1 = points[i]
>         for j in range(i + 1, n):
>             dx, dy = points[j][0] - x1, points[j][1] - y1
>             g = gcd(dx, dy)
>             dx, dy = dx // g, dy // g
>             if dx < 0 or (dx == 0 and dy < 0):
>                 dx, dy = -dx, -dy
>             slopes[(dx, dy)] += 1
>             best = max(best, slopes[(dx, dy)] + 1)
>     return best
> ```

> [!success] Complexity
> Time O(n²) (gcd is O(log) per pair), Space O(n).

> [!warning] Edge Cases & Gotchas
> Never use float slope (precision collapses distinct slopes; `dy/dx` also divides by zero for vertical lines) · points are distinct in LC — with duplicates `gcd(0,0) = 0` crashes, count duplicates separately · `n <= 2` → `n` · only look at `j > i` so each pair is processed once.

> [!question] Follow-ups
> Allow duplicates (count `same` per anchor) · Line with maximum points through given anchors only · Minimum lines to cover all points (bitmask DP).

---

## Random Sampling

---

### Implement Rand10 Using Rand7 `🎯 T2`

> [!example] Problem
> Given `rand7()` uniform on `[1, 7]`, implement `rand10()` uniform on `[1, 10]`.

> [!info] Approach
> **Key insight:** `(rand7() - 1) * 7 + rand7()` is uniform on `[1, 49]` (base-7 two-digit number). Accept only `v ≤ 40` (a multiple of 10) and map with `(v - 1) % 10 + 1`; **reject and retry** otherwise. Rejection keeps uniformity because every accepted outcome is equally likely.
> Expected calls to `rand7` = 2 · 49/40 ≈ 2.45. (Optimization: reuse the rejected 41..49 residue as a smaller uniform source.)

> [!note]- Python Solution
> ```python
> def rand10(rand7):
>     while True:
>         v = (rand7() - 1) * 7 + rand7()      # uniform 1..49
>         if v <= 40:
>             return (v - 1) % 10 + 1
> ```

> [!success] Complexity
> Expected O(1) calls (≈ 2.45 `rand7` per result); worst case unbounded but probability decays geometrically; Space O(1).

> [!warning] Edge Cases & Gotchas
> `rand7() + rand7()` is **not** uniform (triangular distribution) · `rand7() * rand7()` is not uniform either · `rand7() + rand7() * 7` without the `-1` shifts range and breaks uniformity · must accept a multiple of 10 values.

> [!question] Follow-ups
> General `randM` from `randN` (`N^k ≥ M`, accept `< M·floor(N^k / M)`) · Reduce wasted samples by reusing leftovers.

---

### Random Point in Circle `💤 T3`

> [!example] Problem
> Given `radius` and center `(x_center, y_center)`, `randPoint()` returns a uniformly random point inside the circle.

> [!info] Approach
> **Key insight (rejection):** sample uniformly in the bounding square `[-r, r]²`, accept iff `x² + y² ≤ r²`. Acceptance probability = π/4 ≈ 78.5%, expected ≈ 1.27 tries.
> **Direct method:** `r' = R · sqrt(U)`, `θ = 2π · V` — the `sqrt` compensates for area growing ∝ r². Using `r' = R · U` clusters points near the center (classic bug).

> [!note]- Python Solution
> ```python
> import random
>
> def random_point_circle(radius, xc, yc, rnd=random.random):
>     while True:
>         x = (2 * rnd() - 1) * radius
>         y = (2 * rnd() - 1) * radius
>         if x * x + y * y <= radius * radius:
>             return [xc + x, yc + y]
> ```

> [!success] Complexity
> Expected O(1) tries, Space O(1).

> [!warning] Edge Cases & Gotchas
> Compare squared distances (no `sqrt`) · boundary inclusion is irrelevant (measure zero) · polar method without `sqrt` is **not** uniform.

> [!question] Follow-ups
> Random point in a rectangle union (weighted by area + prefix sums) · Random point in non-overlapping rectangles (LC 497) · Reservoir sampling.

---

## Integer Square Root

---

### Sqrt(x) and Valid Perfect Square `🎯 T2`

> [!example] Problem
> `mySqrt(x)`: return `floor(√x)` without `**0.5`. `isPerfectSquare(n)`: return whether `n` is a perfect square without `sqrt`.

> [!info] Approach
> **Key insight:** `m*m <= x` is monotone in `m` → binary search for the **largest** `m` satisfying it. Use the upper-mid `(lo + hi + 1) // 2` and `lo = m` / `hi = m - 1` so the loop converges. Perfect square: `r = isqrt(n); r*r == n`. See [Binary Search](../../02-algorithms/11-binary-search.md).

> [!note]- Python Solution
> ```python
> def my_sqrt(x):
>     lo, hi = 0, x
>     while lo < hi:
>         m = (lo + hi + 1) // 2
>         if m * m <= x:
>             lo = m
>         else:
>             hi = m - 1
>     return lo
>
> def is_perfect_square(n):
>     r = my_sqrt(n)
>     return r * r == n
> ```

> [!success] Complexity
> Time O(log x), Space O(1).

> [!warning] Edge Cases & Gotchas
> Lower-mid `(lo+hi)//2` with `lo = m` loops forever at `hi = lo + 1` · `x = 0, 1` · `m*m` would overflow in C++ — use `m <= x // m` there · `math.isqrt` is the production answer in Python.

> [!tip] Alternatives
> Newton: `r = x; while r*r > x: r = (r + x//r)//2` (quadratic convergence) · `math.isqrt` · float `int(x**0.5)` is wrong for large `x` (precision).

> [!question] Follow-ups
> Sum of two squares (two pointers up to √c) · Nth root / Pow with fractional exponent via binary search.

---

## See Also

- [Math & Number Theory lecture](../../02-algorithms/18-math-and-number-theory.md) — reference, canonical problems, quick revision triggers
- [Bit Manipulation practice](17-bit-manipulation.md) — Sum of Two Integers, Reverse Bits, Power of Two
- [Binary Search](../../02-algorithms/11-binary-search.md) — Sqrt(x) and answer-space search
- [Union-Find practice](14-union-find.md) — Largest Component Size by Common Factor (DSU on primes)
- [Dynamic Programming](../../02-algorithms/15-dynamic-programming.md) — combinatorics via DP, Pascal's triangle
- [Strings practice](02-string-algorithms.md) — digit-by-digit string arithmetic

---

## Flashcards

**Write the iterative fast-power loop and state its complexity.** #flashcard
`res = 1; while n: if n & 1: res *= x; x *= x; n >>= 1`. O(log n) multiplications. For negative `n`: `x, n = 1/x, -n` first. Add `% m` after each multiply for modular exponentiation (or use `pow(x, n, m)`).

**Why does the Sieve of Eratosthenes start crossing out at `i*i`, and what is its complexity?** #flashcard
Multiples `i*k` with `k < i` have a smaller prime factor and were already marked. Outer loop only to `√n`. Time O(n log log n), space O(n).

**How do you compute nCr mod p for many queries (p prime)?** #flashcard
Precompute `fact[0..n]`; `inv_fact[n] = pow(fact[n], p-2, p)` via Fermat, then `inv_fact[i-1] = inv_fact[i] * i % p`. Query: `fact[n] * inv_fact[r] % p * inv_fact[n-r] % p`. O(n) build, O(1) query. Requires p prime.

**How many trailing zeros does n! have, and why?** #flashcard
`n//5 + n//25 + n//125 + ...`. Each zero is a pair (2, 5); 2s are plentiful so count factors of 5, with extra ones from multiples of 25, 125, etc.

**How do you detect a repeating cycle in Fraction to Recurring Decimal?** #flashcard
Long division; map each remainder to the output index where it first appeared. A repeated remainder means digits from that index repeat: insert `(` there and append `)`. At most `den - 1` distinct remainders, so it terminates.

**Why must Excel title conversion subtract 1 before `% 26`?** #flashcard
Titles are bijective base-26 (A=1..Z=26, no zero digit). Doing `n -= 1; digit = n % 26; n //= 26` maps 26 → 'Z' and 52 → 'AZ' correctly; without it 26 yields '@'-style errors.

**Why use gcd-normalized (dx, dy) instead of float slope in Max Points on a Line?** #flashcard
Floats lose precision and vertical lines divide by zero. Reduce `(dx, dy)` by `gcd` and fix sign (dx > 0, or dx == 0 and dy > 0) so every direction has one canonical key.

**How do you build rand10 from rand7 and why does it stay uniform?** #flashcard
`v = (rand7()-1)*7 + rand7()` is uniform on 1..49. If `v <= 40` return `(v-1)%10 + 1`, else retry. Accepting a multiple of 10 values keeps each outcome equally likely. Expected ≈ 2.45 rand7 calls.

**Rectangle overlap with positive area — what is the test and the usual pitfall?** #flashcard
Overlap iff on both axes `max(starts) < min(ends)` (strict). Pitfall: using `<=` counts touching edges; in area computation, clamp negative width/height to 0 before multiplying.

**Detect Squares: how do you count squares for a query point efficiently?** #flashcard
For each stored distinct point sharing the query's x (side `d = y2 - y`, d != 0), try both `x ± d`; add `cnt[(x,y2)] * cnt[(x2,y)] * cnt[(x2,y2)]`. Multiplicities of duplicate points multiply.
