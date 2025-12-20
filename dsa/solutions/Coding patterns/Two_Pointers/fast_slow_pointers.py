from typing import Optional, List

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Problem: Linked List Cycle
        Pattern: Fast & Slow Pointers
        """
        if not head: return False
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    def isHappy(self, n: int) -> bool:
        """
        Problem: Happy Number
        Pattern: Fast & Slow Pointers (Cycle Detection in sequence)
        """
        def get_next(number):
            total_sum = 0
            while number > 0:
                number, digit = divmod(number, 10)
                total_sum += digit ** 2
            return total_sum

        slow, fast = n, get_next(n)
        while fast != 1 and slow != fast:
            slow = get_next(slow)
            fast = get_next(get_next(fast))
            
        return fast == 1

    def findDuplicate(self, nums: List[int]) -> int:
        """
        Problem: Find the Duplicate Number
        Pattern: Fast & Slow Pointers (Floyd's Cycle Detection on Array)
        """
        # Phase 1: Find intersection point
        slow, fast = nums[0], nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        
        # Phase 2: Find entrance to cycle (duplicate number)
        ptr1 = nums[0]
        ptr2 = slow
        while ptr1 != ptr2:
            ptr1 = nums[ptr1]
            ptr2 = nums[ptr2]
            
        return ptr1

# Test
if __name__ == "__main__":
    sol = Solution()
    print(f"Is Happy (19): {sol.isHappy(19)}") # True
    print(f"Duplicate: {sol.findDuplicate([1,3,4,2,2])}") # 2
