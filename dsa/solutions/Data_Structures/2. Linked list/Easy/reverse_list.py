from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Problem: Reverse Linked List
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        prev, curr = None, head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

# Test
if __name__ == "__main__":
    # Create 1->2->3
    head = ListNode(1, ListNode(2, ListNode(3)))
    sol = Solution()
    new_head = sol.reverseList(head)
    # Output reversed
    curr = new_head
    while curr:
        print(curr.val, end=" ") # 3 2 1 
        curr = curr.next
