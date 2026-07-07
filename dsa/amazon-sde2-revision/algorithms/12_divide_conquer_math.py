"""
Divide & Conquer / Math patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Stack overflow on deep recursion trees.\n- Math edge cases: division by zero, modulo of negative numbers.\n- Forgetting the merge step complexity in Divide and Conquer.

Common Variants:
- Merge Sort / Quick Sort\n- Pow(x, n)\n- Majority Element

General Tips & Best Practices:
- Divide and conquer usually results in O(N log N) time.\n- For math problems, look for patterns or use GCD/LCM.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

import math
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class DivideConquerMathSolutions:
    # -----------------------------------------------------------------------
    # 1. Pow(x, n) (LC 50) — T2
    # Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).
    # Example: x = 2.00000, n = 10 → 1024.00000
    # Constraints: 100.0 < x < 100.0, 2^31 <= n <= 2^31-1, 100.0 < x < 100.0, 2^31 <= n <= 2^31-1, n is an integer, Either x is not zero or n > 0, 10^4 <= x^n <= 10^4
    # Time: O(log n), Space: O(log n)
    # -----------------------------------------------------------------------
    def myPow(self, x: float, n: int) -> float:
        def helper(x, n):
            """Helper routine used by the enclosing solution."""
            if x == 0: return 0
            if n == 0: return 1
            # Recursively solve for x^(n//2).
            res = helper(x, n // 2)
            # Square the half-power result.
            res = res * res
            # If n is odd, multiply by x one more time.
            return x * res if n % 2 else res

        res = helper(x, abs(n))
        return res if n >= 0 else 1 / res

    # -----------------------------------------------------------------------
    # 2. Maximum Subarray (LC 53) — T1
    # Given an integer array nums, find the subarray with the largest sum, and return its sum.
    # Example: nums = [-2,1,-3,4,-1,2,1,-5,4] → 6
    # Constraints: 1 <= nums.length <= 10^5
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxSubArray(self, nums: List[int]) -> int:
        res = nums[0]
        cur = 0
        for n in nums:
            # If current subarray sum is negative, discard it and start fresh.
            if cur < 0:
                cur = 0
            # Add current element to the subarray.
            cur += n
            # Keep track of global maximum sum.
            res = max(res, cur)
        return res

    # -----------------------------------------------------------------------
    # 3. Merge K Sorted Lists (LC 23) — T2
    # You are given an array of k linked-lists lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.
    # Example: lists = [[1,4,5],[1,3,4],[2,6]] → [1,1,2,3,4,4,5,6]
    # Constraints: k == lists.length, 0 <= k <= 10^4, 0 <= lists[i].length <= 500, 10^4 <= lists[i][j] <= 10^4, lists[i] is sorted in ascending order, The sum of lists[i].length will not exceed 10^4
    # Time: O(n log k), Space: O(1)
    # -----------------------------------------------------------------------
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists or len(lists) == 0:
            return None
        # Pairwise merge lists until only one list remains.
        while len(lists) > 1:
            mergedLists = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                # If there's no pair for the last list, use None.
                l2 = lists[i + 1] if (i + 1) < len(lists) else None
                mergedLists.append(self.mergeList(l1, l2))
            lists = mergedLists
        return lists[0]

    def mergeList(self, l1, l2):
        dummy = ListNode()
        tail = dummy
        # Merge nodes of l1 and l2 in sorted order.
        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        # Append remaining nodes from either list.
        if l1: tail.next = l1
        if l2: tail.next = l2
        return dummy.next

    # -----------------------------------------------------------------------
    # 4. Happy Number — T2
    # Write an algorithm to determine if a number n is happy. A happy number is a number defined by the following process:
    # 1. Starting with any positive integer, replace the number by the sum of the squares of its digits.
    # 2. Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
    # 3. Those numbers for which this process ends in 1 are happy.
    # Return true if n is a happy number, and false if not.
    # Example: n = 19 → true
    # Constraints: 1 <= n <= 2^31 - 1
    # Time: O(log n), Space: O(log n)
    # -----------------------------------------------------------------------
    def isHappy(self, n: int) -> bool:
        visit = set()
        # Loop while no cycle is detected.
        while n not in visit:
            visit.add(n)
            n = self.sumOfSquares(n)
            # 1 indicates a happy number.
            if n == 1:
                return True
        return False

    def sumOfSquares(self, n):
        output = 0
        while n:
            # Extract last digit.
            digit = n % 10
            # Square the digit and add to output.
            digit = digit ** 2
            output += digit
            # Move to next digit.
            n = n // 10
        return output

    # -----------------------------------------------------------------------
    # 5. Reverse Integer — T2
    # Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-2^31, 2^31 - 1], then return 0. Assume the environment does not allow you to store 64-bit integers (signed or unsigned).
    # Example: x = 123 → 321
    # Constraints: 2^31 <= x <= 2^31 - 1
    # Time: O(log x), Space: O(1)
    # -----------------------------------------------------------------------
    def reverse(self, x: int) -> int:
        MIN, MAX = -2147483648, 2147483647
        res = 0
        while x:
            # Extract last digit preserving sign (C-style fmod).
            digit = int(math.fmod(x, 10))
            # Truncate toward zero.
            x = int(x / 10)
            # Check overflow for positive and negative bounds.
            if res > MAX // 10 or (res == MAX // 10 and digit > MAX % 10):
                return 0
            if res < MIN // 10 or (res == MIN // 10 and digit < MIN % 10):
                return 0
            # Append digit to reversed result.
            res = (res * 10) + digit
        return res

    # -----------------------------------------------------------------------
    # 6. Majority Element (LC 169) — T2
    # Given an array nums of size n, return the majority element. The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.
    # Example: nums = [3,2,3] → 3
    # Constraints: n == nums.length, 1 <= n <= 5 * 10^4, 10^9 <= nums[i] <= 10^9, The input is generated such that a majority element will exist in the array, Follow-up: Could you solve the problem in linear time and in O(1) space?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def majorityElement(self, nums: List[int]) -> int:
        count, candidate = 0, None
        for n in nums:
            # Adopt new candidate when count falls to zero.
            if count == 0:
                candidate = n
            # Increment count if element matches candidate; decrement otherwise.
            if n== candidate:
                count+=1
            else:
                -1
        return candidate

    # -----------------------------------------------------------------------
    # 7. Majority Element II — T2
    # Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.
    # Example: nums = [3,2,3] → [3]
    # Constraints: 1 <= nums.length <= 5 * 10^4, 10^9 <= nums[i] <= 10^9, Follow up: Could you solve the problem in linear time and in O(1) space?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def majorityElementII(self, nums: List[int]) -> List[int]:
        if not nums:
            return []
        c1 = c2 = None
        n1 = n2 = 0
        for n in nums:
            # Increment counts for matching candidates first.
            if c1 == n:
                n1 += 1
            elif c2 == n:
                n2 += 1
            # If a candidate slot is empty, adopt the current number.
            elif n1 == 0:
                c1, n1 = n, 1
            elif n2 == 0:
                c2, n2 = n, 1
            # If current element matches neither and slots are full, decrement both counters.
            else:
                n1 -= 1
                n2 -= 1
        # Verify that candidates truly appear more than n//3 times.
        return [c for c in {c1, c2} if c is not None and nums.count(c) > len(nums) // 3]

    # -----------------------------------------------------------------------
    # 8. Convert Sorted Array to BST — T2
    # Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.
    # Time: O(n), Space: O(log n)
    # -----------------------------------------------------------------------
    def sortedArrayToBST(self, nums: List[int]) -> Optional['TreeNode']:
        """Convert Sorted Array to BST: Uses divide and conquer on the sorted array."""
        def helper(l, r):
            # Base case: empty subarray.
            """Helper routine used by the enclosing solution."""
            if l > r:
                return None
            # Midpoint becomes current root.
            mid = (l + r) // 2
            root = TreeNode(nums[mid])
            # Recursively construct left and right subtrees.
            root.left = helper(l, mid - 1)
            root.right = helper(mid + 1, r)
            return root
        return helper(0, len(nums) - 1)

    # -----------------------------------------------------------------------
    # 9. Pow(x, n) — Iterative Fast Exponentiation — T2
    # Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).
    # Example: x = 2.00000, n = 10 → 1024.00000
    # Constraints: 100.0 < x < 100.0, 2^31 <= n <= 2^31-1
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def myPowIter(self, x: float, n: int) -> float:
        # Convert negative exponents to positive reciprocals.
        if n < 0:
            x, n = 1 / x, -n
        result = 1
        while n:
            # If current bit of exponent is set, multiply result by x.
            if n & 1:
                result *= x
            # Square the base.
            x *= x
            # Right shift exponent.
            n >>= 1
        return result

    # -----------------------------------------------------------------------
    # 10. Sum of Two Integers without + or - — T2
    # Given two integers a and b, return the sum of the two integers without using the operators + and -.
    # Time: O(1), Space: O(1)
    # -----------------------------------------------------------------------
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        while b:
            # Carry bits (where both bits are 1, shifted left by 1).
            carry = ((a & b) << 1) & mask
            # Sum bits without carry (XOR).
            a = (a ^ b) & mask
            # b holds the carry to be added in next iteration.
            b = carry
        # If result is negative in 32-bit signed integer format, perform sign extension.
        if a > 0x7FFFFFFF:
            a = ~(a ^ mask)
        return a


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

if __name__ == "__main__":
    def make_list(vals):
        """Builds list for tests or examples."""
        # Dummy head node
        dummy = ListNode(0)
        cur = dummy
        # Populate list nodes
        for v in vals:
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next

    def to_list(head):
        """Converts the input into list for tests or examples."""
        res = []
        # Traverse list and collect values
        while head:
            res.append(head.val)
            head = head.next
        return res

    def tree_vals_inorder(root):
        # Empty tree returns empty list
        if not root:
            return []
        # Return left subtree, root, then right subtree values
        return tree_vals_inorder(root.left) + [root.val] + tree_vals_inorder(root.right)

    sol = DivideConquerMathSolutions()

    # myPow (recursive fast exponentiation)
    # Details: Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).
    # Example 1:
    # Input: x = 2.00000, n = 10
    # Output: 1024.00000
    # Constraints:
    # - -100.0 < x < 100.0
    # - -2^31 <= n <= 2^31-1
    assert abs(sol.myPow(2.0, 10) - 1024.0) < 1e-9
    assert abs(sol.myPow(2.1, 3) - 9.261000000000001) < 1e-6
    assert abs(sol.myPow(2.0, -2) - 0.25) < 1e-9

    # maxSubArray (Kadane's)
    assert sol.maxSubArray([-2,1,-3,4,-1,2,1,-5,4]) == 6
    assert sol.maxSubArray([1]) == 1
    assert sol.maxSubArray([-1]) == -1

    # mergeKLists (divide & conquer)
    lists = [make_list([1,4,5]), make_list([1,3,4]), make_list([2,6])]
    assert to_list(sol.mergeKLists(lists)) == [1,1,2,3,4,4,5,6]
    assert sol.mergeKLists([]) is None

    # isHappy
    assert sol.isHappy(19) == True   # 19->82->68->100->1
    assert sol.isHappy(2) == False

    # reverse integer
    assert sol.reverse(123) == 321
    assert sol.reverse(-123) == -321
    assert sol.reverse(120) == 21
    assert sol.reverse(1534236469) == 0  # overflow → 0

    # majorityElement (Boyer-Moore)
    assert sol.majorityElement([3,2,3]) == 3
    assert sol.majorityElement([2,2,1,1,1,2,2]) == 2

    # majorityElementII (> n/3 elements)
    assert sorted(sol.majorityElementII([3,2,3])) == [3]
    assert sorted(sol.majorityElementII([1,1,1,3,3,2,2,2])) == [1,2]
    assert sol.majorityElementII([1,2,3]) == []

    # sortedArrayToBST (height-balanced BST)
    bst = sol.sortedArrayToBST([-10,-3,0,5,9])
    inorder = tree_vals_inorder(bst)
    assert inorder == [-10,-3,0,5,9]
    assert bst.val == 0  # mid element becomes root

    # myPowIter (iterative)
    # Details: Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).
    # Example 1:
    # Input: x = 2.00000, n = 10
    # Output: 1024.00000
    # Constraints:
    # - -100.0 < x < 100.0
    # - -2^31 <= n <= 2^31-1
    assert abs(sol.myPowIter(2.0, 10) - 1024.0) < 1e-9
    assert abs(sol.myPowIter(2.0, -2) - 0.25) < 1e-9

    # getSum (without + or -)
    assert sol.getSum(1, 2) == 3
    assert sol.getSum(-1, 1) == 0
    assert sol.getSum(-5, -3) == -8

    print("All divide & conquer / math tests passed.")
