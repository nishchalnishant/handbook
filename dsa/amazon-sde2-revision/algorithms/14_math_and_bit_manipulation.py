"""
Math & Bit Manipulation — L3 Cheat Sheet
=========================================

TRICK PER PROBLEM (memorize these, not the full solutions):

  countPrimes (LC 204)         Sieve: mark multiples starting at p*p, loop to sqrt(n)
  trailingZeroes (LC 172)      Count factors of 5: sum n//5 + n//25 + n//125 + ...
  rangeBitwiseAnd (LC 201)     Shift both right until equal (= common prefix), shift result left
  titleToNumber (LC 171)       Like base-26: res = res * 26 + (ord(c) - ord('A') + 1)
  gcdOfStrings (LC 1071)       str1+str2 == str2+str1? If yes: str1[:gcd(len1,len2)]
  findNthDigit (LC 400)        Find digit group (1-digit: 9, 2-digit: 90*2, ...), then exact number
  isPalindrome (LC 9)          Reverse second half; compare x == rev or x == rev//10 (odd length)
  isPowerOfTwo (LC 231)        n > 0 and (n & (n-1)) == 0
  numberToWords (LC 273)       Process chunks of 1000; helper for each 3-digit group; recurse
  convertToTitle (LC 168)      columnNumber -= 1 each iter to handle 1-indexed; build right-to-left
  fractionToDecimal (LC 166)   Long division; track remainder->index in map; insert '(' at repeat start
  numSquares (LC 279)          DP: dp[i] = min(dp[i-sq]+1) for each perfect sq <= i
  largestNumber (LC 179)       Custom sort: compare a+b vs b+a as strings; lstrip('0') or '0'
  superPow (LC 372)            a^(10x+d) = (a^x)^10 * a^d; process digits left-to-right with pow(..., MOD)
  countDigitOne (LC 233)       Per digit: higher*factor + (0 if cur==0, lower+1 if cur==1, factor if >1)
  isUgly (LC 263)              Divide out 2, 3, 5; check n == 1
  nthUglyNumber (LC 264)       3-pointer DP: next = min(dp[p2]*2, dp[p3]*3, dp[p5]*5); advance all that match
  nthSuperUglyNumber (LC 313)  Same as above but k pointers for k primes
  josephus                     pos = 0; for i in 2..n: pos = (pos+k) % i
  sieveOfEratosthenes          is_prime[p*p::p] = [False]*... for p in range(2, sqrt(n)+1)
  pascalTriangle (LC 118/119)  Each row: [1] + [prev[j-1]+prev[j]] + [1]; LC 119: update in-place right-to-left
  isStrobogrammatic (LC 246)   Map {0:0,1:1,6:9,8:8,9:6}; two pointers inward; check both match
  findStrobogrammatic (LC 247) Recursive: wrap inner results with valid outer pairs; skip leading '0'

QUICK PATTERNS:
  Power of 2         : n > 0 and (n & (n-1)) == 0
  Excel col -> num   : res = res*26 + (ord(c)-ord('A')+1)  [left to right]
  Excel num -> col   : col -= 1 each iter, prepend chr(ord('A') + col%26), col //= 26  [right to left]
  Trailing zeros n!  : sum n//(5**i) while 5**i <= n

SKIP FOR L3 (L4+ only):
  Digit DP, bitmask DP, XOR basis, Sprague-Grundy, convex hull trick
"""

from typing import List, Dict
import heapq
import math
import collections

