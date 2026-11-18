---
module: root
topic: Questions
tags: [root, questions]
---
# Data Structures and Algorithms Questions

## What this covers

> [!abstract] In this file
> **Covers:** Index of all 200 walkthrough problems grouped by topic, with tier and a link to each walkthrough.
> **You'll be able to:** Find any problem's walkthrough and work through all T1s first.
> **Prereqs:** None · **Pair with:** [Mindmap](../03-patterns/mindmap.md) · **Time:** lookup
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [Data Structures](#data-structures) · [Algorithms](#algorithms)

---

> [!note] L3 Reference Index — not a tracker
> A lookup table of every problem covered in the `04-practice/` walkthroughs, grouped by canonical topic. Each problem appears exactly once.
> **Track your own solve progress elsewhere** (LeetCode list, spreadsheet, Anki). This file is for "which problems exist, and where is the writeup" — read it once, then use it as a lookup.

**200 problems** — 72 `⚡ T1` · 115 `🎯 T2` · 13 `💤 T3`. If you are short on time, solve every `⚡ T1` before touching any `🎯 T2`; `💤 T3` only for L4+ / hard-round loops.

- Pattern logic and gotchas → [`03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md`](../03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md)
- Study order and pacing → [`00-start-here/l3-google-roadmap.md`](../00-start-here/l3-google-roadmap.md)
- Difficulty tags: `[E]` easy · `[M]` medium · `[H]` hard

## Data Structures

### Array

- [3Sum `⚡ T1`](data-structures/01-array.md#3sum--t1) — Find all unique triplets `[a, b, c]` in `nums` with `a + b + c = 0`. No duplicate triplets [M]
- [3Sum Closest `⚡ T1`](data-structures/01-array.md#3sum-closest--t1) — Find the triplet whose sum is closest to a given target. Return the sum [M]
- [Two Sum II (sorted) `⚡ T1`](algorithms/03-two-pointers.md#two-sum-ii--input-array-is-sorted-lc-167--t1) — Sorted array; find two numbers that add to a target and return their 1-based indices [M]
- [Container with Most Water `⚡ T1`](data-structures/01-array.md#container-with-most-water--t1) — Given heights of vertical lines, find the two lines that form a container holding the maximum water [M]
- [Trapping Rain Water `⚡ T1`](algorithms/03-two-pointers.md#trapping-rain-water-lc-42--t1) — Given an elevation map, compute how much water it can trap after raining [H]
- [Best Time to Buy and Sell Stock `🎯 T2`](data-structures/01-array.md#best-time-to-buy-and-sell-stock--t2) — Given an array `prices` where `prices[i]` is the price of a stock on day `i`, find the maximum profit from a single buy-sell transaction. You cannot sell before buying [E]
- [Maximum Subarray `🎯 T2`](data-structures/01-array.md#maximum-subarray--t2) — Find the contiguous subarray with the largest sum. Return the sum [M]
- [Find the Duplicate Number `🎯 T2`](data-structures/01-array.md#find-the-duplicate-number--t2) — Given an array of n+1 integers where each integer is in [1, n], find the one duplicate without modifying the array and using O(1) extra space [M]
- [Spiral Matrix `🎯 T2`](data-structures/01-array.md#spiral-matrix) — Return all elements of an m×n matrix in spiral order [M]
- [Set Matrix Zeroes `🎯 T2`](data-structures/01-array.md#set-matrix-zeroes) — If a cell is zero, set its entire row and column to zero. Do it in-place [M]

### Hashing

- [Two Sum `⚡ T1`](data-structures/02-hashing.md#two-sum--t1) — Given an integer array `nums` and target, return indices of two numbers that sum to `target`. Exactly one solution exists [E]
- [Valid Anagram `🎯 T2`](data-structures/03-string.md#valid-anagram--t2) — Return true if `t` is an anagram of `s` (same characters, same counts) [E]
- [Subarray Sum Equals K `⚡ T1`](data-structures/01-array.md#subarray-sum-equals-k-with-negative-numbers--t1) — Count the number of contiguous subarrays with sum equal to `k`. Array may contain negatives [M]
- [Longest Consecutive Sequence `⚡ T1`](data-structures/02-hashing.md#longest-consecutive-sequence--t1) — Find the length of the longest consecutive elements sequence in an unsorted array. O(n) required [H]
- [Valid Sudoku (LC 36) `🎯 T2`](data-structures/02-hashing.md#valid-sudoku-lc-36--t2) — 27 sets over rows, columns and 3x3 boxes in one pass [M]

### String

- [Longest Substring Without Repeating Characters `⚡ T1`](data-structures/03-string.md#longest-substring-without-repeating-characters--t1) — Given string `s`, return the length of the longest substring with all unique characters [M]
- [Minimum Window Substring `⚡ T1`](data-structures/03-string.md#minimum-window-substring--t1) — Find the smallest substring of `s` containing all characters of `t` (with multiplicity) [H]
- [Longest Repeating Character Replacement `⚡ T1`](data-structures/03-string.md#longest-repeating-character-replacement--t1) — Given string `s` and integer `k`, find the length of the longest substring where you can replace at most `k` characters to make all characters in the window the same [M]
- [Permutation in String `⚡ T1`](algorithms/04-sliding-window.md#permutation-in-string-lc-567--t1) — Given strings `s1` and `s2`, return True if any permutation of `s1` is a substring of `s2`. LeetCode 567 [M]
- [Longest Palindromic Substring `⚡ T1`](data-structures/03-string.md#longest-palindromic-substring--t1) — Given string `s`, return the longest substring that is a palindrome [M]
- [Palindromic Substrings `🎯 T2`](data-structures/03-string.md#palindromic-substrings-count-all-palindromic-substrings) — Given string `s`, return the total count of substrings that are palindromes (single characters count too) [M]
- [Valid Palindrome `🎯 T2`](data-structures/03-string.md#valid-palindrome--t2) — Given string `s`, return true if it is a palindrome considering only alphanumeric characters and ignoring case [E]
- [Valid Palindrome II `🎯 T2`](data-structures/03-string.md#valid-palindrome-ii-lc-680--t2) — Given string `s`, return true if the string can become a palindrome by removing **at most one** character [E]
- [Group Anagrams `⚡ T1`](data-structures/03-string.md#group-anagrams--t1) — Group strings that are anagrams of each other [M]
- [Encode and Decode Strings `🎯 T2`](data-structures/03-string.md#encode-and-decode-strings--t2) — Design functions `encode(strs)` and `decode(s)` to encode a list of strings into a single string and decode it back. The encoding must handle strings that contain any character including `#` and `/` [M]
- [Longest Duplicate Substring `⚡ T1`](algorithms/02-string-algorithms.md#longest-duplicate-substring--t1) — Find the longest substring appearing at least twice. Binary search on length + Rabin-Karp rolling hash [H]
- [Repeated String Match `🎯 T2`](algorithms/02-string-algorithms.md#repeated-string-match--t2) — Minimum times to repeat `a` so that `b` is a substring of it; KMP or Z on the bounded repetition [M]
- [Longest Happy Prefix `🎯 T2`](algorithms/02-string-algorithms.md#longest-happy-prefix--t2) — Longest proper prefix that is also a suffix. The answer *is* `lps[-1]` from KMP [H]
- [Shortest Palindrome `🎯 T2`](algorithms/02-string-algorithms.md#add-minimum-characters-to-make-a-string-palindrome) — Add minimum characters to the front to make `s` a palindrome; run KMP on `s + '#' + rev(s)` [H]

### Linked List

- [LRU Cache `🎯 T2`](data-structures/07-linked-list.md#lru-cache--t2) — Design a cache with O(1) `get` and `put` operations, evicting the Least Recently Used item when capacity is exceeded [M]
- [Merge Two Sorted Lists `🎯 T2`](data-structures/07-linked-list.md#merge-two-sorted-lists--t2) — Merge two sorted linked lists into one sorted list. Return the head of the merged list [E]
- [Linked List Cycle `🎯 T2`](data-structures/07-linked-list.md#linked-list-cycle--t2) — Detect if a linked list has a cycle [E]
- [Add Two Numbers `🎯 T2`](data-structures/07-linked-list.md#add-two-numbers) — Two non-empty linked lists represent non-negative integers in reverse order (each node = one digit). Return the sum as a linked list in reverse order [M]
- [Reorder List `🎯 T2`](data-structures/07-linked-list.md#reorder-list--t2) — Reorder list in-place: `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...` [M]
- [Copy List with Random Pointer `🎯 T2`](data-structures/07-linked-list.md#copy-list-with-random-pointer--t2) — Deep copy a linked list where each node has `next` and `random` pointers. `random` may point to any node or null [M]

### Stack

- [Valid Parentheses `🎯 T2`](data-structures/05-stack.md#valid-parentheses--t2) — Given a string of `()[]{}`, determine if the brackets are valid (properly nested and matched) [E]
- [Min Stack `🎯 T2`](data-structures/05-stack.md#min-stack--t2) — Design a stack with O(1) `push`, `pop`, `top`, and `get_min` [M]
- [Daily Temperatures `🎯 T2`](data-structures/05-stack.md#daily-temperatures--t2) — Given a list of daily temperatures, return an array where `result[i]` is the number of days until a warmer temperature. If no warmer day exists, `result[i] = 0` [M]
- [Largest Rectangle in Histogram `🎯 T2`](data-structures/05-stack.md#largest-rectangle-in-histogram--t2) — Given heights of bars in a histogram, find the area of the largest rectangle that fits within the histogram [H]
- [Valid Parenthesis String `🎯 T2`](data-structures/05-stack.md#valid-parenthesis-string-lc-678--t2) — String of `(`, `)`, and `*` where `*` can act as `(`, `)`, or empty. Determine if the string can be valid [M]

### Queue

- [Sliding Window Maximum `⚡ T1`](data-structures/06-queue.md#sliding-window-maximum--t1) — Return the maximum in each sliding window of size `k` [H]
- [Jump Game III `🎯 T2`](data-structures/06-queue.md#jump-game-iii--t2) — Given array `arr` and start index `start`, at each index `i` you can jump to `i + arr[i]` or `i - arr[i]`. Return true if you can reach any index with value 0 [M]
- [Walls and Gates `⚡ T1`](data-structures/13-graph.md#walls-and-gates-lc-286--t1) — Grid with `-1` (wall), `0` (gate), `INF` (empty room). Fill each empty room with its distance to the nearest gate. Modify in place [M]

### Tree

- [Invert Binary Tree `🎯 T2`](data-structures/08-tree.md#invert-binary-tree--t2) — Given a binary tree root, mirror it — every left child becomes right and vice versa at every level [E]
- [Diameter of Binary Tree `🎯 T2`](data-structures/08-tree.md#diameter-of-binary-tree--t2) — Return the length of the longest path between any two nodes (measured in edges). The path need not pass through the root [M]
- [Lowest Common Ancestor `🎯 T2`](data-structures/08-tree.md#lowest-common-ancestor) — Find LCA of two nodes in a BST and in a general binary tree [M]
- [Validate BST `🎯 T2`](data-structures/08-tree.md#validate-binary-search-tree--t2) — Check if a binary tree satisfies BST ordering [M]
- [Kth Smallest in BST `🎯 T2`](data-structures/08-tree.md#kth-smallest-element-in-a-bst--t2) — Return the kth smallest value in a BST [M]
- [Count Good Nodes `🎯 T2`](data-structures/08-tree.md#count-good-nodes-in-binary-tree--t2) — A node X is "good" if no node on the root-to-X path has a value greater than X.val. Count good nodes [M]
- [Construct Binary Tree from Preorder and Inorder `🎯 T2`](data-structures/08-tree.md) — Given preorder and inorder traversal arrays, reconstruct the binary tree [M]
- [Binary Tree Maximum Path Sum `🎯 T2`](data-structures/08-tree.md#binary-tree-maximum-path-sum--t2) — Find the maximum path sum between any two nodes. Values can be negative; a path can start and end anywhere [H]
- [House Robber III `🎯 T2`](data-structures/08-tree.md#house-robber-iii--t2) — Houses are arranged in a binary tree. Adjacent nodes (parent-child) cannot both be robbed. Maximize total money robbed [M]
- [Balanced Binary Tree (LC 110) `⚡ T1`](data-structures/08-tree.md#balanced-binary-tree-lc-110--t1) — O(n) post-order with a `-1` sentinel [E]

### Heap

- [Merge K Sorted Lists `⚡ T1`](data-structures/10-heap.md#merge-k-sorted-lists--t1) — Merge `k` sorted linked lists into one sorted linked list [H]
- [Kth Largest Element `⚡ T1`](data-structures/10-heap.md#kth-largest-element-in-an-array--t1) — Find the kth largest element in an array [M]
- [Top K Frequent `⚡ T1`](data-structures/02-hashing.md#top-k-frequent-elements--t1) — Return the k most frequent elements or words [M]
- [K Closest Points to Origin `⚡ T1`](data-structures/10-heap.md#k-closest-points-to-origin--t1) — Given `n` points, return the `k` closest to the origin `(0, 0)` (Euclidean distance) [M]
- [Task Scheduler `⚡ T1`](data-structures/06-queue.md#task-scheduler--t1) — Given tasks (letters) and a cooldown `n`, find the minimum time to finish all tasks. Same task must have at least `n` intervals gap [M]
- [Last Stone Weight `⚡ T1`](data-structures/10-heap.md#last-stone-weight--t1) — Each turn smash the two heaviest stones. If equal, both destroyed; otherwise the difference survives. Return the weight of the last stone (or 0) [E]
- [Find Median from Data Stream `⚡ T1`](data-structures/06-queue.md#find-median-from-data-stream--t1) — Design a data structure supporting `add_num(num)` and `find_median()` on a dynamic stream [H]
- Trapping Rain Water II `⚡ T1` — Given a 2D height map, compute the total trapped water. Min-heap over boundary cells, flood inward [H]
- [Minimum Interval to Include Each Query (LC 1851) `🎯 T2`](data-structures/10-heap.md#minimum-interval-to-include-each-query-lc-1851--t2) — offline sweep with a min-heap of `(size, right)` and lazy expiry [H]

### Trie

- [Implement Trie `⚡ T1`](data-structures/09-trie.md#implement-trie-prefix-tree--t1) — Implement a Trie with `insert(word)`, `search(word)` (returns true only if the exact word was inserted), and `startsWith(prefix)` (returns true if any inserted word begins with `prefix`) [E]
- [Word Search II `⚡ T1`](data-structures/09-trie.md#word-search-ii--t1) — Given a board of characters and a list of words, return all words that appear on the board. A word is valid if it can be traced through adjacent (4-directional) cells without reusing any cell within the same word [H]

### Graphs

- [Number of Islands `⚡ T1`](data-structures/13-graph.md#number-of-islands-bfs--t1) — Given a 2D grid of '1' (land) and '0' (water), count the number of islands (connected components of land, 4-directional) [M]
- [Max Area of Island `⚡ T1`](data-structures/13-graph.md#max-area-of-island--t1) — Given a binary 2D grid (0=water, 1=land), return the maximum area of any island (connected 1s, 4-directional). Return 0 if no island [M]
- [Rotting Oranges `⚡ T1`](data-structures/13-graph.md#rotting-oranges--t1) — Grid of `0` (empty), `1` (fresh), `2` (rotten). Each minute every rotten orange infects its 4-directional fresh neighbors. Return time until no fresh orange remains, or -1 if impossible [M]
- [Surrounded Regions `⚡ T1`](data-structures/13-graph.md#surrounded-regions--t1) — Given an m×n board of 'X' and 'O', flip all 'O' regions completely surrounded by 'X' to 'X'. 'O's connected to the border are never flipped [M]
- [Pacific Atlantic Water Flow `⚡ T1`](data-structures/13-graph.md#pacific-atlantic-water-flow--t1) — Given an m×n height matrix, water flows to 4-adjacent cells of equal or lesser height. Find all cells from which water can reach both the Pacific (top/left border) and Atlantic (bottom/right border) oceans [M]
- [Clone Graph `⚡ T1`](data-structures/13-graph.md#clone-graph--t1) — Given a reference to a node in an undirected connected graph, return a deep copy [M]
- [Course Schedule `⚡ T1`](data-structures/06-queue.md#course-schedule--t1) — Given `numCourses` and a list of `prerequisites [a, b]` meaning "to take course `a`, you must first take course `b`", return `true` if it is possible to finish all courses (LC 207) [M]
- [Course Schedule II `⚡ T1`](data-structures/13-graph.md#course-schedule-ii--t1) — Same setup as Course Schedule, but return one valid ordering of courses to take. Return an empty list if impossible (LC 210) [M]
- [Word Ladder `⚡ T1`](data-structures/13-graph.md#word-ladder--t1) — Given `beginWord`, `endWord`, and a word list, return the length of the shortest transformation sequence from `beginWord` to `endWord` where each step changes exactly one letter and each intermediate word must exist in the word list. Return 0 if no sequence exists [H]
- [Word Ladder II `⚡ T1`](algorithms/13-graph-algorithms.md#word-ladder-ii-all-shortest-transformation-sequences--t1) — Same as Word Ladder, but return **all** shortest transformation sequences from `beginWord` to `endWord` [H]
- [Alien Dictionary `⚡ T1`](algorithms/00-sorting.md#alien-dictionary-lc-269--t1) — Given a list of words from an alien dictionary sorted in alien lexicographic order, derive the order of letters in the alien alphabet. Return any valid order, or `""` if the ordering is invalid (contains a cycle or a word is a prefix-violated neighbor) [H]

## Algorithms

### Binary Search

- [Koko Eating Bananas `⚡ T1`](algorithms/11-binary-search.md#koko-eating-bananas-lc-875--t1) — `piles` of bananas. Eat at constant speed `k` bananas/hour, one pile at a time. Must finish all piles in `h` hours. Minimize `k` [M]
- [Capacity to Ship Packages Within D Days `⚡ T1`](algorithms/11-binary-search.md#capacity-to-ship-packages-within-d-days-lc-1011--t1) — Ship packages in order. Ship has fixed capacity per day. Minimize capacity to ship all within `days` days [M]
- [Search in Rotated Sorted Array II `⚡ T1`](algorithms/11-binary-search.md#search-in-rotated-sorted-array-ii-lc-81--t1) — Rotated sorted array *with duplicates*. Return True if target exists [M]
- [Find Minimum in Rotated Sorted Array II `⚡ T1`](algorithms/11-binary-search.md#find-minimum-in-rotated-sorted-array-ii-lc-154--t1) — Rotated sorted array with duplicates. Find the minimum [M]
- [Search a 2D Matrix `⚡ T1`](algorithms/11-binary-search.md#search-a-2d-matrix-lc-74--t1) — Given an m×n matrix where each row is sorted and the first element of each row is greater than the last element of the previous row, search for a target value in O(log(m×n)) [M]
- [Time Based Key-Value Store `🎯 T2`](algorithms/11-binary-search.md#time-based-key-value-store-lc-981--t2) — Design a store where `set(key, value, timestamp)` saves versions and `get(key, timestamp)` returns the latest value with time ≤ timestamp (binary search over versions) [M]

### Greedy / Intervals

- [Merge Intervals `🎯 T2`](data-structures/01-array.md#merge-intervals-lc-56--t2) — Given a list of intervals, merge all overlapping intervals and return the result [M]
- [Meeting Rooms II `🎯 T2`](algorithms/16-greedy.md#meeting-rooms-ii) — Given intervals [start, end], find the minimum number of conference rooms required [M]
- [Jump Game `🎯 T2`](algorithms/16-greedy.md#jump-game-can-reach--t2) — Given an array where `nums[i]` is the max jump length from index `i`, determine if you can reach the last index [M]
- [Jump Game II `🎯 T2`](algorithms/16-greedy.md#jump-game-ii-minimum-jumps--t2) — Given an array where `nums[i]` is the max jump from index `i`, return the minimum number of jumps to reach the last index. Always reachable [M]
- [Gas Station `🎯 T2`](data-structures/01-array.md#gas-station-lc-134--t2) — There are `n` gas stations in a circle. `gas[i]` is the gas available at station `i`; `cost[i]` is the cost to travel from `i` to `i+1`. Find the starting station index from which you can complete the full circle, or return −1 if impossible [M]
- [Partition Labels `🎯 T2`](algorithms/16-greedy.md#partition-labels-lc-763) — Partition string s into as many parts as possible such that each letter appears in at most one part. Return list of partition sizes [M]

### Design

- [Insert Delete GetRandom `⚡ T1`](data-structures/02-hashing.md#insert-delete-getrandom-o1--t1) — Design a structure supporting `insert`, `delete`, and `getRandom` (uniform) all in O(1) average time [M]
- [Design Twitter `⚡ T1`](data-structures/10-heap.md#design-twitter--t1) — Design a simplified Twitter: `post_tweet(userId, tweetId)`, `get_news_feed(userId)` (10 most recent tweets from self + followees), `follow(followerId, followeeId)`, `unfollow` [M]
- [Design Underground System `⚡ T1`](data-structures/14-design.md#design-underground-system--t1) — open trips plus per-route `[sum, count]` aggregate, O(1) per op [M]
- [Design Browser History `⚡ T1`](data-structures/14-design.md#design-browser-history--t1) — two stacks, with the array+cursor variant as the O(1) follow-up [M]
- [Design Tic-Tac-Toe `⚡ T1`](data-structures/14-design.md#design-tic-tac-toe--t1) — signed row, column and diagonal counters, O(1) move [M]
- [Design Leaderboard `🎯 T2`](data-structures/14-design.md#design-leaderboard--t2) — dict plus `nlargest`, with a SortedList trade-off [M]
- [Design Snake Game `🎯 T2`](data-structures/14-design.md#design-snake-game--t2) — deque plus set; the tail moves before the collision check [M]
- [All O(1) Data Structure `🎯 T2`](data-structures/14-design.md#all-o1-data-structure--t2) — doubly linked list of count buckets with key sets [H]
- [Design a Food Rating System `🎯 T2`](data-structures/14-design.md#design-a-food-rating-system--t2) — per-cuisine heap with lazy deletion [M]
- [Design Phone Directory / Seat Reservation Manager `🎯 T2`](data-structures/14-design.md#design-phone-directory--seat-reservation-manager--t2) — counter plus min-heap of released seats; deque plus set for the directory [M]
- [Zigzag Iterator / Combination Iterator `🎯 T2`](data-structures/14-design.md#zigzag-iterator--combination-iterator--t2) — round-robin queue, and a lazy index odometer for combinations [M]
- [Encode and Decode TinyURL `🎯 T2`](data-structures/14-design.md#encode-and-decode-tinyurl--t2) — random base62 code with collision retry [M]
- [Design Bounded Blocking Queue `💤 T3`](data-structures/14-design.md#design-bounded-blocking-queue--t3) — two `Condition`s on one lock; senior follow-up [M]
- [Design Skiplist `💤 T3`](data-structures/14-design.md#design-skiplist--t3) — layered lists with random promotion, O(log n) expected [H]

### Backtracking

- [Subsets `🎯 T2`](algorithms/12-backtracking.md#subsets-power-set--t2) — Given distinct integers, return all subsets (the power set) [M]
- [Subsets II `🎯 T2`](algorithms/09-recursion.md#subsets-ii-lc-90--t2) — Input may contain duplicates; return only unique subsets [M]
- [Permutations `🎯 T2`](algorithms/12-backtracking.md#permutations--t2) — Given distinct integers, return all permutations [M]
- [Permutations II `🎯 T2`](algorithms/09-recursion.md#permutations-ii-lc-47--t2) — Input may contain duplicates; return only unique permutations [M]
- [Combinations `🎯 T2`](algorithms/09-recursion.md#combinations-lc-77--t2) — Return all combinations of k numbers from the range [1, n] [M]
- [Combination Sum `🎯 T2`](algorithms/12-backtracking.md#combination-sum-unbounded--t2) — Given distinct candidates and a target, return all unique combinations (with repetition) summing to target [M]
- [Combination Sum II `🎯 T2`](algorithms/12-backtracking.md#combination-sum-ii-01--no-reuse--t2) — Candidates may contain duplicates; each used at most once. Return unique combinations summing to target [M]
- [Combination Sum III `🎯 T2`](algorithms/12-backtracking.md#combination-sum-iii--t2) — Find all combinations of exactly k numbers from 1-9 that sum to target n. Each number used at most once, no duplicates in output [M]
- [Letter Combinations `🎯 T2`](algorithms/12-backtracking.md#letter-combinations-of-a-phone-number--t2) — Given digits 2–9, return all letter combinations the number could represent (phone keypad) [M]
- [Generate Parentheses `🎯 T2`](algorithms/12-backtracking.md#generate-parentheses--t2) — Generate all combinations of n pairs of well-formed parentheses [M]
- [Palindrome Partitioning `🎯 T2`](algorithms/12-backtracking.md#palindrome-partitioning--t2) — Partition string s such that every substring is a palindrome. Return all valid partitioning schemes [M]
- [Word Search `⚡ T1`](algorithms/09-recursion.md#word-search-grid-backtracking--t1) — Given a 2D board and a word, determine if the word exists as a path of adjacent non-revisiting cells [M]
- [Word Break II `🎯 T2`](algorithms/12-backtracking.md#word-break-ii--t2) — Given a string `s` and a dictionary, return all ways to segment `s` into space-separated dictionary words [M]
- [N-Queens `🎯 T2`](algorithms/12-backtracking.md#n-queens--t2) — Place n queens on an n×n board so no two queens attack each other. Return all valid configurations [H]
- [Unique Paths III `🎯 T2`](algorithms/12-backtracking.md#unique-paths-iii--t2) — Start at cell with value 1, reach cell with value 2, visiting every non-obstacle cell exactly once. Return count of such paths [H]
- [Target Sum `🎯 T2`](algorithms/12-backtracking.md#target-sum--t2) — Given an integer array and a target, assign `+` or `-` to each element and count the number of ways to reach target [M]
- [Pow(x, n) `🎯 T2`](algorithms/09-recursion.md#powx-n--fast-exponentiation) — Compute `x^n` efficiently; handle negative exponents [M]

### Dynamic Programming

- [Climbing Stairs `🎯 T2`](algorithms/15-dynamic-programming.md#climbing-stairs--t2) — Count distinct ways to climb n stairs, taking 1 or 2 steps at a time [E]
- [Min Cost Climbing Stairs `🎯 T2`](algorithms/15-dynamic-programming.md#min-cost-climbing-stairs--t2) — Each step has a cost. You can start from step 0 or 1. Pay cost to leave a step (+1 or +2). Minimize total cost to reach beyond the last step [E]
- [House Robber `🎯 T2`](algorithms/15-dynamic-programming.md#house-robber--t2) — Rob houses along a street; no two adjacent houses. Maximize money [M]
- [House Robber II `🎯 T2`](algorithms/15-dynamic-programming.md#house-robber-ii-circular--t2) — Houses in a circle — first and last are adjacent [M]
- [Decode Ways `🎯 T2`](algorithms/15-dynamic-programming.md#decode-ways--t2) — String of digits where A=1..Z=26. Count distinct decodings [M]
- [Word Break `🎯 T2`](algorithms/15-dynamic-programming.md#word-break--t2) — Given string s and a word dictionary, return true if s can be segmented into dictionary words [M]
- [Subset Sum `🎯 T2`](algorithms/15-dynamic-programming.md#subset-sum-problem--t2) — Determine if any subset of the array sums to a given target [M]
- [Partition Equal Subset Sum `🎯 T2`](algorithms/15-dynamic-programming.md#partition-equal-subset-sum--t2) — Can `nums` be split into two subsets with equal sum? [M]
- [Coin Change `🎯 T2`](algorithms/15-dynamic-programming.md#coin-change-min-coins--t2) — Fewest coins to make `amount`; return -1 if impossible [M]
- [Coin Change II `🎯 T2`](algorithms/15-dynamic-programming.md#coin-change-ii-total-ways--t2) — Count combinations (not permutations) of coins summing to `amount` [M]
- [Last Stone Weight II `⚡ T1`](algorithms/15-dynamic-programming.md#last-stone-weight-ii--t1) — Smash pairs of stones (losing the difference); minimize the last remaining stone weight [M]
- [Unique Paths `⚡ T1`](algorithms/15-dynamic-programming.md#unique-paths--t1) — Count distinct paths from top-left to bottom-right of m×n grid, moving only right or down [M]
- [Unique Paths II `🎯 T2`](algorithms/15-dynamic-programming.md#unique-paths-ii-with-obstacles--t2) — Unique paths but some cells are blocked (obstacle=1) [M]
- [Longest Increasing Subsequence `⚡ T1`](algorithms/15-dynamic-programming.md#longest-increasing-subsequence--t1) — Given an integer array `nums`, return the length of the longest strictly increasing subsequence [M]
- [Edit Distance `🎯 T2`](algorithms/15-dynamic-programming.md#edit-distance--t2) — Minimum insert/delete/replace operations to convert `word1` to `word2` [H]
- [Regular Expression Matching `🎯 T2`](algorithms/15-dynamic-programming.md#regular-expression-matching) — Given string `s` and pattern `p` with `'.'` (any single char) and `'*'` (zero or more of preceding element), implement full regex matching. Must match the entire string [H]
- [Interleaving String `🎯 T2`](algorithms/15-dynamic-programming.md#interleaving-string--t2) — Given `s1`, `s2`, `s3`, return true if `s3` is formed by an interleaving of `s1` and `s2` (LC 97) [M]
- [Palindrome Partitioning II `🎯 T2`](algorithms/12-backtracking.md#palindrome-partitioning-ii-minimum-cuts--t2) — Return the minimum number of cuts to partition a string so every substring is a palindrome [H]
- [Burst Balloons `🎯 T2`](algorithms/15-dynamic-programming.md#burst-balloons-lc-312--t2) — `n` balloons with values. Bursting balloon `i` scores `nums[i-1]*nums[i]*nums[i+1]`. Maximize total coins [H]
- [Best Time to Buy and Sell Stock II `⚡ T1`](algorithms/16-greedy.md#best-time-to-buy-and-sell-stock-ii-lc-122--t1) — Unlimited transactions; collect every positive day-to-day price difference [M]
- [Best Time to Buy and Sell Stock with Cooldown `🎯 T2`](algorithms/15-dynamic-programming.md#best-time-to-buy-and-sell-stock-with-cooldown-lc-309--t2) — After selling you must skip one day before buying again. Maximize profit (state-machine DP) [M]
- [Frog Jump (LC 403) `🎯 T2`](algorithms/15-dynamic-programming.md#frog-jump-lc-403--t2) — stone to set-of-last-jumps reachability [H]
- [Dungeon Game (LC 174) `🎯 T2`](algorithms/15-dynamic-programming.md#dungeon-game-lc-174--t2) — reverse-fill minimum starting health [H]
- [Cherry Pickup (LC 741) `💤 T3`](algorithms/15-dynamic-programming.md#cherry-pickup-lc-741--t3) — two simultaneous walkers on anti-diagonals [H]
- [Best Time to Buy and Sell Stock IV (LC 188) `🎯 T2`](algorithms/15-dynamic-programming.md#best-time-to-buy-and-sell-stock-iv-lc-188--t2) — hold/sold arrays over k transactions [H]
- [Wildcard Matching (LC 44) `🎯 T2`](algorithms/15-dynamic-programming.md#wildcard-matching-lc-44--t2) — 2-D DP where `*` is free-standing [H]
- [Smallest Sufficient Team (LC 1125) `💤 T3`](algorithms/15-dynamic-programming.md#smallest-sufficient-team-lc-1125--t3) — set-cover bitmask DP over skills [H]
- [Super Egg Drop (LC 887) `💤 T3`](algorithms/15-dynamic-programming.md#super-egg-drop-lc-887--t3) — flipped state: floors covered per number of moves [H]
- [Minimum Number of Refueling Stops (LC 871) `🎯 T2`](algorithms/15-dynamic-programming.md#minimum-number-of-refueling-stops-lc-871--t2) — max-heap greedy plus the DP view [H]
- [Minimum Cost to Cut a Stick (LC 1547) `🎯 T2`](algorithms/15-dynamic-programming.md#minimum-cost-to-cut-a-stick-lc-1547--t2) — interval DP over sorted cuts [H]
- [Strange Printer (LC 664) `💤 T3`](algorithms/15-dynamic-programming.md#strange-printer-lc-664--t3) — interval DP after compressing duplicates [H]
- [Predict the Winner / Stone Game (LC 486 / 877) `🎯 T2`](algorithms/15-dynamic-programming.md#predict-the-winner--stone-game-lc-486--877--t2) — minimax stored as score difference [M]
- [Stone Game II (LC 1140) `🎯 T2`](algorithms/15-dynamic-programming.md#stone-game-ii-lc-1140--t2) — memoized on `(i, M)` with suffix sums [M]
- [Numbers At Most N Given Digit Set (LC 902) `💤 T3`](algorithms/15-dynamic-programming.md#numbers-at-most-n-given-digit-set-lc-902--t3) — digit walk, shorter lengths free, tight prefix [H]
- [Count Numbers with Unique Digits (LC 357) `🎯 T2`](algorithms/15-dynamic-programming.md#count-numbers-with-unique-digits-lc-357--t2) — product recurrence by length [M]

### Union Find

- [Redundant Connection `⚡ T1`](data-structures/13-graph.md#redundant-connection--t1) — Given a tree of n nodes with one extra edge added (creating exactly one cycle), find the redundant edge. If multiple valid answers, return the last one in the input [M]
- [Graph Valid Tree `⚡ T1`](algorithms/14-union-find.md#graph-valid-tree--t1) — `n` nodes, list of undirected edges. Determine if the graph forms a valid tree [M]
- [Number of Provinces `⚡ T1`](data-structures/13-graph.md#number-of-provinces-lc-547--t1) — Given an n×n adjacency matrix `isConnected`, return the number of provinces (connected components of cities) [E]
- [Accounts Merge `⚡ T1`](algorithms/14-union-find.md#accounts-merge-email-graph--t1) — List of accounts `[name, email1, email2, ...]`. Merge accounts sharing at least one email. Return sorted merged accounts [M]
- [Number of Islands II `⚡ T1`](algorithms/14-union-find.md#number-of-islands-ii--t1) — Initially empty `m×n` grid. Receive `addLand(r, c)` operations. After each, return island count [H]

### Bit Manipulation

- [Single Number `⚡ T1`](algorithms/17-bit-manipulation.md#single-number--t1) — XOR cancellation [E]
- [Single Number II `🎯 T2`](algorithms/17-bit-manipulation.md#single-number-ii--t2) — ones/twos state machine [M]
- [Single Number III `🎯 T2`](algorithms/17-bit-manipulation.md#single-number-iii--t2) — split on a differing bit [M]
- [Missing Number `⚡ T1`](algorithms/17-bit-manipulation.md#missing-number--t1) — XOR indices and values [E]
- [Number of 1 Bits `⚡ T1`](algorithms/17-bit-manipulation.md#number-of-1-bits--t1) — Kernighan `n & (n-1)` [E]
- [Counting Bits `⚡ T1`](algorithms/17-bit-manipulation.md#counting-bits--t1) — bit DP, O(n) [E]
- [Power of Two / Power of Four `⚡ T1`](algorithms/17-bit-manipulation.md#power-of-two--power-of-four--t1) — `n & (n-1) == 0` plus a mask for 4 [E]
- [Reverse Bits `🎯 T2`](algorithms/17-bit-manipulation.md#reverse-bits--t2) — reverse a 32-bit value [E]
- [Sum of Two Integers `🎯 T2`](algorithms/17-bit-manipulation.md#sum-of-two-integers--t2) — add without `+`, 32-bit mask [M]
- [Bitwise AND of Numbers Range `🎯 T2`](algorithms/17-bit-manipulation.md#bitwise-and-of-numbers-range--t2) — common prefix [M]
- [Subsets via Bitmask Enumeration `⚡ T1`](algorithms/17-bit-manipulation.md#subsets-via-bitmask-enumeration--t1) — enumerate 2^n masks [M]
- [Gray Code `💤 T3`](algorithms/17-bit-manipulation.md#gray-code--t3) — `i ^ (i >> 1)` [M]
- [Minimum Flips to Make a OR b Equal to c `🎯 T2`](algorithms/17-bit-manipulation.md#minimum-flips-to-make-a-or-b-equal-to-c--t2) — per-bit cases [M]
- [Maximum XOR of Two Numbers in an Array `⚡ T1`](algorithms/17-bit-manipulation.md#maximum-xor-of-two-numbers-in-an-array--t1) — prefix-set greedy; trie variant in the trie file [H]

### Math & Number Theory

- [Reverse Integer `🎯 T2`](algorithms/18-math-and-number-theory.md#reverse-integer--t2) — 0 on 32-bit overflow [M]
- [Plus One `⚡ T1`](algorithms/18-math-and-number-theory.md#plus-one--t1) — digit-array increment [E]
- [Multiply Strings `⚡ T1`](algorithms/18-math-and-number-theory.md#multiply-strings--t1) — no big-int conversion [M]
- [Add Binary `⚡ T1`](algorithms/18-math-and-number-theory.md#add-binary--t1) — carry [E]
- [Excel Sheet Column Number and Title `🎯 T2`](algorithms/18-math-and-number-theory.md#excel-sheet-column-number-and-title--t2) — bijective base-26 [E]
- [Count Primes `🎯 T2`](algorithms/18-math-and-number-theory.md#count-primes--t2) — sieve [M]
- [Factorial Trailing Zeroes `🎯 T2`](algorithms/18-math-and-number-theory.md#factorial-trailing-zeroes--t2) — count factors of 5 [M]
- [Fraction to Recurring Decimal (with GCD/LCM) `🎯 T2`](algorithms/18-math-and-number-theory.md#fraction-to-recurring-decimal-with-gcdlcm--t2) — remainder map [M]
- [Modular Exponentiation and nCr mod p `🎯 T2`](algorithms/18-math-and-number-theory.md#modular-exponentiation-and-ncr-mod-p--t2) — Fermat inverse; Pow(x, n) is under Backtracking [M]
- [Rectangle Overlap and Rectangle Area `🎯 T2`](algorithms/18-math-and-number-theory.md#rectangle-overlap-and-rectangle-area--t2) — interval overlap [M]
- [Detect Squares `⚡ T1`](algorithms/18-math-and-number-theory.md#detect-squares--t1) — design with point counts [M]
- [Max Points on a Line `🎯 T2`](algorithms/18-math-and-number-theory.md#max-points-on-a-line--t2) — gcd-normalized slope [H]
- [Implement Rand10 Using Rand7 `🎯 T2`](algorithms/18-math-and-number-theory.md#implement-rand10-using-rand7--t2) — rejection sampling [M]
- [Random Point in Circle `💤 T3`](algorithms/18-math-and-number-theory.md#random-point-in-circle--t3) — rejection / polar sqrt [M]
- [Sqrt(x) and Valid Perfect Square `🎯 T2`](algorithms/18-math-and-number-theory.md#sqrtx-and-valid-perfect-square--t2) — binary search on answer [E]

### Range Queries

- [Range Sum Query - Immutable `⚡ T1`](algorithms/19-range-queries.md#range-sum-query---immutable--t1) — prefix sums; O(1) query after O(n) build [E]
- [Range Sum Query 2D - Immutable `⚡ T1`](algorithms/19-range-queries.md#range-sum-query-2d---immutable--t1) — 2D prefix sums; inclusion-exclusion rectangle query [M]
- [Range Sum Query - Mutable `🎯 T2`](algorithms/19-range-queries.md#range-sum-query---mutable--t2) — Fenwick or iterative segment tree; point update + range sum [M]
- [Count of Smaller Numbers After Self `🎯 T2`](algorithms/19-range-queries.md#count-of-smaller-numbers-after-self--t2) — Fenwick over compressed ranks, or merge sort on indices [H]
- [Reverse Pairs `🎯 T2`](algorithms/19-range-queries.md#reverse-pairs--t2) — merge sort; count cross pairs before merging [H]
- [Count of Range Sum `💤 T3`](algorithms/19-range-queries.md#count-of-range-sum--t3) — prefix sums + Fenwick over compressed prefixes [H]
- [The Skyline Problem `🎯 T2`](algorithms/19-range-queries.md#the-skyline-problem--t2) — sweep line with max-heap and lazy expiry [H]
- [My Calendar I `⚡ T1`](algorithms/19-range-queries.md#my-calendar-i--t1) — sorted list + bisect neighbour check [M]
- [My Calendar II `🎯 T2`](algorithms/19-range-queries.md#my-calendar-ii--t2) — track booked and double-booked intervals [M]
- [My Calendar III `🎯 T2`](algorithms/19-range-queries.md#my-calendar-iii--t2) — boundary-delta sweep; dynamic segment tree for scale [H]
- [Range Module `💤 T3`](algorithms/19-range-queries.md#range-module--t3) — disjoint sorted intervals with bisect splice [H]
- [Falling Squares `💤 T3`](algorithms/19-range-queries.md#falling-squares--t3) — O(n^2) overlap scan; segment tree if large [H]
- [Sliding Window Median `🎯 T2`](algorithms/19-range-queries.md#sliding-window-median--t2) — two heaps with lazy deletion, or sorted window [H]
- [Create Sorted Array through Instructions `💤 T3`](algorithms/19-range-queries.md#create-sorted-array-through-instructions--t3) — Fenwick counts of smaller/larger values [H]
