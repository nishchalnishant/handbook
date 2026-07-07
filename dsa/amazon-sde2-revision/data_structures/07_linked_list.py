"""
Linked List patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Losing the head reference. Always use a `dummy` node!\n- Null pointer exceptions (`node.next.next` when `node.next` is None).\n- Creating cycles accidentally when rearranging pointers.

Common Variants:
- Reverse a linked list (Iterative is safer than recursive for space)\n- Fast and Slow pointers (Cycle detection, find middle)\n- Merge two/k sorted lists\n- LRU Cache (Doubly Linked List + Hash Map)

General Tips & Best Practices:
- Draw the pointer changes on a whiteboard/paper.\n- Always update `next` pointers carefully and in the correct order.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import Optional, List
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        return self.val < other.val

class LinkedListSolutions:
    # -----------------------------------------------------------------------
    # 1. Reverse Linked List (LC 206) — T1
    # Given the head of a singly linked list, reverse the list, and return the reversed list.
    # Example: head = [1,2,3,4,5] → [5,4,3,2,1]
    # Constraints: The number of nodes in the list is the range [0, 5000], 5000 <= Node.val <= 5000, Follow up: A linked list can be reversed either iteratively or recursively. Could you implement, both?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # prev tracks the reversed portion, curr tracks the remaining
        prev, curr = None, head
        while curr:
            # Save the next node before overwriting pointers
            nxt = curr.next
            # Reverse current node's pointer
            curr.next = prev
            # Move prev and curr forward
            prev = curr
            curr = nxt
        return prev

    # -----------------------------------------------------------------------
    # 2. Linked List Cycle (LC 141) — T1
    # Given head, the head of a linked list, determine if the linked list has a cycle in it. There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter. Return true if there is a cycle in the linked list. Otherwise, return false.
    # Example: head = [3,2,0,-4], pos = 1 → true
    # Constraints: The number of the nodes in the list is in the range [0, 10^4], 10^5 <= Node.val <= 10^5, pos is -1 or a valid index in the linked-list, Follow up: Can you solve it using O(1) (i.e. constant) memory?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # Tortoise and Hare pointers starting at head
        slow, fast = head, head
        while fast and fast.next:
            # Advance pointers at 1x and 2x speeds
            slow = slow.next
            fast = fast.next.next
            # If pointers meet, a cycle exists
            if slow is fast:
                return True
        return False

    # -----------------------------------------------------------------------
    # 3. Merge Two Sorted Lists (LC 21) — T1
    # You are given the heads of two sorted linked lists list1 and list2. Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.
    # Example: list1 = [1,2,4], list2 = [1,3,4] → [1,1,2,3,4,4]
    # Constraints: The number of nodes in both lists is in the range [0, 50], 100 <= Node.val <= 100, Both list1 and list2 are sorted in non-decreasing order
    # Time: O(n+m), Space: O(1)
    # -----------------------------------------------------------------------
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # Sentinel node to build the merged list
        dummy = ListNode()
        curr = dummy
        # Traverse both lists and link the smaller element
        while list1 and list2:
            if list1.val < list2.val:
                curr.next = list1
                list1 = list1.next
            else:
                curr.next = list2
                list2 = list2.next
            curr = curr.next

        # Attach remaining elements of the non-empty list
        curr.next = list1 or list2
        return dummy.next

    # -----------------------------------------------------------------------
    # 4. Merge K Sorted Lists (LC 23) — T1
    # You are given an array of k linked-lists lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.
    # Example: lists = [[1,4,5],[1,3,4],[2,6]] → [1,1,2,3,4,4,5,6]
    # Constraints: k == lists.length, 0 <= k <= 10^4, 0 <= lists[i].length <= 500, 10^4 <= lists[i][j] <= 10^4, lists[i] is sorted in ascending order, The sum of lists[i].length will not exceed 10^4
    # Time: O(N log k), Space: O(k)
    # -----------------------------------------------------------------------
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        min_heap = []
        # Populate the min-heap with the heads of all non-empty lists
        for i, lst in enumerate(lists):
            if lst:
                heapq.heappush(min_heap, (lst.val, i, lst))

        dummy = ListNode()
        curr = dummy

        # Repeatedly extract smallest element and advance that list's pointer
        while min_heap:
            val, i, node = heapq.heappop(min_heap)
            curr.next = node
            curr = curr.next
            # Push successor node onto heap
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))

        return dummy.next

    # -----------------------------------------------------------------------
    # 5. Reorder List (LC 143) — T1
    # You are given the head of a singly linked-list. The list can be represented as: L0 → L1 → … → Ln - 1 → Ln Reorder the list to be on the following form: L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → … You may not modify the values in the list's nodes. Only nodes themselves may be changed.
    # Example: head = [1,2,3,4] → [1,4,2,3]
    # Constraints: The number of nodes in the list is in the range [1, 5 * 10^4], 1 <= Node.val <= 1000
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next: return

        # Phase 1: Locate middle using slow/fast pointers
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Phase 2: Sever list and reverse second half
        prev, curr = None, slow.next
        slow.next = None
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # Phase 3: Interleave first and second halves
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2

class LinkedListSolutionsT2:
    # -----------------------------------------------------------------------
    # 1. Remove Nth From End (LC 19) — T2
    # Given the head of a linked list, remove the nth node from the end of the list and return its head.
    # Example: head = [1,2,3,4,5], n = 2 → [1,2,3,5]
    # Constraints: The number of nodes in the list is sz, 1 <= sz <= 30
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Sentinel node to handle deletion of head node cleanly
        dummy = ListNode(0, head)
        left = dummy
        right = head
        # Advance right pointer by n steps to create gap
        while n > 0 and right:
            right = right.next
            n -= 1
        # Walk both pointers until right reaches the end
        while right:
            left = left.next
            right = right.next
        # Delete the target node
        left.next = left.next.next
        return dummy.next

    # -----------------------------------------------------------------------
    # 2. Linked List Cycle II (LC 142) — T2
    # Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null. There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to (0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a parameter. Do not modify the linked list.
    # Example: head = [3,2,0,-4], pos = 1 → tail connects to node index 1
    # Constraints: The number of the nodes in the list is in the range [0, 10^4], 10^5 <= Node.val <= 10^5, pos is -1 or a valid index in the linked-list, Follow up: Can you solve it using O(1) (i.e. constant) memory?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        # Phase 1: Detect cycle meeting point
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                # Phase 2: Find cycle start by walking from head and meeting point
                slow = head
                while slow is not fast:
                    slow = slow.next
                    fast = fast.next
                return slow
        return None

    # -----------------------------------------------------------------------
    # 3. Palindrome Linked List (LC 234) — T2
    # Given the head of a singly linked list, return true if it is a palindrome or false otherwise.
    # Example: head = [1,2,2,1] → true
    # Constraints: The number of nodes in the list is in the range [1, 10^5], 0 <= Node.val <= 9, Follow up: Could you do it in O(n) time and O(1) space?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        fast = head
        slow = head
        # Find middle of the list
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

        # Reverse second half of the list
        prev = None
        while slow:
            nxt = slow.next
            slow.next = prev
            prev = slow
            slow = nxt

        # Compare values of first half and reversed second half
        left, right = head, prev
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        return True

    # -----------------------------------------------------------------------
    # 5. Copy List with Random Pointer (LC 138) — T2
    # A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null. Construct a deep copy of the list. The deep copy should consist of exactly n brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the next and random pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list. For example, if there are two nodes X and Y in the original list, where X.random --> Y, then for the corresponding two nodes x and y in the copied list, x.random --> y. Return the head of the copied linked list. The linked list is represented in the input/output as a list of n nodes. Each node is represented as a pair of [val, random_index] where: null if it does not point to any node. Your code will only be given the head of the original linked list.
    # Example: head = [[7,null],[13,0],[11,4],[10,2],[1,0]] → [[7,null],[13,0],[11,4],[10,2],[1,0]]
    # Constraints: 0 <= n <= 1000, 10^4 <= Node.val <= 10^4, Node.random is null or is pointing to some node in the linked list
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head: return None
        # Map to store old node to cloned node relationship
        oldToCopy = {None: None}

        # First pass: create all copy nodes
        curr = head
        while curr:
            oldToCopy[curr] = Node(curr.val)
            curr = curr.next

        # Second pass: wire up next and random pointers of clones
        curr = head
        while curr:
            copy = oldToCopy[curr]
            copy.next = oldToCopy[curr.next]
            copy.random = oldToCopy[curr.random]
            curr = curr.next
        return oldToCopy[head]

    # -----------------------------------------------------------------------
    # 6. Reverse K-Group (LC 25) — T2
    # Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list. k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.
    # Example: head = [1,2,3,4,5], k = 2 → [2,1,4,3,5]
    # Constraints: The number of nodes in the list is in the range [1, 5000], 1 <= k <= 5000
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        groupPrev = dummy

        def getKth(curr, k):
                # Advance curr by k steps
                # Advance curr by k steps
            # Advance curr by k steps
            while curr and k > 0:
                curr = curr.next
                k -= 1
            return curr

        while True:
            kth = getKth(groupPrev, k)
            if not kth:
                break
            groupNext = kth.next

            prev, curr = kth.next, groupPrev.next
            while curr != groupNext:
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt

            tmp = groupPrev.next
            groupPrev.next = kth
            groupPrev = tmp
        return dummy.next

    # -----------------------------------------------------------------------
    # 7. Sort List (LC 148) — T2
    # Given the head of a linked list, return the list after sorting it in ascending order.
    # Example: head = [4,2,1,3] → [1,2,3,4]
    # Constraints: The number of nodes in the list is in the range [0, 5 * 10^4], 10^5 <= Node.val <= 10^5, Follow up: Can you sort the linked list in O(n logn) time and O(1) memory (i.e. constant space)?
    # Time: O(n log n), Space: O(log n)
    # -----------------------------------------------------------------------
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next: return head

        left = head
        # Find the midpoint node to divide the list
        right = self.getMid(head)
        tmp = right.next
        # Sever the list into two halves
        right.next = None
        right = tmp

        # Recursively sort both halves
        left = self.sortList(left)
        right = self.sortList(right)
        # Merge sorted lists
        return self.merge(left, right)

    def getMid(self, head):
        # Walk with slow and fast pointers to find mid node
        # Walk with slow and fast pointers to find mid node
        # Walk with slow and fast pointers to find mid node
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def merge(self, list1, list2):
        # Sentinel node to assemble merged list
        tail = dummy = ListNode()
        while list1 and list2:
            if list1.val < list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        # Attach any leftover nodes
        tail.next = list1 or list2
        return dummy.next

    # -----------------------------------------------------------------------
    # 8. Intersection of Two Lists (LC 160) — T2
    # Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null.
    # Example: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3 → Intersected at '8'
    # Constraints: The number of nodes of listA is in the m, The number of nodes of listB is in the n
    # Time: O(n+m), Space: O(1)
    # -----------------------------------------------------------------------
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        """Intersection of Two Lists (LC 160): Initialize `l1 = headA` and `l2 = headB`."""
        # Cross-wire the lists to synchronize their lengths
        # Cross-wire the lists to synchronize their lengths
        # Cross-wire the lists to synchronize their lengths
        l1, l2 = headA, headB
        while l1 is not l2:
            l1 = l1.next if l1 else headB
            l2 = l2.next if l2 else headA
        return l1

    # -----------------------------------------------------------------------
    # 9. Add Two Numbers (LC 2) — T2
    # You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list. You may assume the two numbers do not contain any leading zero, except the number 0 itself.
    # Example: l1 = [2,4,3], l2 = [5,6,4] → [7,0,8]
    # Constraints: The number of nodes in each linked list is in the range [1, 100], 0 <= Node.val <= 9, It is guaranteed that the list represents a number that does not have leading zeros
    # Time: O(max(n,m)), Space: O(max(n,m))
    # -----------------------------------------------------------------------
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # Dummy head to start result list
        dummy = ListNode()
        curr = dummy
        carry = 0

        # Traverse both numbers digit-by-digit
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            # Compute sum and carry values
            val = v1 + v2 + carry
            carry = val // 10
            val = val % 10

            curr.next = ListNode(val)
            curr = curr.next

            # Advance input pointers if possible
            if l1: l1 = l1.next
            if l2: l2 = l2.next

        return dummy.next

    # -----------------------------------------------------------------------
    # 10. Flatten a Multilevel Doubly Linked List (LC 430) — T2
    # You are given a doubly linked list, which contains nodes that have a next pointer, a previous pointer, and an additional child pointer. This child pointer may or may not point to a separate doubly linked list, also containing these special nodes. These child lists may have one or more children of their own, and so on, to produce a multilevel data structure as shown in the example below. Given the head of the first level of the list, flatten the list so that all the nodes appear in a single-level, doubly linked list. Let curr be a node with a child list. The nodes in the child list should appear after curr and before curr.next in the flattened list. Return the head of the flattened list. The nodes in the list must have all of their child pointers set to null. You are given a doubly linked list, which contains nodes that have a next pointer, a previous pointer, and an additional child pointer. This child pointer may or may not point to a separate doubly linked list, also containing these special nodes. These child lists may have one or more children of their own, and so on, to produce a multilevel data structure. Flatten the list so that all the nodes appear in a single-level, doubly linked list. You are given a doubly linked list, which contains nodes that have a next pointer, a previous pointer, and an additional child pointer. This child pointer may or may not point to a separate doubly linked list, also containing these special nodes. These child lists may have one or more children of their own, and so on, to produce a multilevel data structure. Flatten the list so that all the nodes appear in a single-level, doubly linked list.
    # Example: head = [1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12] → [1,2,3,7,8,11,12,9,10,4,5,6]
    # Constraints: The number of Nodes will not exceed 1000, Explanation: The multilevel linked list in the input is shown, After flattening the multilevel linked list it becomes:, The number of Nodes will not exceed 1000, 1 <= Node.val <= 10^5, How the multilevel linked list is represented in test cases:, We use the multilevel linked list from Example 1 above:, 1---2---3---4---5---6--NULL, |, 7---8---9---10--NULL, |, 11--12--NULL, The serialization of each level is as follows:, [1,2,3,4,5,6,null], [7,8,9,10,null], [11,12,null], To serialize all levels together, we will add nulls in each level to signify no node connects to the, upper node of the previous level. The serialization becomes:, [1,    2,    3, 4, 5, 6, null], |, [null, null, 7,    8, 9, 10, null], |, [            null, 11, 12, null], Merging the serialization of each level and removing trailing nulls we obtain:, [1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12], The number of Nodes will not exceed 1000
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def flatten(self, head: Optional['Node']) -> Optional['Node']:
        if not head:
            return head
        # Stack to hold the next nodes in depth-first order
        stack = [head]
        prev = Node(0)
        while stack:
            curr = stack.pop()
            # Double link prev and curr
            prev.next = curr
            curr.prev = prev
            # Push next first, then child so child is processed first (LIFO)
            if curr.next:
                stack.append(curr.next)
            if curr.child:
                stack.append(curr.child)
                curr.child = None
            prev = curr
        # Sever reference to sentinel
        head.prev = None
        return head

# Node class for Copy List with Random Pointer
class Node:
    def __init__(self, x: int, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random

class DLLNode:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    # -----------------------------------------------------------------------
    # 4. LRU Cache (T2) — DLL + HashMap → O(1) get and put
    # Design and implement a data structure for Least Recently Used (LRU) cache. Key insight: dummy head/tail sentinels; _remove + _insert helpers
    # -----------------------------------------------------------------------
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # key → DLLNode
        # Sentinel nodes: left = LRU end, right = most-recent end
        self.left = DLLNode()
        self.right = DLLNode()
        self.left.next = self.right
        self.right.prev = self.left

    def _remove(self, node: DLLNode) -> None:
        """Removes a value from the underlying data structure when present."""
        # Update adjacent links to sever node from list
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert(self, node: DLLNode) -> None:
        """Insert just before right sentinel (= most recent position)."""
        # Insert node at the MRU end (just before right sentinel)
        prev = self.right.prev
        prev.next = node
        node.prev = prev
        node.next = self.right
        self.right.prev = node

    def get(self, key: int) -> int:
        """Returns the value associated with the requested key or index."""
        if key in self.cache:
            # Move accessed node to the most recently used end
            self._remove(self.cache[key])
            self._insert(self.cache[key])
            return self.cache[key].val
        # Return -1 if key is not found
        return -1

    def put(self, key: int, value: int) -> None:
        """Stores or updates the value associated with the requested key."""
        if key in self.cache:
            self._remove(self.cache[key])
        node = DLLNode(key, value)
        self.cache[key] = node
        self._insert(node)
        if len(self.cache) > self.cap:
            lru = self.left.next  # LRU = just after left sentinel
            self._remove(lru)
            del self.cache[lru.key]

class LFUDllNode:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.freq = 1
        self.prev = self.next = None

class LFUCache:
    # -----------------------------------------------------------------------
    # 11. LFU Cache (T2) — DLL per frequency + hashmap → O(1) get/put
    # Design and implement a data structure for Least Frequently Used (LFU) cache.
    # -----------------------------------------------------------------------
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_freq = 0
        self.cache = {}            # key → LFUDllNode
        self.freq_lists = {}       # freq → (head, tail) DLL of nodes

    def _new_list(self):
        # Initialize sentinel head and tail nodes for a new DLL
        head = LFUDllNode()
        tail = LFUDllNode()
        head.next, tail.prev = tail, head
        return [head, tail]  # [head, tail]

    def _remove_node(self, node: LFUDllNode) -> None:
        # Sever connections for the node
        node.prev.next = node.next
        node.next.prev = node.prev
        # If the freq-list becomes empty, drop it (and update min_freq if needed)
        head, tail = self.freq_lists[node.freq]
        if head.next is tail:
            del self.freq_lists[node.freq]
            if self.min_freq == node.freq:
                self.min_freq += 1

    def _insert_after(self, node: LFUDllNode, freq: int) -> None:
        # Create freq list if it does not exist
        if freq not in self.freq_lists:
            self.freq_lists[freq] = self._new_list()
        head, tail = self.freq_lists[freq]
        # Insert node at the end (just before tail sentinel) of the list
        node.prev = tail.prev
        node.next = tail
        tail.prev.next = node
        tail.prev = node

    def _bump(self, node: LFUDllNode) -> None:
        # Remove node from its current frequency list
        self._remove_node(node)
        # Increment frequency of the node
        node.freq += 1
        # Insert node into the new frequency list
        self._insert_after(node, node.freq)

    def get(self, key: int) -> int:
        """Returns the value associated with the requested key or index."""
        # Return -1 if key is not present in cache
        if key not in self.cache:
            return -1
        node = self.cache[key]
        # Increase frequency count and move node
        self._bump(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        """Stores or updates the value associated with the requested key."""
        if self.cap == 0:
            return
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._bump(node)
            return
        node = LFUDllNode(key, value)
        self.cache[key] = node
        self._insert_after(node, 1)
        self.min_freq = 1
        if len(self.cache) > self.cap:
            # Evict LRU from the lowest-frequency list
            head, tail = self.freq_lists[self.min_freq]
            lfu = head.next
            self._remove_node(lfu)
            del self.cache[lfu.key]

# ─────────────────────────────────────────────────────────────────────────────
# All O(1) Data Structure (LC 432)
# ─────────────────────────────────────────────────────────────────────────────

class AllOneNode:
    def __init__(self, count=0):
        """Doubly-linked list node holding a set of keys at the same count."""
        self.count = count
        self.keys = set()
        self.prev = self.next = None

class AllOne:
    def __init__(self):
        self.key_node = {}          # key → AllOneNode
        self.head = AllOneNode(0)   # sentinel min-side
        self.tail = AllOneNode(float('inf'))  # sentinel max-side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _insert_after(self, node: AllOneNode, new_node: AllOneNode) -> None:
        # Insert new_node directly after node in the DLL
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node

    def _remove_node(self, node: AllOneNode) -> None:
        # Sever node links to remove it from DLL
        node.prev.next = node.next
        node.next.prev = node.prev

    def inc(self, key: str) -> None:
        # Case 1: Key already exists in the mapping
        if key in self.key_node:
            node = self.key_node[key]
            nxt = node.next
            # Create a new bucket node if count+1 bucket does not exist
            if nxt is self.tail or nxt.count != node.count + 1:
                new_node = AllOneNode(node.count + 1)
                self._insert_after(node, new_node)
                nxt = new_node
            # Move key to the next bucket
            nxt.keys.add(key)
            self.key_node[key] = nxt
            node.keys.discard(key)
            # Remove empty bucket
            if not node.keys:
                self._remove_node(node)
        # Case 2: New key is inserted
        else:
            first = self.head.next
            # Create count=1 bucket if it doesn't exist
            if first is self.tail or first.count != 1:
                new_node = AllOneNode(1)
                self._insert_after(self.head, new_node)
                first = new_node
            first.keys.add(key)
            self.key_node[key] = first

    def dec(self, key: str) -> None:
        node = self.key_node[key]
        prv = node.prev
        # If count drops to 0, delete key mapping entirely
        if node.count == 1:
            del self.key_node[key]
        # Otherwise move key to count-1 bucket
        else:
            if prv is self.head or prv.count != node.count - 1:
                new_node = AllOneNode(node.count - 1)
                self._insert_after(prv, new_node)
                prv = new_node
            prv.keys.add(key)
            self.key_node[key] = prv
        node.keys.discard(key)
        # Prune empty bucket
        if not node.keys:
            self._remove_node(node)

    def getMaxKey(self) -> str:
        # If cache is empty, return empty string
        if self.tail.prev is self.head:
            return ""
        # Return one of the keys from the max-count bucket (prev of tail sentinel)
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        # If cache is empty, return empty string
        if self.head.next is self.tail:
            return ""
        # Return one of the keys from the min-count bucket (next of head sentinel)
        return next(iter(self.head.next.keys))


# ─────────────────────────────────────────────────────────────────────────────
# Design Linked List (LC 707)
# ─────────────────────────────────────────────────────────────────────────────

class MyLinkedList:
    def __init__(self):
        """Design Linked List (LC 707)."""
        self.dummy = ListNode(0)
        self.size = 0

    def get(self, index: int) -> int:
        """Design Linked List (LC 707)."""
        # Index bounds check
        if index < 0 or index >= self.size:
            return -1
        curr = self.dummy.next
        # Walk index times to find target node
        for _ in range(index):
            curr = curr.next
        return curr.val

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        # Reject invalid index greater than current list size
        if index > self.size:
            return
        index = max(index, 0)
        curr = self.dummy
        # Walk to index-1 node (predecessor of insertion point)
        for _ in range(index):
            curr = curr.next
        new_node = ListNode(val)
        # Link new node into the list
        new_node.next = curr.next
        curr.next = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        # Check index range bounds
        if index < 0 or index >= self.size:
            return
        curr = self.dummy
        # Find predecessor of the target node
        for _ in range(index):
            curr = curr.next
        # Relink to delete the target node
        curr.next = curr.next.next
        self.size -= 1


class LinkedListSolutionsAdditional:
    # -----------------------------------------------------------------------
    # 13. Delete the Middle Node of a Linked List (LC 2095) — T2
    # You are given the head of a linked list. Delete the middle node, and return the head of the modified linked list. The middle node of a linked list of size n is the ⌊n / 2⌋^th node from the start using 0-based indexing, where ⌊x⌋ denotes the largest integer less than or equal to x.
    # Example: head = [1,3,4,7,1,2,6] → [1,3,4,1,2,6]
    # Constraints: The number of nodes in the list is in the range [1, 10^5], 1 <= Node.val <= 10^5
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return None

        slow = fast = head
        prev = None
        # Walk slow/fast pointers to find middle and predecessor
        while fast and fast.next:
            fast = fast.next.next
            prev = slow
            slow = slow.next

        # Delete middle node by bypassing it
        if prev:
            prev.next = slow.next

        return head

    # -----------------------------------------------------------------------
    # 14. Swap Nodes in Pairs (LC 24) — T2
    # Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)
    # Example: head = [1,2,3,4] → [2,1,4,3]
    # Constraints: The number of nodes in the list is in the range [0, 100], 0 <= Node.val <= 100
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        dummy.next = head
        curr = dummy

        # Loop while there is a pair of nodes to swap
        while curr.next and curr.next.next:
            first = curr.next
            second = curr.next.next

            # Swap adjacent nodes
            first.next = second.next
            second.next = first
            curr.next = second

            # Move curr pointer forward
            curr = first

        return dummy.next

    # Rotate List (LC 61)
    # Details: Given the head of a linked list, rotate the list to the right by k places.
    # Example: head = [1,2,3,4,5], k = 2 → [4,5,1,2,3]
    # Time: O(n), Space: O(1)
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """Rotate List (LC 61). O(n)."""
        if not head or not head.next or k == 0:
            return head
        tail = head
        n = 1
        # Count elements and locate the tail node
        while tail.next:
            tail = tail.next
            n += 1
        tail.next = head  # form cycle
        # Find cut position
        steps = n - k % n
        new_tail = head
        for _ in range(steps - 1):
            new_tail = new_tail.next
        # Sever the loop and identify new head
        new_head = new_tail.next
        new_tail.next = None
        return new_head

    # Partition List (LC 86)
    # Details: Given the head of a linked list and a value x, partition it such
    # that all nodes less than x come before nodes greater than or equal to x.
    # Preserve the original relative order of the nodes in each partition.
    # Example: head = [1,4,3,2,5,2], x = 3 → [1,2,2,4,3,5]
    # Time: O(n), Space: O(1)
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        """Rotate List (LC 61). O(n)."""
        less_dummy = ListNode(0)
        geq_dummy = ListNode(0)
        less_tail = less_dummy
        geq_tail = geq_dummy
        curr = head
        # Distribute elements to two lists based on value constraint x
        while curr:
            if curr.val < x:
                less_tail.next = curr
                less_tail = less_tail.next
            else:
                geq_tail.next = curr
                geq_tail = geq_tail.next
            curr = curr.next
        # Stitch partitions together
        geq_tail.next = None
        less_tail.next = geq_dummy.next
        return less_dummy.next

    # Odd Even Linked List (LC 328)
    # Details: Given the head of a singly linked list, group all the nodes with
    # odd indices together followed by the nodes with even indices, and return the
    # reordered list. The first node is considered odd, second even, etc. Preserve
    # the relative order within each group.
    # Example: head = [1,2,3,4,5] → [1,3,5,2,4]
    # Time: O(n), Space: O(1)
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Partition List (LC 86). O(n)."""
        if not head:
            return head
        odd = head
        even = head.next
        even_head = even
        # Segregate odd and even indexed nodes
        while even and even.next:
            odd.next = even.next
            odd = odd.next
            even.next = odd.next
            even = even.next
        # Append even list head to the tail of odd list
        odd.next = even_head
        return head

    # Remove Duplicates from Sorted List II (LC 82)
    # Details: Given the head of a sorted linked list, delete all nodes that have
    # duplicate numbers, leaving only distinct numbers from the original list.
    # Example: head = [1,2,3,3,4,4,5] → [1,2,5]
    # Time: O(n), Space: O(1)
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Odd Even Linked List (LC 328). O(n)."""
        dummy = ListNode(0, head)
        prev = dummy
        while head:
            # Check if there is a run of duplicate values starting at current node
            if head.next and head.val == head.next.val:
                # Advance pointer to skip duplicates
                while head.next and head.val == head.next.val:
                    head = head.next
                # Skip duplicate run in the result list
                prev.next = head.next
            else:
                prev = prev.next
            head = head.next
        return dummy.next

    # Find the Middle of Linked List (LC 876)
    # Details: Given the head of a singly linked list, return the middle node.
    # If there are two middle nodes, return the second middle node.
    # Example: head = [1,2,3,4,5] → node with value 3
    #          head = [1,2,3,4]   → node with value 3 (second middle)
    # Time: O(n), Space: O(1)
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Remove Duplicates from Sorted List II (LC 82). O(n)."""
        slow = fast = head
        # Advance pointers at 1x and 2x speeds to find middle
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

