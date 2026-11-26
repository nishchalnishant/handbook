from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Problem: Remove Nth Node From End of List
        Pattern: Two Pointers - Fixed Separation
        """
        dummy = ListNode(0, head)
        first = dummy
        second = dummy
        
        # Advance first pointer so the gap between first and second is n nodes apart
        for _ in range(n + 1):
            first = first.next
            
        # Move first to the end, maintaining the gap
        while first:
            first = first.next
            second = second.next
            
        # Second is now just before the node to delete
        second.next = second.next.next
        
        return dummy.next

# Test
if __name__ == "__main__":
    # Helper to create list [1,2,3,4,5]
    head = ListNode(1)
    curr = head
    for i in range(2, 6):
        curr.next = ListNode(i)
        curr = curr.next
        
    sol = Solution()
    new_head = sol.removeNthFromEnd(head, 2)
    
    # Print result
    res = []
    while new_head:
        res.append(new_head.val)
        new_head = new_head.next
    print(res) # Expected: [1,2,3,5]
