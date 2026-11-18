---
tags: [coding, data-structures, linked-list]
topic: linked-list
difficulty: mixed
---
# Linked List — Problem Deep Dives

## What this covers

> [!abstract] In this file
> **Covers:** Worked linked-list problems: reversal, fast/slow, cycle detection, merge/sort, copy, LRU design.
> **You'll be able to:** Do pointer surgery without losing nodes; dry-run on 0/1/2-node lists.
> **Prereqs:** Linked list lecture · **Pair with:** [Linked list lecture](../../02-data-structures/07-linked-list.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [In-Place Reversal](#in-place-reversal) · [Fast / Slow Pointers](#fast--slow-pointers) · [Floyd's Cycle Detection](#floyds-cycle-detection) · [Merge / Sorting](#merge--sorting) · [Copy / Design](#copy--design) · [Other Manipulation](#other-manipulation)

> [!tip] If you only have 20 minutes
> **Do these first:** [Reverse Linked List](#reverse-linked-list--t2) · [Merge Two Sorted Lists](#merge-two-sorted-lists--t2) · [Linked List Cycle II](#linked-list-cycle-ii--t2) · [Remove Nth Node From End of List](#remove-nth-node-from-end-of-list--t2) · [Reorder List](#reorder-list--t2) · [Copy List with Random Pointer](#copy-list-with-random-pointer--t2) · [LRU Cache](#lru-cache--t2) · [Reverse Nodes in K-Group](#reverse-nodes-in-k-group--t2)
> **Template:** Reverse: `prev, cur = None, head; while cur: cur.next, prev, cur = prev, cur, cur.next`.
> **Template:** Dummy head whenever the head can change; fast/slow for middle (`while fast and fast.next`).
> **Gotchas:** Save `next` before rewiring · cycle start: reset one pointer to head after meeting, move both by 1 · Nth from end: advance fast `n+1` from dummy · LRU: dict maps key → node, never key → value.

---

**Core invariants to internalize:**
- Singly linked: each node holds `val` + `next`. No backward traversal.
- Doubly linked: each node holds `val` + `next` + `prev`.
- The dummy/sentinel head eliminates edge cases on head deletion/insertion.
- Two-pointer (slow/fast) detects cycles and finds midpoints in O(n) / O(1) space.
- Floyd's algorithm: if fast meets slow inside cycle, resetting one pointer to head and stepping both at speed 1 lands them at the cycle entry.

**Interview patterns to recognize quickly:**
- Dummy node + pointer relinks for head-safe insertion/deletion.
- Slow/fast pointers for cycle detection, middle finding, and end-relative deletes.
- Reverse-then-merge for palindrome, reorder, and k-group style problems.
- Hash map + list node pairs for random pointers and LRU caches.
- Heap for merging multiple sorted lists.

**Edge cases to sanity-check:**
- Empty list, one node, and two nodes.
- Head changes after deletion/reversal.
- Odd vs even length when finding the middle.
- `k = 1`, `k > length`, or `left == right`.
- Cycles absent vs present; duplicate values vs duplicate nodes.

---

## In-Place Reversal

---

### Reverse Linked List `🎯 T2`

> [!example] Problem
> Given the head of a singly linked list, reverse the list, and return the reversed list.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5]
> Output: [5,4,3,2,1]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2]
> Output: [2,1]
> ```
> 
> **Example 3:**
> ```
> Input: head = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the list is the range [0, 5000].
> - -5000 <= Node.val <= 5000

> [!tip] Recognize · Gotcha
> **Signal:** Pointer rewiring · **Gotcha:** **Recursive** uses O(n) stack; **null** head.

> [!info] Approach
> **Three-pointer iterative reversal.** We cannot reverse without visiting every node. The question is whether we need O(n) space (recursion stack) or O(1). Iteratively reversing edges is O(1) space. Three-pointer technique maintaining invariant: `prev` is the fully-reversed prefix, `curr` is the unprocessed suffix head. Save `nxt = curr.next` before overwriting. Set `curr.next = prev`. Advance `prev = curr`, `curr = nxt`. When `curr` is None, `prev` is the new head. Watch the order carefully: save `next` before rewiring or you lose the rest of the list.

> [!note]- Python Solution
> ```python
> from typing import Optional
> 
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val
>         self.next = next
> 
> def reverse_list(head):
>     prev, curr = None, head
>     while curr:
>         nxt = curr.next       # save before overwriting
>         curr.next = prev      # reverse edge
>         prev, curr = curr, nxt
>     return prev  # prev is the new head
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Recursive: elegant but O(n) call stack. `reverse(head.next)` then `head.next.next = head; head.next = None; return new_head`. Stack overflow risk on large n.

---

### Reverse Linked List II `🎯 T2`

> [!example] Problem
> Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], left = 2, right = 4
> Output: [1,4,3,2,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [5], left = 1, right = 1
> Output: [5]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is n.
> - 1 <= n <= 500
> - -500 <= Node.val <= 500
> - 1 <= left <= right <= n

> [!info] Approach
> **Find pre-node + in-place splice-reversal.** We need to splice a reversed sublist back into the outer list. A dummy node handles the case where `left == 1` (head changes). Find `pre` (node before position `left`). Then run `right - left` iterations of in-place splice-reversal. Each iteration: save `nxt = curr.next`, detach `nxt` from its position, reattach it after `pre`. This inserts nodes one by one at the front of the reversed section. After `right - left` iterations, the segment is reversed. If `left == right`, the loop runs zero times and the list stays unchanged.

> [!note]- Python Solution
> ```python
> def reverse_between(head, left, right):
>     dummy = ListNode(0, head)
>     pre = dummy
>     for _ in range(left - 1):
>         pre = pre.next
>     curr = pre.next
>     for _ in range(right - left):
>         nxt = curr.next
>         curr.next = nxt.next
>         nxt.next = pre.next
>         pre.next = nxt
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Collect sublist values, reverse them, overwrite: O(n) time, O(right-left) space. Simpler but uses extra space.
> - Full reversal then splice: two-pass; same complexity, more code.

---

### Palindrome Linked List `🎯 T2`

> [!example] Problem
> Given the head of a singly linked list, return true if it is a palindrome or false otherwise.
> 
> **Example 1:**
> ```
> Input: head = [1,2,2,1]
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2]
> Output: false
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [1, 10^5].
> - 0 <= Node.val <= 9

> [!info] Approach
> **Find middle + reverse second half + compare.** Arrays allow index-based palindrome check in O(1) space. Linked lists don't. The trick: reverse the second half in-place and compare. Three-step: find middle (slow/fast pointers), skip the exact middle on odd-length lists, reverse second half, compare both halves node-by-node. Slow/fast to find middle. If the list has odd length, advance `slow` one more step to skip the middle node. Reverse from that point onward. Walk two pointers — one from `head`, one from reversed head — checking values. Restore (optional): reverse second half back.

> [!note]- Python Solution
> ```python
> def is_palindrome(head):
>     # Find middle
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>     if fast:  # odd length: skip the center node
>         slow = slow.next
>     # Reverse second half
>     prev, curr = None, slow
>     while curr:
>         nxt = curr.next
>         curr.next = prev
>         prev, curr = curr, nxt
>     # Compare
>     l, r = head, prev
>     result = True
>     while r:
>         if l.val != r.val:
>             result = False
>             break
>         l, r = l.next, r.next
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Push first half onto a stack, compare with second half: O(n) time, O(n/2) space.
> - Recursion: O(n) call stack. Use a nonlocal `left` pointer advancing from head while recursion unwinds from tail.
> - If you need to preserve the original list, reverse the second half back after comparison.

---

### Reorder List `🎯 T2`

> [!example] Problem
> You are given the head of a singly linked-list. The list can be represented as:
> Reorder the list to be on the following form:
> You may not modify the values in the list's nodes. Only nodes themselves may be changed.
> 
> **Example 1:**
> ```
> L0 → L1 → … → Ln - 1 → Ln
> ```
> 
> **Example 2:**
> ```
> L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …
> ```
> 
> **Example 3:**
> ```
> Input: head = [1,2,3,4]
> Output: [1,4,2,3]
> ```
> 
> **Example 4:**
> ```
> Input: head = [1,2,3,4,5]
> Output: [1,5,2,4,3]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [1, 5 * 10^4].
> - 1 <= Node.val <= 1000

> [!info] Approach
> **Find middle + reverse second half + interleave.** We need nodes from both ends simultaneously. The structure is: first half forward, second half backward, interleaved. Three clean steps — find middle, reverse second half, interleave two halves. Slow/fast to find mid. Reverse second half. Merge two halves alternating: take one from first, one from second (reversed), repeat until second half is exhausted.

> [!note]- Python Solution
> ```python
> def reorder_list(head):
>     if not head or not head.next:
>         return
>     # Step 1: find middle
>     slow, fast = head, head
>     while fast.next and fast.next.next:
>         slow = slow.next
>         fast = fast.next.next
>     # Step 2: reverse second half
>     prev, curr = None, slow.next
>     slow.next = None  # cut the list
>     while curr:
>         nxt = curr.next
>         curr.next = prev
>         prev, curr = curr, nxt
>     # Step 3: interleave
>     first, second = head, prev
>     while second:
>         tmp1, tmp2 = first.next, second.next
>         first.next = second
>         second.next = tmp1
>         first, second = tmp1, tmp2
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Collect nodes into an array, two-pointer reassignment: O(n) time, O(n) space. Much simpler to write, unacceptable if O(1) space required.

---

### Reverse Nodes in K-Group `🎯 T2`

> [!example] Problem
> Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.
> k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.
> You may not alter the values in the list's nodes, only nodes themselves may be changed.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], k = 2
> Output: [2,1,4,3,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2,3,4,5], k = 3
> Output: [3,2,1,4,5]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is n.
> - 1 <= k <= n <= 5000
> - 0 <= Node.val <= 1000

> [!info] Approach
> **Count-verify + in-place reversal per group.** We reverse groups of exactly K. Must verify K nodes exist before reversing each group — don't reverse a partial tail. Count K nodes forward. If fewer than K remain, return head as-is. Reverse K nodes. Connect tail of reversed group to result of recursive call on the rest. Check-count loop + standard in-place reversal of exactly K nodes. After reversing, `head` (original) is the tail of the reversed group; link it to the recursive result.

> [!note]- Python Solution
> ```python
> def reverse_k_group(head, k):
>     # Check if k nodes exist
>     node, count = head, 0
>     while node and count < k:
>         node = node.next
>         count += 1
>     if count < k:
>         return head  # fewer than k nodes — don't reverse
>     # Reverse exactly k nodes
>     prev, curr = None, head
>     for _ in range(k):
>         nxt = curr.next
>         curr.next = prev
>         prev, curr = curr, nxt
>     # head is now the tail of reversed group; link to next group
>     head.next = reverse_k_group(curr, k)
>     return prev  # prev is new head of this group
> ```

> [!success] Complexity
> Time O(n), Space O(n/k) recursion stack.

> [!tip] Alternatives
> - Iterative with `tail_of_prev_group.next` pointer: O(1) space, more complex bookkeeping.
> - `k=2` special case (Swap Nodes in Pairs): cleaner iterative code with dummy node.

---

## Fast / Slow Pointers

---

### Linked List Cycle `🎯 T2`

> [!example] Problem
> Given head, the head of a linked list, determine if the linked list has a cycle in it.
> There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.
> Return true if there is a cycle in the linked list. Otherwise, return false.
> 
> **Example 1:**
> ```
> Input: head = [3,2,0,-4], pos = 1
> Output: true
> Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2], pos = 0
> Output: true
> Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.
> ```
> 
> **Example 3:**
> ```
> Input: head = [1], pos = -1
> Output: false
> Explanation: There is no cycle in the linked list.
> ```
> 
> **Constraints:**
> - The number of the nodes in the list is in the range [0, 10^4].
> - -10^5 <= Node.val <= 10^5
> - pos is -1 or a valid index in the linked-list.

> [!tip] Recognize · Gotcha
> **Signal:** Floyd; meet proves cycle · **Gotcha:** Check `fast` and `fast.next` before advancing.

> [!info] Approach
> **Floyd's fast/slow pointer cycle detection.** Without Floyd's, you'd need to store all visited nodes in a hash set — O(n) space. Floyd's uses two pointers that must meet inside a cycle. Fast moves 2 steps, slow moves 1. If they ever point to the same node, a cycle exists. If fast reaches null, no cycle. Start both at `head`. Loop: `slow = slow.next`, `fast = fast.next.next`. Check `slow is fast` (identity, not equality). If `fast` or `fast.next` is None, exit — no cycle. The identity check matters whenever node values can repeat.

> [!note]- Python Solution
> ```python
> def has_cycle(head):
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>         if slow is fast:
>             return True
>     return False
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Hash set of visited nodes: O(n) time, O(n) space. Simpler logic but extra space.
> - Critical: use `is` not `==`. Two nodes with equal values would falsely trigger `==`.

---

### Remove Nth Node From End of List `🎯 T2`

> [!example] Problem
> Given the head of a linked list, remove the nth node from the end of the list and return its head.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], n = 2
> Output: [1,2,3,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1], n = 1
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: head = [1,2], n = 1
> Output: [1]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is sz.
> - 1 <= sz <= 30
> - 0 <= Node.val <= 100
> - 1 <= n <= sz

> [!info] Approach
> **Two pointers with N+1 gap.** We don't know the length. One pointer can be N steps ahead — when it hits null, the other is at the target. Two pointers with a dummy head. `fast` advances N+1 steps ahead (one extra to land `slow` before the deletion target). Then both advance until `fast` is None. Dummy → head. Advance `fast` by `n+1` steps. Then `while fast: slow=slow.next, fast=fast.next`. Now `slow` is the predecessor of the node to delete. `slow.next = slow.next.next`.

> [!note]- Python Solution
> ```python
> def remove_nth_from_end(head, n):
>     dummy = ListNode(0, head)
>     fast = slow = dummy
>     for _ in range(n + 1):
>         fast = fast.next
>     while fast:
>         slow = slow.next
>         fast = fast.next
>     slow.next = slow.next.next
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Find length, then walk to `length - n`: two passes. O(n) each, simpler code.
> - Recursion with counter: elegant but O(n) stack space.

**Also try:**

- **Middle of the Linked List** — Fast/slow one-pass middle finder
- **Delete the Middle Node of a Linked List** — Slow/fast with prev pointer — land before middle
- **Happy Number** — Floyd's cycle detection on the implicit sequence

---

## Floyd's Cycle Detection

---

### Linked List Cycle II `🎯 T2`

> [!example] Problem
> Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.
> There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to (0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a parameter.
> Do not modify the linked list.
> 
> **Example 1:**
> ```
> Input: head = [3,2,0,-4], pos = 1
> Output: tail connects to node index 1
> Explanation: There is a cycle in the linked list, where tail connects to the second node.
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2], pos = 0
> Output: tail connects to node index 0
> Explanation: There is a cycle in the linked list, where tail connects to the first node.
> ```
> 
> **Example 3:**
> ```
> Input: head = [1], pos = -1
> Output: no cycle
> Explanation: There is no cycle in the linked list.
> ```
> 
> **Constraints:**
> - The number of the nodes in the list is in the range [0, 10^4].
> - -10^5 <= Node.val <= 10^5
> - pos is -1 or a valid index in the linked-list.

> [!tip] Recognize · Gotcha
> **Signal:** Floyd + math · **Gotcha:** **Why entry?** — length algebra; **wrong**: restarting only fast from meet.

> [!info] Approach
> **Floyd's two-phase cycle entry detection.** Detection alone is O(1) space. Finding the entry requires a mathematical insight from Floyd's algorithm. After slow/fast meet inside cycle, reset one pointer to head. Advance both at speed 1. Their meeting point is the cycle entry. Phase 1 — slow and fast meet after slow travels distance `d+c`, fast travels `d+c+L` (one full cycle extra), where `d` = head-to-entry, `c` = entry-to-meeting, `L` = cycle length. This implies `d = L - c = d'` (distance from meeting point back to entry). Phase 2 — slow resets to head, both advance 1 step at a time → they meet at the entry.

> [!note]- Python Solution
> ```python
> def detect_cycle(head):
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>         if slow is fast:
>             break
>     else:
>         return None  # no cycle
>     slow = head
>     while slow is not fast:
>         slow = slow.next
>         fast = fast.next
>     return slow
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Hash set of visited nodes: O(n) space. Return first node seen twice.
> - The `for-else` pattern catches the no-cycle case cleanly; alternatively use a boolean flag.

---

### Find the Duplicate Number (Floyd's variant) `🎯 T2`

> Full walkthrough: [Find the Duplicate Number](01-array.md#find-the-duplicate-number--t2).

---

## Merge / Sorting

---

### Merge Two Sorted Lists `🎯 T2`

> [!example] Problem
> You are given the heads of two sorted linked lists list1 and list2.
> Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.
> Return the head of the merged linked list.
> 
> **Example 1:**
> ```
> Input: list1 = [1,2,4], list2 = [1,3,4]
> Output: [1,1,2,3,4,4]
> ```
> 
> **Example 2:**
> ```
> Input: list1 = [], list2 = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: list1 = [], list2 = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - The number of nodes in both lists is in the range [0, 50].
> - -100 <= Node.val <= 100
> - Both list1 and list2 are sorted in non-decreasing order.

> [!tip] Recognize · Gotcha
> **Signal:** Dummy node · **Gotcha:** **In-place** vs new list; **dummy** avoids null head cases.

> [!info] Approach
> **Dummy head + two-pointer merge.** Two-pointer merge from merge sort. A dummy head eliminates the special case of "what is the initial head of the result?" Compare heads of both lists, attach the smaller, advance that pointer. Append the remaining non-empty list. `dummy → result chain`. `curr` pointer builds the result. While both `l1` and `l2` non-null: attach smaller, advance it. After loop, attach the non-null remainder.

> [!note]- Python Solution
> ```python
> def merge_two_lists(l1, l2):
>     dummy = ListNode(0)
>     curr = dummy
>     while l1 and l2:
>         if l1.val <= l2.val:
>             curr.next = l1
>             l1 = l1.next
>         else:
>             curr.next = l2
>             l2 = l2.next
>         curr = curr.next
>     curr.next = l1 or l2
>     return dummy.next
> ```

> [!success] Complexity
> Time O(m+n), Space O(1).

> [!tip] Alternatives
> - Recursive: elegant, O(m+n) stack space. `return l1 if not l2 else l2 if not l1 else ...`
> - Creating new nodes: O(m+n) space — never do this; just relink existing nodes.

---

### Sort List `🎯 T2`

> [!example] Problem
> Given the head of a linked list, return the list after sorting it in ascending order.
> 
> **Example 1:**
> ```
> Input: head = [4,2,1,3]
> Output: [1,2,3,4]
> ```
> 
> **Example 2:**
> ```
> Input: head = [-1,5,3,4,0]
> Output: [-1,0,3,4,5]
> ```
> 
> **Example 3:**
> ```
> Input: head = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 5 * 10^4].
> - -10^5 <= Node.val <= 10^5

> [!info] Approach
> **Bottom-up merge sort on linked list.** Quicksort on linked lists has O(n²) worst case (no random access for pivot selection). Merge sort is naturally suited to linked lists — splitting is O(n) with slow/fast, merging is O(n). Bottom-up merge sort to achieve O(1) space (avoids O(log n) recursion stack). For each sublist size `size = 1, 2, 4, 8, ...`: split list into pairs of `size`-length sublists, merge each pair, connect results. One full pass per doubling of `size`, log n passes total. This is the version interviewers like when they explicitly ask for O(1) extra space.

> [!note]- Python Solution
> ```python
> def sort_list(head):
>     if not head or not head.next:
>         return head
> 
>     # Get length
>     length, node = 0, head
>     while node:
>         length += 1
>         node = node.next
> 
>     dummy = ListNode(0, head)
>     size = 1
>     while size < length:
>         curr = dummy.next
>         tail = dummy
>         while curr:
>             left = curr
>             right = split(left, size)
>             curr = split(right, size)
>             merged_head, merged_tail = merge(left, right)
>             tail.next = merged_head
>             tail = merged_tail
>         size *= 2
>     return dummy.next
> 
> def split(head, n):
>     """Cut first n nodes, return the rest."""
>     for _ in range(n - 1):
>         if not head:
>             break
>         head = head.next
>     if not head:
>         return None
>     rest = head.next
>     head.next = None
>     return rest
> 
> def merge(l1, l2):
>     """Merge two sorted lists, return (head, tail)."""
>     dummy = ListNode(0)
>     curr = dummy
>     while l1 and l2:
>         if l1.val <= l2.val:
>             curr.next = l1
>             l1 = l1.next
>         else:
>             curr.next = l2
>             l2 = l2.next
>         curr = curr.next
>     curr.next = l1 or l2
>     while curr.next:
>         curr = curr.next
>     return dummy.next, curr
> ```

> [!success] Complexity
> Time O(n log n), Space O(1).

> [!tip] Alternatives
> - Top-down recursive merge sort: O(n log n) time, O(log n) stack. Simpler to write; acceptable unless O(1) space is required.

**Also try:**

- **Insertion Sort List** — Dummy head + find-insertion-point per node

---

## Copy / Design

---

### Copy List with Random Pointer `🎯 T2`

> [!example] Problem
> A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null.
> Construct a deep copy of the list. The deep copy should consist of exactly n brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the next and random pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.
> For example, if there are two nodes X and Y in the original list, where X.random --> Y, then for the corresponding two nodes x and y in the copied list, x.random --> y.
> Return the head of the copied linked list.
> The linked list is represented in the input/output as a list of n nodes. Each node is represented as a pair of [val, random_index] where:
> Your code will only be given the head of the original linked list.
> 
> **Example 1:**
> ```
> Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
> Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]
> ```
> 
> **Example 2:**
> ```
> Input: head = [[1,1],[2,1]]
> Output: [[1,1],[2,1]]
> ```
> 
> **Example 3:**
> ```
> Input: head = [[3,null],[3,0],[3,null]]
> Output: [[3,null],[3,0],[3,null]]
> ```
> 
> **Constraints:**
> - 0 <= n <= 1000
> - -10^4 <= Node.val <= 10^4
> - Node.random is null or is pointing to some node in the linked list.

> [!tip] Recognize · Gotcha
> **Signal:** Old→new map · **Gotcha:** **O(n)** space; **O(1)** space trick exists (interleave nodes) — bonus for senior.

> [!info] Approach
> **Hash map original→clone, two-pass wiring.** Copying `next` is easy. `random` points to arbitrary nodes — we need to map original nodes to their clones to set `random` correctly. Hash map `original → clone`. Two passes: first create all clones, second assign `next` and `random` using the map. Pass 1: iterate and create `{node: ListNode(node.val)}` for all nodes. Pass 2: for each original node, set `clone.next = map[node.next]`, `clone.random = map[node.random]`. Mapping `None → None` keeps the wiring concise.

> [!note]- Python Solution
> ```python
> class Node:
>     def __init__(self, val, next=None, random=None):
>         self.val = val
>         self.next = next
>         self.random = random
> 
> def copy_random_list(head):
>     if not head:
>         return None
>     clone_map = {None: None}
>     curr = head
>     while curr:
>         clone_map[curr] = Node(curr.val)
>         curr = curr.next
>     curr = head
>     while curr:
>         clone_map[curr].next = clone_map[curr.next]
>         clone_map[curr].random = clone_map[curr.random]
>         curr = curr.next
>     return clone_map[head]
> ```

> [!success] Complexity
> Time O(n), Space O(n) for the map.

> [!tip] Alternatives
> - O(1) space interleave trick: Insert each clone right after its original (`A → A' → B → B'`). Set `clone.random = orig.random.next`. Detach clones. Three passes, O(n) time, O(1) space.

---

### LRU Cache `🎯 T2`

> [!example] Problem
> Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
> Implement the LRUCache class:
> The functions get and put must each run in O(1) average time complexity.
> 
> **Example 1:**
> ```
> Input
> ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
> [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
> Output
> [null, null, null, 1, null, -1, null, -1, 3, 4]
> 
> Explanation
> LRUCache lRUCache = new LRUCache(2);
> lRUCache.put(1, 1); // cache is {1=1}
> lRUCache.put(2, 2); // cache is {1=1, 2=2}
> lRUCache.get(1);    // return 1
> lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
> lRUCache.get(2);    // returns -1 (not found)
> lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
> lRUCache.get(1);    // return -1 (not found)
> lRUCache.get(3);    // return 3
> lRUCache.get(4);    // return 4
> ```
> 
> **Constraints:**
> - 1 <= capacity <= 3000
> - 0 <= key <= 10^4
> - 0 <= value <= 10^5
> - At most 2 * 10^5 calls will be made to get and put.

> [!tip] Recognize · Gotcha
> **Signal:** HashMap + DLL · **Gotcha:** **Doubly linked** for O(1) remove; **dummy head/tail** simplifies edges. Thread-safety follow-up at senior level.

> [!failure] Tempting wrong approach
> A list with `remove()` (O(n)), or a dict alone (no recency order). Use a hashmap + doubly linked list with sentinels (or `OrderedDict.move_to_end`).

> [!info] Approach
> **Doubly linked list + hash map.** We need O(1) access (hash map) and O(1) eviction/promotion (doubly linked list). Neither alone suffices. Doubly linked list for recency order (MRU at head, LRU at tail) + hash map for O(1) node lookup by key. Dummy head and dummy tail eliminate all edge cases in `_remove` and `_insert_front`. On `get`: remove from current position, insert at front, return value. On `put`: if key exists, remove old; create new node, insert at front, update map; if over capacity, remove LRU (tail.prev), delete from map.

> [!note]- Python Solution
> ```python
> class DLLNode:
>     def __init__(self, key=0, val=0):
>         self.key = key
>         self.val = val
>         self.prev: Optional['DLLNode'] = None
>         self.next: Optional['DLLNode'] = None
> 
> class LRUCache:
>     def __init__(self, capacity):
>         self.cap = capacity
>         self.cache: dict[int, DLLNode] = {}
>         self.head = DLLNode()  # dummy MRU sentinel
>         self.tail = DLLNode()  # dummy LRU sentinel
>         self.head.next = self.tail
>         self.tail.prev = self.head
> 
>     def _remove(self, node):
>         node.prev.next = node.next
>         node.next.prev = node.prev
> 
>     def _insert_front(self, node):
>         node.next = self.head.next
>         node.prev = self.head
>         self.head.next.prev = node
>         self.head.next = node
> 
>     def get(self, key):
>         if key not in self.cache:
>             return -1
>         node = self.cache[key]
>         self._remove(node)
>         self._insert_front(node)
>         return node.val
> 
>     def put(self, key, value):
>         if key in self.cache:
>             self._remove(self.cache[key])
>         node = DLLNode(key, value)
>         self.cache[key] = node
>         self._insert_front(node)
>         if len(self.cache) > self.cap:
>             lru = self.tail.prev
>             self._remove(lru)
>             del self.cache[lru.key]
> ```

> [!success] Complexity
> Time O(1) average for `get` and `put`, Space O(capacity).

> [!tip] Alternatives
> - `collections.OrderedDict`: great in Python interviews if allowed, but explain the underlying DLL + hash map idea first.
> - The key invariant is consistency: every cache key must have exactly one live node in the list and one entry in the map.

---

## Other Manipulation

**Also try:**

- **Add Two Numbers** — Digit-by-digit addition with carry
- **Swap Nodes in Pairs** — Dummy head + iterative pair swapping
- **Intersection of Two Linked Lists** — Two pointers traversing both lists — alignment by total distance
- **Rotate List (Circular List Trick)** — Make circular, find new tail, break circle
- **Remove Duplicates from Sorted List** — Single pass: skip consecutive equal nodes
- **Remove Duplicates from Sorted List II** — Dummy head + prev pointer skipping duplicate runs
- **Partition List** — Two dummy heads — collect two sublists, then join
- **Flatten a Multilevel Doubly Linked List** — Iterative in-place child list splicing

---
