from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Problem: Swap Nodes in Pairs (Recursive)
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(n) stack
        """
        if not head or not head.next:
            return head
            
        first = head
        second = head.next
        
        first.next = self.swapPairs(second.next)
        second.next = first
        
        return second
