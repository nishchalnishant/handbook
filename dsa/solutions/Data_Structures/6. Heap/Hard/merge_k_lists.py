from typing import List, Optional
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Problem: Merge k Sorted Lists
        Difficulty: Hard
        Time Complexity: O(N log k)
        Space Complexity: O(k)
        """
        min_heap = []
        
        for i, l in enumerate(lists):
            if l:
                heapq.heappush(min_heap, (l.val, i, l))
                
        dummy = ListNode()
        curr = dummy
        
        while min_heap:
            val, i, node = heapq.heappop(min_heap)
            curr.next = node
            curr = curr.next
            
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))
                
        return dummy.next
