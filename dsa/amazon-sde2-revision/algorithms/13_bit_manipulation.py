"""
Bit Manipulation — Google L3 Cheat Sheet
=========================================

bin(10)         #convert to bin
# '0b1010'

int('1010', 2)      #convert to int
# 10

OPERATORS (memorize these cold)
---------------------------------
x & y       AND   — both bits set
x | y       OR    — either bit set
x ^ y       XOR   — bits differ (same→0, diff→1)
~x          NOT   — flip all bits (in Python: ~x == -x-1)
x << n      left shift  — multiply by 2^n
x >> n      right shift — divide by 2^n

ALWAYS use parentheses around bit ops: (x & y) == 0, not x & y == 0
(& | ^ have lower precedence than ==)

THE 6 TRICKS (L3 relevant)
----------------------------
x & (x - 1)        clear lowest set bit        → count set bits (Kernighan), check power of 2
x & (-x)            isolate lowest set bit       → used in BIT, single number III
x ^ x == 0          XOR with itself = 0          → cancel duplicates
x ^ 0 == x          XOR with 0 = identity        → XOR accumulator seed
1 << k              bitmask with only bit k set  → check/set/clear bit k
(x >> k) & 1        extract bit k               → iterate bits

COMMON PATTERNS
----------------
Check if power of 2:        n > 0 and (n & (n-1)) == 0
Count set bits:             while n: n &= n-1; count += 1
Get bit k:                  (x >> k) & 1
Set bit k:                  x | (1 << k)
Clear bit k:                x & ~(1 << k)
Toggle bit k:               x ^ (1 << k)
XOR to find missing/single: res = 0; for n in nums: res ^= n

L3 PROBLEMS MAP
----------------
Single Number I (LC 136)    XOR all — pairs cancel, unique survives
Missing Number (LC 268)     XOR indices with values — missing survives
Count Set Bits (LC 191)     n &= n-1 loop (Kernighan)
Counting Bits (LC 338)      dp[i] = 1 + dp[i - offset]
Reverse Bits (LC 190)       extract bit i, place at 31-i
Sum Without + (LC 371)      XOR = sum without carry, AND<<1 = carry; loop until carry=0
Subsets via bitmask (LC 78) for mask in range(1<<n): check bit k → include nums[k]

NOT L3 (skip for now): XOR basis, submask enumeration, bitmask DP, LC 421 (max XOR trie)

=========================================
Bit Manipulation patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Operator precedence: `&`, `|`, `^` have lower precedence than `==`. Always use parentheses!\n- Negative numbers in Python: Python integers have infinite precision, so `~` acts weirdly compared to C++/Java (often need `& 0xFFFFFFFF`).\n- Shifting by a negative amount or too large an amount.

Common Variants:
- Single Number (using XOR)\n- Counting bits (Brian Kernighan's algorithm `n & (n-1)`)\n- Subsets generation using bitmasks

General Tips & Best Practices:
- `x & (x - 1)` clears the lowest set bit.\n- `x & -x` extracts the lowest set bit.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List

class BitManipulationSolutions:
    # -----------------------------------------------------------------------
    # 1. Single Number I (LC 136) — T1
    # Given a non-empty array of integers nums, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space.
    # Example: nums = [2,2,1] → 1
    # Constraints: 1 <= nums.length <= 3 * 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def singleNumber(self, nums: List[int]) -> int:
        # Initialize the running XOR accumulator to 0 (since 0 ^ x = x).
        res = 0
        
        # Iterate through all numbers in the array. Since XOR is commutative and associative,
        # duplicate pairs will cancel each other out (n ^ n = 0), leaving only the unique number.
        for n in nums:
            res = res ^ n
        return res

    # -----------------------------------------------------------------------
    # 2. Single Number II (LC 137) — T1
    # Given a non-empty array of integers nums, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space.
    # Example: nums = [2,2,1] → 1
    # Constraints: 1 <= nums.length <= 3 * 10^4, exactly once. Find the single element and return it, You must implement a solution with a linear runtime complexity and use only constant extra space, 1 <= nums.length <= 3 * 10^4, 2^31 <= nums[i] <= 2^31 - 1, Each element in nums appears exactly three times except for one element which appears once
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def singleNumberII(self, nums: List[int]) -> int:
        # ones: tracks bits that have appeared 1 time (modulo 3)
        # twos: tracks bits that have appeared 2 times (modulo 3)
        ones, twos = 0, 0
        
        # Process each number bit-by-bit via state machine transitions
        for n in nums:
            # Update ones: include bits of n that are not already in twos (representing a 3rd count)
            ones = (ones ^ n) & ~twos
            # Update twos: include bits of n that were in ones but not in the new ones
            twos = (twos ^ n) & ~ones
        return ones

    # -----------------------------------------------------------------------
    # 3. Single Number III (LC 260) — T2
    # Given a non-empty array of integers nums, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space.
    # Example: nums = [2,2,1] → 1
    # Constraints: 1 <= nums.length <= 3 * 10^4, elements appear exactly twice. Find the two elements that appear only once. You can return the, answer in any order, You must write an algorithm that runs in linear runtime complexity and uses only constant extra, space, 2 <= nums.length <= 3 * 10^4, 2^31 <= nums[i] <= 2^31 - 1, Each integer in nums will appear twice, only two integers will appear once
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def singleNumberIII(self, nums: List[int]) -> List[int]:
        # XOR all numbers to find the XOR combination of the two unique elements (a ^ b)
        xor = 0
        for n in nums:
            xor ^= n
            
        # Isolate the lowest set bit in xor (diff_bit = xor & -xor).
        # Since a and b are distinct, at least one bit differs between them.
        # This bit is set in xor and will partition the numbers into two groups.
        diff_bit = xor & (-xor)
        
        # Accumulate XOR sum for numbers where the partitioning bit is set.
        # This will isolate one of the two unique elements (say, a).
        a = 0
        for n in nums:
            if diff_bit & n:
                a ^= n
                
        # The other unique number (b) is found by XORing the first unique number (a)
        # with the combined XOR sum (xor = a ^ b).
        return [a, xor ^ a]

    # -----------------------------------------------------------------------
    # 4. Number of 1 Bits (LC 191) — T2
    # Given a positive integer n, write a function that returns the number of set bits in its binary representation (also known as the Hamming weight).
    # Example: n = 11 → 3
    # Constraints: 1 <= n <= 2^31 - 1, Follow up: If this function is called many times, how would you optimize it?
    # Time: O(k) where k = number of set bits, Space: O(1)
    # -----------------------------------------------------------------------
    def hammingWeight(self, n: int) -> int:
        res = 0
        # Iterate while there are set bits remaining in n
        while n:
            # Kernighan's bit trick: clears the lowest set bit of n
            n &= (n - 1)
            # Increment count of set bits found
            res += 1
        return res

    # -----------------------------------------------------------------------
    # 5. Counting Bits (LC 338) — T2
    # Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n), ans[i] is the number of 1's in the binary representation of i.
    # Example: n = 2 → [0,1,1]
    # Constraints: 0 <= n <= 10^5, Follow up:, It is very easy to come up with a solution with a runtime of O(n log n). Can you do it in linear, time O(n) and possibly in a single pass?, Can you do it without using any built-in function (i.e., like __builtin_popcount in C++)?
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def countBits(self, n: int) -> List[int]:
        # Initialize DP table with zeros, representing counts for 0 to n.
        dp = [0] * (n + 1)
        # offset tracks the most significant power of 2 seen so far.
        offset = 1
        for i in range(1, n + 1):
            # When we reach a new power of 2, update the offset.
            if offset * 2 == i:
                offset = i
            # The count for i is 1 (for the MSB) plus the count of the remainder.
            dp[i] = 1 + dp[i - offset]
        return dp

    # -----------------------------------------------------------------------
    # 6. Reverse Bits (LC 190) — T2
    # Reverse bits of a given 32 bits signed integer.
    # Example: n = 43261596 → 964176192
    # Constraints: 0 <= n <= 2^31 - 2, n is even, Follow up: If this function is called many times, how would you optimize it?
    # Time: O(1), Space: O(1)
    # -----------------------------------------------------------------------
    def reverseBits(self, n: int) -> int:
        res = 0
        # Iterate over all 32 bit positions from 0 to 31.
        for i in range(32):
            # Extract the i-th bit from the input n.
            bit = (n >> i) & 1
            # Shift the extracted bit to its reversed position (31 - i) and merge it.
            res = res | (bit << (31 - i))
        return res

    # -----------------------------------------------------------------------
    # 7. Missing Number (LC 268) — T2
    # Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.
    # Example: nums = [3,0,1] → 2
    # Constraints: n == nums.length, 1 <= n <= 10^4, 0 <= nums[i] <= n, All the numbers of nums are unique, Follow up: Could you implement a solution using only O(1) extra space complexity and O(n) runtime, complexity?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def missingNumber(self, nums: List[int]) -> int:
        # Initialize result with the maximum index n (which equals len(nums)).
        res = len(nums)
        # For each index i, add i and subtract nums[i].
        # If nums contains all elements 0..n except one, matching elements
        # cancel each other out, leaving exactly the missing element.
        for i in range(len(nums)):
            res += (i - nums[i])
        return res

    # -----------------------------------------------------------------------
    # 8. Sum of Two Integers (LC 371) — T2
    # Given two integers a and b, return the sum of the two integers without using the operators + and -.
    # Example: a = 1, b = 2 → 3
    # Constraints: 1000 <= a, b <= 1000
    # Time: O(1), Space: O(1)
    # -----------------------------------------------------------------------
    def getSum(self, a: int, b: int) -> int:
        # 32-bit mask to handle Python's arbitrary-precision negative numbers
        mask = 0xffffffff
        # Loop until there is no carry left to add
        while (b & mask) > 0:
            # Carry bit is set at position i if both a and b have bit set at i-1
            carry = (a & b) << 1
            # Add without carry using XOR
            a = a ^ b
            # Shift carry to be processed in next iteration
            b = carry
        # If b is greater than 0, it means it completed carrying beyond 32 bits.
        # Mask the final result to 32 bits. If the result represents a negative number
        # (bit 31 is set), the mask operation (a & mask) will keep it positive,
        # but Python handles the check correctly using the b conditional.
        return (a & mask) if b > 0 else a

    # -----------------------------------------------------------------------
    # 9. Maximum XOR of Two Numbers in an Array (LC 421) — T1
    # Given an integer array nums, return the maximum result of nums[i] XOR nums[j], where 0 <= i <= j < n.
    # Example: nums = [3,10,5,25,2,8] → 28
    # Constraints: 1 <= nums.length <= 2 * 10^5, 0 <= nums[i] <= 2^31 - 1
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def findMaximumXOR(self, nums: List[int]) -> int:
        max_xor = 0
        mask = 0
        # Sweep bit positions from most significant (bit 31) down to 0
        for i in range(31, -1, -1):
            # Grow the prefix mask to include the current bit
            mask = mask | (1 << i)
            s = set()
            # Extract the prefix of each number using the mask and store it
            for num in nums:
                s.add(num & mask)
            # Hypothesize that the i-th bit of max_xor can be set to 1
            target = max_xor | (1 << i)
            # Find if there are two prefixes in our set that XOR to target
            for prefix in s:
                if target ^ prefix in s:
                    # If found, our hypothesis is correct: update max_xor
                    max_xor = target
                    break
        return max_xor

    # -----------------------------------------------------------------------
    # 10. Subsets via Bitmask (LC 78 variant) — T2
    # Given an integer array nums of unique elements, return all possible subsets (the power set) using bit manipulation. Key insight: For each mask in 0..2^N-1, bit k set means include nums[k]
    # Time: O(n * 2^n), Space: O(n * 2^n)
    # -----------------------------------------------------------------------
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """Subsets via Bitmask: Enumerate all integers from `0` to `2^n - 1`."""
        n = len(nums)
        res = []
        # Enumerate all 2^n possible subsets represented by bitmasks
        for mask in range(1 << n):   # 1 << n == 2^n
            subset = []
            # Check each element index k
            for k in range(n):
                # If the k-th bit of the mask is set, include nums[k]
                if mask & (1 << k):  # bit k is set → include nums[k]
                    subset.append(nums[k])
            res.append(subset)
        return res
    # -----------------------------------------------------------------------
    # 11. Reservoir Sampling — Random Pick Index (LC 398) — T2
    # Pick an index uniformly at random from indices where nums[i] == target.
    # -----------------------------------------------------------------------
    class RandomPickIndex:
        # Time: O(n), Space: O(n)
        def __init__(self, nums: List[int]):
            self.nums = nums

        # Time: O(n), Space: O(1)
        def pick(self, target: int) -> int:
            import random
            # Seed our result and match counter
            res = -1
            count = 0
            # Scan elements linearly to implement Reservoir Sampling
            for i, n in enumerate(self.nums):
                if n == target:
                    # Increment count of matching elements found
                    count += 1
                    # With probability 1/count, choose the current index i as candidate
                    if random.randint(1, count) == 1:
                        res = i
            return res

    # -----------------------------------------------------------------------
    # 12. Random Pick with Weight (LC 528) — T2
    # You are given a 0-indexed array of positive integers w where w[i] describes the weight of the i^th index. You need to implement the function pickIndex(), which randomly picks an index in the range [0, w.length - 1] (inclusive) and returns it. The probability of picking an index i is w[i] / sum(w). and the probability of picking index 1 is 3 / (1 + 3) = 0.75 (i.e., 75%).
    # Constraints: 1 <= w.length <= 10^4, 1 <= w[i] <= 10^5, pickIndex will be called at most 10^4 times
    # -----------------------------------------------------------------------
    class RandomPickWithWeight:
        # Time: O(n), Space: O(n)
        def __init__(self, weights: List[int]):
            self.prefix = []
            total = 0
            # Build prefix sum array where prefix[i] stores sum(w[0]..w[i])
            for w in weights:
                total += w
                self.prefix.append(total)
            self.total = total

        # Time: O(log n), Space: O(1)
        def pickIndex(self) -> int:
            import random
            # Pick a target weight uniformly from [1, total]
            target = random.randint(1, self.total)
            lo, hi = 0, len(self.prefix) - 1
            # Perform binary search to locate the index corresponding to the target range
            while lo < hi:
                mid = (lo + hi) // 2
                # If prefix[mid] is less than target, search right half
                if self.prefix[mid] < target:
                    lo = mid + 1
                else:
                    # Otherwise, search left half (inclusive of mid)
                    hi = mid
            return lo


class XORBasisSolutions:
    # Linear basis over GF(2) — find max XOR, count distinct XOR values (L4)
    # Gaussian elimination on bits

    # Time: O(1), Space: O(1)
    def __init__(self):
        # Initialize an empty list to store the linear basis vectors (pivots)
        self.basis = []

    # Time: O(k^2) where k = number of basis elements (at most 32), Space: O(k)
    def insert(self, num: int) -> None:
        # Reduce the inserted number against existing basis vectors
        for b in self.basis:
            num = min(num, num ^ b)
        # If num is not completely reduced to zero, it is independent
        if num:
            # Add to basis and sort descending to maintain MSB priority
            self.basis.append(num)
            self.basis.sort(reverse=True)

    # Time: O(k) where k = number of basis elements (at most 32), Space: O(1)
    def max_xor(self) -> int:
        result = 0
        # Greedily XOR basis elements from largest to smallest to maximize the output value
        for b in self.basis:
            result = max(result, result ^ b)
        return result

    # Maximum XOR of Two Numbers in Array (LC 421) — greedy bit-by-bit
    # Details: Given an integer array nums, return the maximum result of nums[i] XOR nums[j], where 0 <= i <= j < n.
    # Example 1:
    # Input: nums = [3,10,5,25,2,8]
    # Output: 28
    # Constraints:
    # - 1 <= nums.length <= 2 * 10^5
    # Time: O(n), Space: O(n)
    def findMaximumXOR(self, nums: List[int]) -> int:
        """Maximum XOR of Two Numbers in Array (LC 421). O(n)."""
        max_xor = 0
        mask = 0
        # Check each bit from MSB to LSB
        for i in range(31, -1, -1):
            # Grow mask to cover the current bit position
            mask |= (1 << i)
            # Create set of all prefixes of numbers using set comprehension
            prefixes = {num & mask for num in nums}
            # Try to see if target XOR (with current bit set) is possible
            candidate = max_xor | (1 << i)
            # Check if there exists some p such that (candidate ^ p) is also in prefixes
            if any((candidate ^ p) in prefixes for p in prefixes):
                max_xor = candidate
        return max_xor

    # Maximum XOR With an Element From Array (LC 1707) — offline queries + linear basis
    # Details: You are given an array nums consisting of non-negative integers. You are also given a queries array, where queries[i] = [xi, mi]. The answer to the ith query is the maximum bitwise XOR value of xi and any element of nums that does not exceed mi. If all elements in nums are larger than mi, then the answer is -1.
    # Example 1:
    # Input: nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
    # Output: [3,3,7]
    # Constraints:
    # - 1 <= nums.length, queries.length <= 10^5
    # Time: O((n + q) log n) where q = number of queries, Space: O(n + q)
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        """Maximum XOR of Two Numbers in Array (LC 421). O((n + q) log n) where q = number of queries."""
        # Sort input numbers to allow linear scan sweep based on limits
        nums.sort()
        # Sort queries based on their limit values (mi), preserving original query indices
        indexed_queries = sorted(enumerate(queries), key=lambda x: x[1][1])
        basis = []
        result = [-1] * len(queries)
        j = 0

        # Helper function to insert a number into the local basis
        def insert_basis(num):
            for i, b in enumerate(basis):
                num = min(num, num ^ b)
            if num:
                basis.append(num)
                # Keep basis sorted descending
                basis.sort(reverse=True)

        def query_max_xor(x):
            res = 0
            # Greedily search elements in linear basis to maximize XOR
            for b in basis:
                res = max(res, res ^ b)
            # Return max XOR value
            return res ^ x if basis else -1

        # Process each sorted query one-by-one
        for qi, (x, limit) in indexed_queries:
            # Insert all elements that are <= current query limit into our linear basis
            while j < len(nums) and nums[j] <= limit:
                insert_basis(nums[j])
                j += 1
            # If our linear basis has elements, find the maximum XOR of x
            if basis:
                r = x
                for b in basis:
                    r = max(r, r ^ b)
                result[qi] = r
        return result

class SubmaskEnumSolutions:
    # Submask enumeration — iterate all submasks of a mask in O(3^n) total (L4)

    # Time: O(2^k) where k = popcount(mask), Space: O(2^k)
    def enumerate_submasks(self, mask: int) -> List[int]:
        submasks = []
        sub = mask
        # Loop visits all submasks of the mask, moving from largest to smallest.
        while sub:
            submasks.append(sub)
            # sub - 1 flips the rightmost set bit in sub and sets all bits to its right.
            # & mask strips away any bits that were not in the original mask,
            # yielding the next valid submask.
            sub = (sub - 1) & mask
        # 0 (the empty submask) is always a valid submask, append it at the end.
        submasks.append(0)
        return submasks

    # Count OR Subsets (LC 2044) — count subsets with OR equal to max OR
    # Details: Given an integer array nums, find the maximum possible bitwise OR of a subset of nums and return the number of different non-empty subsets with the maximum bitwise OR.
    # Example 1:
    # Input: nums = [3,1]
    # Output: 2
    # Constraints:
    # - 1 <= nums.length <= 16
    # Time: O(n * 2^n), Space: O(1)
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        """Count OR Subsets (LC 2044). O(n * 2^n)."""
        max_or = 0
        # Determine the maximum OR value achievable by ORing all elements.
        for n in nums:
            max_or |= n
        count = 0
        # Iterate over all 2^len(nums) subsets using mask as a selector.
        # Start from 1 to only check non-empty subsets.
        for mask in range(1, 1 << len(nums)):
            cur_or = 0
            for i, n in enumerate(nums):
                # If the i-th bit is set, include nums[i] in the current subset OR sum.
                if mask & (1 << i):
                    cur_or |= n
            # If the current subset OR sum equals the maximum OR, increment count.
            if cur_or == max_or:
                count += 1
        return count

    # Partition to K Equal Sum Subsets (LC 698) — bitmask DP
    # Details: Given an integer array nums and an integer k, return true if it is possible to divide this array into k non-empty subsets whose sums are all equal.
    # Example 1:
    # Input: nums = [4,3,2,3,5,2,1], k = 4
    # Output: true
    # Constraints:
    # - 1 <= k <= nums.length <= 16
    # Time: O(n * 2^n), Space: O(2^n)
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        """Partition to K Equal Sum Subsets (LC 698). O(n * 2^n)."""
        total = sum(nums)
        # If the total sum is not divisible by k, partition is impossible.
        if total % k != 0:
            return False
        target = total // k
        n = len(nums)
        # dp[mask] stores whether the subset of elements selected by mask can form groups summing to target.
        dp = [False] * (1 << n)
        dp[0] = True
        # cur_sum[mask] stores the total accumulated sum of elements selected by mask.
        cur_sum = [0] * (1 << n)

        for mask in range(1 << n):
            # Skip if this subset configuration is unreachable.
            if not dp[mask]:
                continue
            for i in range(n):
                # Skip if the i-th element is already included in the mask.
                if mask & (1 << i):
                    continue
                next_mask = mask | (1 << i)
                # Skip if next state is already marked reachable.
                if dp[next_mask]:
                    continue
                # Calculate sum inside current partial partition group.
                add = cur_sum[mask] % target + nums[i]
                # If adding nums[i] doesn't exceed target, transition is valid.
                if add <= target:
                    dp[next_mask] = True
                    cur_sum[next_mask] = cur_sum[mask] + nums[i]

        # The final state with all elements used holds the result.
        return dp[(1 << n) - 1]

if __name__ == "__main__":
    sol = BitManipulationSolutions()
    xb = XORBasisSolutions()
    sm = SubmaskEnumSolutions()

    # singleNumber I
    assert sol.singleNumber([2, 2, 1]) == 1
    assert sol.singleNumber([4, 1, 2, 1, 2]) == 4

    # singleNumber II (appears 3x, one appears once)
    assert sol.singleNumberII([2, 2, 3, 2]) == 3
    assert sol.singleNumberII([0, 1, 0, 1, 0, 1, 99]) == 99

    # singleNumber III (two singles)
    assert sorted(sol.singleNumberIII([1, 2, 1, 3, 2, 5])) == [3, 5]

    # hammingWeight
    assert sol.hammingWeight(0b00000000000000000000000000001011) == 3
    assert sol.hammingWeight(0b10000000000000000000000000000000) == 1

    # countBits
    assert sol.countBits(5) == [0, 1, 1, 2, 1, 2]

    # reverseBits
    assert sol.reverseBits(0b00000010100101000001111010011100) == 964176192

    # missingNumber
    assert sol.missingNumber([3, 0, 1]) == 2
    assert sol.missingNumber([0, 1]) == 2

    # getSum (without + or -)
    assert sol.getSum(1, 2) == 3
    assert sol.getSum(-1, 1) == 0

    # findMaximumXOR (pairwise greedy)
    assert sol.findMaximumXOR([3, 10, 5, 25, 2, 8]) == 28
    assert sol.findMaximumXOR([0, 0]) == 0

    # subsets via bitmask
    res = sorted([sorted(s) for s in sol.subsets([1, 2, 3])])
    assert res == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

    # XOR Basis max_xor
    xb2 = XORBasisSolutions()
    for n in [1, 2, 4, 8]:
        xb2.insert(n)
    assert xb2.max_xor() == 15  # 1|2|4|8 in GF(2)

    # XOR Basis findMaximumXOR (pairwise)
    assert xb.findMaximumXOR([3, 10, 5, 25, 2, 8]) == 28

    # maximizeXor (offline queries)
    result = xb.maximizeXor([0, 1, 2, 3, 4], [[3, 1], [1, 3], [5, 6]])
    assert result == [3, 3, 7]

    # enumerate_submasks
    subs = sm.enumerate_submasks(0b1010)
    assert sorted(subs) == sorted([0b1010, 0b1000, 0b0010, 0b0000])

    # countMaxOrSubsets
    assert sm.countMaxOrSubsets([3, 1]) == 2  # OR=3: {3}, {3,1} -> max_or=3
    assert sm.countMaxOrSubsets([2, 2, 2]) == 7

    # canPartitionKSubsets
    assert sm.canPartitionKSubsets([4, 3, 2, 3, 5, 2, 1], 4) == True
    assert sm.canPartitionKSubsets([1, 2, 3, 4], 3) == False

    print("All bit manipulation tests passed.")