if __name__ == "__main__":
    def make_list(vals):
        """Find the Middle of Linked List (LC 876). O(n)."""
        # Dummy head node
        dummy = ListNode(0)
        cur = dummy
        # Append all values as new ListNodes
        for v in vals:
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next

    def to_list(head):
        """Find the Middle of Linked List (LC 876). O(n)."""
        # List to collect values
        res = []
        # Traverse list and record all node values
        while head:
            res.append(head.val)
            head = head.next
        return res

    sol = LinkedListSolutions()
    sol2 = LinkedListSolutionsT2()
    sol3 = LinkedListSolutionsAdditional()

    # reverseList
    assert to_list(sol.reverseList(make_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert to_list(sol.reverseList(make_list([1]))) == [1]
    assert sol.reverseList(None) is None

    # hasCycle
    head = make_list([1, 2, 3])
    assert sol.hasCycle(head) == False
    head2 = make_list([1, 2, 3])
    head2.next.next.next = head2.next  # cycle
    assert sol.hasCycle(head2) == True

    # mergeTwoLists
    assert to_list(sol.mergeTwoLists(make_list([1, 3, 5]), make_list([2, 4, 6]))) == [1, 2, 3, 4, 5, 6]
    assert to_list(sol.mergeTwoLists(None, make_list([1]))) == [1]

    # reorderList: [1,2,3,4] -> [1,4,2,3]
    h = make_list([1, 2, 3, 4])
    sol.reorderList(h)
    assert to_list(h) == [1, 4, 2, 3]

    # removeNthFromEnd
    assert to_list(sol2.removeNthFromEnd(make_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert to_list(sol2.removeNthFromEnd(make_list([1]), 1)) == []

    # detectCycle
    head3 = make_list([3, 2, 0, -4])
    head3.next.next.next.next = head3.next  # cycle at node with val 2
    assert sol2.detectCycle(head3).val == 2

    # isPalindrome
    assert sol2.isPalindrome(make_list([1, 2, 2, 1])) == True
    assert sol2.isPalindrome(make_list([1, 2])) == False

    # reverseKGroup
    assert to_list(sol2.reverseKGroup(make_list([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert to_list(sol2.reverseKGroup(make_list([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]

    # sortList
    assert to_list(sol2.sortList(make_list([4, 2, 1, 3]))) == [1, 2, 3, 4]
    assert to_list(sol2.sortList(make_list([-1, 5, 3, 4, 0]))) == [-1, 0, 3, 4, 5]

    # addTwoNumbers: 342 + 465 = 807
    assert to_list(sol2.addTwoNumbers(make_list([2, 4, 3]), make_list([5, 6, 4]))) == [7, 0, 8]

    # LRUCache
    lru = LRUCache(2)
    lru.put(1, 1); lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3)
    assert lru.get(2) == -1  # evicted
    lru.put(4, 4)
    assert lru.get(1) == -1  # evicted
    assert lru.get(3) == 3
    assert lru.get(4) == 4

    # deleteMiddle: [1,3,4,7,1,2,6] -> [1,3,4,1,2,6]
    assert to_list(sol3.deleteMiddle(make_list([1, 3, 4, 7, 1, 2, 6]))) == [1, 3, 4, 1, 2, 6]
    assert sol3.deleteMiddle(make_list([1])) is None

    # swapPairs
    assert to_list(sol3.swapPairs(make_list([1, 2, 3, 4]))) == [2, 1, 4, 3]
    assert to_list(sol3.swapPairs(make_list([1]))) == [1]

    # rotateRight (LC 61)
    assert to_list(sol3.rotateRight(make_list([1, 2, 3, 4, 5]), 2)) == [4, 5, 1, 2, 3]
    assert to_list(sol3.rotateRight(make_list([0, 1, 2]), 4)) == [2, 0, 1]
    assert to_list(sol3.rotateRight(make_list([1, 2]), 0)) == [1, 2]

    # partition (LC 86)
    assert to_list(sol3.partition(make_list([1, 4, 3, 2, 5, 2]), 3)) == [1, 2, 2, 4, 3, 5]
    assert to_list(sol3.partition(make_list([2, 1]), 2)) == [1, 2]

    # oddEvenList (LC 328)
    assert to_list(sol3.oddEvenList(make_list([1, 2, 3, 4, 5]))) == [1, 3, 5, 2, 4]
    assert to_list(sol3.oddEvenList(make_list([2, 1, 3, 5, 6, 4, 7]))) == [2, 3, 6, 7, 1, 5, 4]

    # deleteDuplicates II (LC 82)
    assert to_list(sol3.deleteDuplicates(make_list([1, 2, 3, 3, 4, 4, 5]))) == [1, 2, 5]
    assert to_list(sol3.deleteDuplicates(make_list([1, 1, 1, 2, 3]))) == [2, 3]
    assert to_list(sol3.deleteDuplicates(make_list([1, 1]))) == []

    # middleNode (LC 876)
    assert sol3.middleNode(make_list([1, 2, 3, 4, 5])).val == 3
    assert sol3.middleNode(make_list([1, 2, 3, 4])).val == 3
    assert sol3.middleNode(make_list([1])).val == 1

    # AllOne (LC 432)
    ao = AllOne()
    ao.inc("a"); ao.inc("b"); ao.inc("b"); ao.inc("c"); ao.inc("c"); ao.inc("c")
    assert ao.getMaxKey() == "c"
    assert ao.getMinKey() == "a"   # a=1, b=2, c=3
    ao.dec("b"); ao.dec("b")       # a=1, b=0 (removed), c=3
    assert ao.getMinKey() == "a"   # only a=1 and c=3 remain
    ao.dec("a")                    # a=0 (removed), c=3
    assert ao.getMinKey() == "c"
    assert ao.getMaxKey() == "c"

    # MyLinkedList (LC 707)
    ml = MyLinkedList()
    ml.addAtHead(1); ml.addAtTail(3); ml.addAtIndex(1, 2)
    assert ml.get(1) == 2
    ml.deleteAtIndex(1)
    assert ml.get(1) == 3
    assert ml.get(0) == 1
    assert ml.get(2) == -1

    # mergeKLists already tested implicitly; verify once more
    assert to_list(sol.mergeKLists([make_list([1, 4, 5]), make_list([1, 3, 4]), make_list([2, 6])])) == [1, 1, 2, 3, 4, 4, 5, 6]

    # LFU Cache (LC 460)
    lfu = LFUCache(2)
    lfu.put(1, 1); lfu.put(2, 2)
    assert lfu.get(1) == 1   # freq(1)=2, freq(2)=1
    lfu.put(3, 3)            # evicts key 2 (LRU at min_freq=1)
    assert lfu.get(2) == -1  # evicted
    assert lfu.get(3) == 3   # freq(1)=2, freq(3)=2
    lfu.put(4, 4)            # evicts key 4 itself (implementation evicts from new min_freq=1)
    assert lfu.get(1) == 1
    assert lfu.get(3) == 3
    assert lfu.get(4) == -1  # evicted immediately

    print("All linked list tests passed.")