class MathAndBitManipulation:
    # -----------------------------------------------------------------------
    # 1. Count Primes — T1
    # Given an integer n, return the number of prime numbers that are strictly less than n.
    # Example: n = 10 → 4
    # Constraints: 0 <= n <= 5 * 10^6
    # Time: O(n log log n), Space: O(n)
    # -----------------------------------------------------------------------
    def countPrimes(self, n: int) -> int:
        # If n is 2 or less, there are no primes strictly less than n.
        if n <= 2:
            return 0

        # Initialize prime tracking list. Index represents the number, value is primality.
        primes = [True] * n
        # 0 and 1 are not primes.
        primes[0] = primes[1] = False

        # Loop from 2 up to sqrt(n).
        for p in range(2, int(n ** 0.5) + 1):
            # If p is prime, mark all of its multiples starting from p*p as non-prime.
            if primes[p]:
                for i in range(p * p, n, p):
                    primes[i] = False

        # Sum the prime flags to count total primes strictly less than n.
        return sum(primes)

    # -----------------------------------------------------------------------
    # 2. Factorial Trailing Zeroes — T2
    # Given an integer n, return the number of trailing zeroes in n!. Note that n! = n * (n - 1) * (n - 2) * ... * 3 * 2 * 1.
    # Example: n = 3 → 0
    # Constraints: 0 <= n <= 10^4, Follow up: Could you write a solution that works in logarithmic time complexity?
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def trailingZeroes(self, n: int) -> int:
        zero_count = 0
        current_multiple = 5
        # Count total factors of 5 by dividing by powers of 5 (5, 25, 125, ...).
        while n >= current_multiple:
            # Accumulate quotients.
            zero_count += n // current_multiple
            # Shift to the next power of 5.
            current_multiple *= 5
        return zero_count

    # -----------------------------------------------------------------------
    # 3. Bitwise AND of Numbers Range — T2
    # Given two integers left and right that represent the range [left, right], return the bitwise AND of all numbers in this range, inclusive.
    # Example: left = 5, right = 7 → 4
    # Constraints: 0 <= left <= right <= 2^31 - 1
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        shift = 0
        # Shift both numbers right until they match, isolating the common binary prefix.
        while left < right:
            left >>= 1
            right >>= 1
            shift += 1
        # Re-introduce the trailing zeros by shifting left.
        return left << shift

    # -----------------------------------------------------------------------
    # 4. Excel Sheet Column Number — T2
    # Given a string columnTitle that represents the column title as appears in an Excel sheet, return its corresponding column number. For example: A -> 1 B -> 2 C -> 3 ... Z -> 26 AA -> 27 AB -> 28 ...
    # Example: columnTitle = "A" → 1
    # Constraints: 1 <= columnTitle.length <= 7, columnTitle consists only of uppercase English letters, columnTitle is in the range ["A", "FXSHRXW"]
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def titleToNumber(self, columnTitle: str) -> int:
        res = 0
        # Loop through each character in the title.
        for char in columnTitle:
            # Shift the base of the accumulated result and add the mapped value of the character.
            res = res * 26 + (ord(char) - ord('A') + 1)
        return res

    # -----------------------------------------------------------------------
    # 5. Greatest Common Divisor of Strings — T2
    # For two strings s and t, we say "t divides s" if and only if s = t + t + t + ... + t + t (i.e., t is concatenated with itself one or more times). Given two strings str1 and str2, return the largest string x such that x divides both str1 and str2.
    # Example: str1 = "ABCABC", str2 = "ABC" → "ABC"
    # Constraints: 1 <= str1.length, str2.length <= 1000, str1 and str2 consist of English uppercase letters
    # Time: O(m + n), Space: O(m + n)
    # -----------------------------------------------------------------------
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        import math
        # If order of concatenation changes the combined string, no common divisor string exists.
        if str1 + str2 != str2 + str1:
            return ""
        # Get the numeric GCD of the lengths and slice the prefix of that length.
        return str1[:math.gcd(len(str1), len(str2))]

    # -----------------------------------------------------------------------
    # 6. Nth Digit — T2
    # Given an integer n, return the n^th digit of the infinite integer sequence [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...].
    # Example: n = 3 → 3
    # Constraints: 1 <= n <= 2^31 - 1
    # Time: O(log n), Space: O(log n)
    # -----------------------------------------------------------------------
    def findNthDigit(self, n: int) -> int:
        digit_len = 1
        count = 9
        start = 1

        # Advance through digit groups (1-digit, 2-digits, 3-digits...) until n is within the group.
        while n > digit_len * count:
            n -= digit_len * count
            digit_len += 1
            count *= 10
            start *= 10

        # Calculate the actual number containing the nth digit.
        start += (n - 1) // digit_len
        s = str(start)
        # Return the exact digit as an integer.
        return int(s[(n - 1) % digit_len])

    # -----------------------------------------------------------------------
    # 7. Palindrome Number — T1
    # Given an integer x, return true if x is a palindrome, and false otherwise.
    # Example: x = 121 → true
    # Constraints: 2^31 <= x <= 2^31 - 1, Follow up: Could you solve it without converting the integer to a string?
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def isPalindrome(self, x: int) -> bool:
        # Negative numbers and non-zero numbers ending in 0 cannot be palindromic.
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reverted_half = 0
        # Reverse digits until we've processed half of them.
        while x > reverted_half:
            reverted_half = reverted_half * 10 + x % 10
            x //= 10

        # For even lengths: x == reverted_half
        # For odd lengths: x == reverted_half // 10 (discards the middle digit)
        return x == reverted_half or x == reverted_half // 10

    # -----------------------------------------------------------------------
    # 8. Power of Two — T2
    # Given an integer n, return true if it is a power of two. Otherwise, return false. An integer n is a power of two, if there exists an integer x such that n == 2^x.
    # Example: n = 1 → true
    # Constraints: 2^31 <= n <= 2^31 - 1, Follow up: Could you solve it without loops/recursion?
    # Time: O(1), Space: O(1)
    # -----------------------------------------------------------------------
    def isPowerOfTwo(self, n: int) -> bool:
        # Power of 2 must be positive.
        if n <= 0:
            return False
        # Use bitwise AND with n-1 to check if there is exactly one set bit.
        return (n & (n - 1)) == 0

    # -----------------------------------------------------------------------
    # 11. Fraction to Recurring Decimal (LC 166)
    # Given two integers representing the numerator and denominator of a fraction, return the fraction in string format. If the fractional part is repeating, enclose the repeating part in parentheses.
    # Time: O(denominator), Space: O(denominator)
    # -----------------------------------------------------------------------
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        """Fraction to Recurring Decimal (LC 166): Simulate long division."""
        # Zero divided by any number is zero.
        if numerator == 0:
            return "0"

        # If one operand is negative (but not both), the result is negative.
        sign = "-" if (numerator < 0) ^ (denominator < 0) else ""
        # Work with positive numbers for convenience.
        numerator, denominator = abs(numerator), abs(denominator)

        # Calculate the integer quotient and the remainder.
        integer_part = numerator // denominator
        remainder = numerator % denominator

        # If it divides evenly, return the integer part.
        if remainder == 0:
            return sign + str(integer_part)

        fraction_chars = []
        # Store index of where a remainder was first seen to detect recurring cycles.
        remainder_map: Dict[int, int] = {}

        # Loop until division terminates or we find a repeating remainder.
        while remainder != 0:
            # Repeating remainder found: insert parentheses around the cycle.
            if remainder in remainder_map:
                insert_pos = remainder_map[remainder]
                fraction_chars.insert(insert_pos, '(')
                fraction_chars.append(')')
                break
            # Record the index of the first digit generated by this remainder.
            remainder_map[remainder] = len(fraction_chars)
            # Multiply remainder by 10 to compute the next decimal digit.
            remainder *= 10
            fraction_chars.append(str(remainder // denominator))
            # Get the new remainder.
            remainder %= denominator

        # Combine the sign, integer part, decimal point, and fractional part.
        return sign + str(integer_part) + "." + "".join(fraction_chars)

    # -----------------------------------------------------------------------
    # 12. Perfect Squares (LC 279)
    # Given an integer n, return the least number of perfect square numbers that sum to n.
    # Time: O(n * sqrt(n)), Space: O(n)
    # -----------------------------------------------------------------------
    def numSquares(self, n: int) -> int:
        # Generate all perfect squares smaller than or equal to n.
        squares = [j * j for j in range(1, int(n ** 0.5) + 1)]
        # dp[i] will store the minimum number of perfect squares that sum to i.
        dp = [float('inf')] * (n + 1)
        # 0 requires 0 perfect squares.
        dp[0] = 0

        # Fill the DP table up to n.
        for i in range(1, n + 1):
            # Try subtracting each perfect square.
            for sq in squares:
                if sq > i:
                    break
                # Update with the minimum choice.
                dp[i] = min(dp[i], dp[i - sq] + 1)

        return dp[n]

    # -----------------------------------------------------------------------
    # 13. Largest Number (LC 179)
    # Given a list of non-negative integers nums, arrange them such that they form the largest number and return it as a string.
    # Time: O(n log n * k) where k is max digit length, Space: O(n)
    # -----------------------------------------------------------------------
    def largestNumber(self, nums: List[int]) -> str:
        import functools

        # Custom comparison function: checks which concatenation order is larger.
        def compare(a: str, b: str) -> int:
            # If a followed by b is larger, order as a then b (return negative for sorting).
            """Comparator helper used to order candidate values."""
            if a + b > b + a:
                return -1
            # If b followed by a is larger, order as b then a (return positive).
            elif a + b < b + a:
                return 1
            return 0

        # Convert integers to string representations.
        strs = [str(n) for n in nums]
        # Sort using the custom comparator.
        strs.sort(key=functools.cmp_to_key(compare))
        # Join the sorted strings.
        result = "".join(strs)
        # Strip leading zeros, returning "0" if all inputs were zero.
        return result.lstrip('0') or '0'

    # -----------------------------------------------------------------------
    # 14. Super Pow (LC 372)
    # Your task is to calculate a^b mod 1337 where a is a positive integer and b is an extremely large positive integer given in the form of an array.
    # Time: O(n) where n = len(b), Space: O(1)
    # -----------------------------------------------------------------------
    def superPow(self, a: int, b: List[int]) -> int:
        MOD = 1337
        result = 1
        # Reduce the base modulo 1337 initially.
        a %= MOD
        # Process the exponent digits from left to right.
        for digit in b:
            # a^(10*x + digit) = (a^x)^10 * a^digit
            result = pow(result, 10, MOD) * pow(a, digit, MOD) % MOD
        return result

    # -----------------------------------------------------------------------
    # 17. Ugly Number II (LC 264)
    # An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Given an integer n, return the nth ugly number.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def nthUglyNumber(self, n: int) -> int:
        """Ugly Number II (LC 264): Use a three-pointer DP approach."""
        # dp[i] stores the (i+1)-th ugly number.
        dp = [1] * n
        # Three pointers tracking indices in the dp list for prime factors 2, 3, and 5.
        p2 = p3 = p5 = 0

        # Generate ugly numbers up to index n-1.
        for i in range(1, n):
            # Compute candidates for the next ugly number.
            next2 = dp[p2] * 2
            next3 = dp[p3] * 3
            next5 = dp[p5] * 5
            # Select the smallest candidate.
            next_ugly = min(next2, next3, next5)
            dp[i] = next_ugly
            # Advance all pointers that produced the selected next_ugly to avoid duplicates.
            if next_ugly == next2:
                p2 += 1
            if next_ugly == next3:
                p3 += 1
            if next_ugly == next5:
                p5 += 1

        # Return the n-th ugly number.
        return dp[n - 1]

    # -----------------------------------------------------------------------
    # 18. Super Ugly Number (LC 313)
    # A super ugly number is a positive integer whose prime factors are a subset of the given primes array. Given an integer n and an array of integers primes, return the nth super ugly number.
    # Time: O(n * k) where k = len(primes), Space: O(n + k)
    # -----------------------------------------------------------------------
    def nthSuperUglyNumber(self, n: int, primes: List[int]) -> int:
        k = len(primes)
        # dp[i] stores the (i+1)-th super ugly number.
        dp = [1] * n
        # Track pointers for each prime factor.
        pointers = [0] * k

        # Generate super ugly numbers.
        for i in range(1, n):
            # Compute next candidate for each prime.
            candidates = [dp[pointers[j]] * primes[j] for j in range(k)]
            # Choose the minimum candidate.
            next_ugly = min(candidates)
            dp[i] = next_ugly
            # Advance pointers for all primes matching the chosen minimum.
            for j in range(k):
                if candidates[j] == next_ugly:
                    pointers[j] += 1

        # Return the n-th super ugly number.
        return dp[n - 1]

    # -----------------------------------------------------------------------
    # 19. Josephus Problem
    # n people stand in a circle. Starting from person 0, every k-th person is eliminated. Find the position of the last survivor (0-indexed).
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def josephus(self, n: int, k: int) -> int:
        # Base case: 1 person circle has survivor at position 0.
        pos = 0
        # Iteratively build up the survivor's position from size 2 to n.
        for i in range(2, n + 1):
            # The survivor's index shifts by k positions (modulo current size i).
            pos = (pos + k) % i
        return pos

    # -----------------------------------------------------------------------
    # 20. Sieve of Eratosthenes (Primes) — prime generation
    # Return a list of all prime numbers up to and including n.
    # Time: O(n log log n), Space: O(n)
    # -----------------------------------------------------------------------
    def sieveOfEratosthenes(self, n: int) -> List[int]:
        # Primes start from 2.
        if n < 2:
            return []
        # Create prime status lookup list, index from 0 to n.
        is_prime = [True] * (n + 1)
        # 0 and 1 are not primes.
        is_prime[0] = is_prime[1] = False
        # Filter multiples of primes up to sqrt(n).
        for p in range(2, int(n ** 0.5) + 1):
            if is_prime[p]:
                # Slice assignment to mark all multiples p*p, p*p + p, ... as False.
                is_prime[p * p::p] = [False] * len(is_prime[p * p::p])
        # Return indices that are still marked as True.
        return [i for i, v in enumerate(is_prime) if v]

    # -----------------------------------------------------------------------
    # 23. Strobogrammatic Number II (LC 247)
    # Given an integer n, return all strobogrammatic numbers of length n.
    # Example: n=2 → ["11","69","88","96"]
    # Time: O(5^(n/2)), Space: O(5^(n/2))
    # -----------------------------------------------------------------------
    def findStrobogrammatic(self, n: int) -> List[str]:
        # Symmetric strobogrammatic pairs.
        pairs = [('0', '0'), ('1', '1'), ('6', '9'), ('8', '8'), ('9', '6')]

        # Recursive helper to generate numbers of the specified sub-length.
        def helper(length: int, original_n: int) -> List[str]:
            # Base case for even length.
            """Helper routine used by the enclosing solution."""
            if length == 0:
                return [""]
            # Base case for odd length.
            if length == 1:
                return ["0", "1", "8"]
            # Recurse on length-2 to generate the inner parts.
            middles = helper(length - 2, original_n)
            result = []
            # Wrap each middle sequence with valid strobogrammatic outer pairs.
            for mid in middles:
                for left, right in pairs:
                    # Avoid leading zeros on the outermost boundary.
                    if left == '0' and length == original_n:
                        continue
                    result.append(left + mid + right)
            return result

        return helper(n, n)


if __name__ == "__main__":
    sol = MathAndBitManipulation()

    # countPrimes (Sieve of Eratosthenes)
    assert sol.countPrimes(10) == 4  # 2,3,5,7
    assert sol.countPrimes(0) == 0
    assert sol.countPrimes(1) == 0

    # trailingZeroes (count factors of 5)
    assert sol.trailingZeroes(3) == 0
    assert sol.trailingZeroes(5) == 1
    assert sol.trailingZeroes(25) == 6   # 25 contributes 2 factors of 5

    # rangeBitwiseAnd
    assert sol.rangeBitwiseAnd(5, 7) == 4
    assert sol.rangeBitwiseAnd(0, 0) == 0
    assert sol.rangeBitwiseAnd(1, 2147483647) == 0

    # titleToNumber (Excel column)
    assert sol.titleToNumber("A") == 1
    assert sol.titleToNumber("Z") == 26
    assert sol.titleToNumber("AB") == 28
    assert sol.titleToNumber("ZY") == 701

    # gcdOfStrings
    assert sol.gcdOfStrings("ABCABC", "ABC") == "ABC"
    assert sol.gcdOfStrings("ABABAB", "ABAB") == "AB"
    assert sol.gcdOfStrings("LEET", "CODE") == ""

    # findNthDigit
    assert sol.findNthDigit(3) == 3
    assert sol.findNthDigit(11) == 0   # "10" -> digit at pos 11 is '0'
    assert sol.findNthDigit(1) == 1

    # isPalindrome (number)
    assert sol.isPalindrome(121) == True
    assert sol.isPalindrome(-121) == False
    assert sol.isPalindrome(10) == False
    assert sol.isPalindrome(0) == True

    # isPowerOfTwo
    assert sol.isPowerOfTwo(1) == True
    assert sol.isPowerOfTwo(16) == True
    assert sol.isPowerOfTwo(3) == False
    assert sol.isPowerOfTwo(0) == False

    # fractionToDecimal (LC 166)
    assert sol.fractionToDecimal(1, 2) == "0.5"
    assert sol.fractionToDecimal(2, 3) == "0.(6)"
    assert sol.fractionToDecimal(4, 333) == "0.(012)"
    assert sol.fractionToDecimal(0, 3) == "0"
    assert sol.fractionToDecimal(-1, 2) == "-0.5"
    assert sol.fractionToDecimal(1, 6) == "0.1(6)"

    # numSquares (LC 279)
    assert sol.numSquares(12) == 3  # 4+4+4
    assert sol.numSquares(13) == 2  # 4+9
    assert sol.numSquares(1) == 1
    assert sol.numSquares(4) == 1

    # largestNumber (LC 179)
    assert sol.largestNumber([10, 2]) == "210"
    assert sol.largestNumber([3, 30, 34, 5, 9]) == "9534330"
    assert sol.largestNumber([0, 0]) == "0"
    assert sol.largestNumber([1]) == "1"

    # superPow (LC 372)
    assert sol.superPow(2, [3]) == 8
    assert sol.superPow(2, [1, 0]) == 1024
    assert sol.superPow(1, [4, 3, 3, 8, 5, 2]) == 1

    # nthUglyNumber (LC 264)
    assert sol.nthUglyNumber(10) == 12
    assert sol.nthUglyNumber(1) == 1
    assert sol.nthUglyNumber(7) == 8

    # nthSuperUglyNumber (LC 313)
    assert sol.nthSuperUglyNumber(12, [2, 7, 13, 19]) == 32
    assert sol.nthSuperUglyNumber(1, [2, 3, 5]) == 1

    # josephus
    assert sol.josephus(7, 3) == 3
    assert sol.josephus(1, 1) == 0
    assert sol.josephus(6, 2) == 4

    # sieveOfEratosthenes
    assert sol.sieveOfEratosthenes(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    assert sol.sieveOfEratosthenes(1) == []
    assert sol.sieveOfEratosthenes(2) == [2]

    # findStrobogrammatic (LC 247)
    assert sorted(sol.findStrobogrammatic(2)) == sorted(["11", "69", "88", "96"])
    assert sorted(sol.findStrobogrammatic(1)) == sorted(["0", "1", "8"])

    print("All math & bit manipulation tests passed.")
