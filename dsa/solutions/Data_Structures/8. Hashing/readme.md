# Hashing Overview

Hashing provides O(1) average time complexity for lookups, insertions, and deletions using a hash function to map keys to indices.

## Topics Covered

### 1. Hash Map (Dictionary)
- **Key-Value Store**: Map unique keys to values.
- **Handling Collisions**: Chaining (Linked Lists) or Open Addressing (Probing).
- **Time Complexity**: O(1) average, O(n) worst case.

### 2. Hash Set
- **Unique Collection**: Store unique elements for O(1) membership check.

---

## Problems & Solutions

### Easy
1. **[Two Sum](Easy/two_sum.py)**
   - Find indices of two numbers summing to target.
2. **[Contains Duplicate](Easy/contains_duplicate.py)**
   - Check if array contains duplicates (HashSet).
3. **[Valid Anagram](Easy/valid_anagram.py)**
   - Check if two strings have same character counts.

### Medium
1. **[Group Anagrams](Medium/group_anagrams.py)**
   - Group strings that are anagrams of each other.
2. **[Top K Frequent Elements](Medium/top_k_frequent.py)**
   - Find k most frequent items (Bucket Sort / Heap).
3. **[Longest Consecutive Sequence](Medium/longest_consecutive.py)**
   - Find longest sequence in unsorted array (HashSet).
4. **[Subarray Sum Equals K](Medium/subarray_sum_k.py)**
   - Count subarrays with sum `k` (Prefix Sum + Map).
5. **[LRU Cache](Medium/lru_cache.py)**
   - Least Recently Used eviction policy (HashMap + Doubly Linked List).

---

## Tips for Interviews
- **Duplicates/Membership**: Use a HashSet (O(1)).
- **Frequency Counting**: Use a HashMap (Counter).
- **Pair Finding**: Store complements in HashMap (e.g., Two Sum).
- **Caching**: HashMap is the core of most caches (LRU/LFU).
