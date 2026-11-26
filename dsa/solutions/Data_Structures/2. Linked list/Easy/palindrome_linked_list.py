from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        Problem: Palindrome Linked List
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        slow, fast = head, head
        
        # Find middle
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
        # Reverse second half
        prev = None
        while slow:
            temp = slow.next
            slow.next = prev
            prev = slow
            slow = temp
            
        # Check palindrome
        left, right = head, prev
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        return True
