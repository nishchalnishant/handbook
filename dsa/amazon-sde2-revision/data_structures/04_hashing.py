"""
Hashing (Hash Maps & Sets) patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Using mutable objects (like lists or sets) as dictionary keys (Python will throw a TypeError). Use tuples instead.\n- Iterating over a dictionary while modifying its size.\n- Assuming order is maintained (Python 3.7+ keeps insertion order, but conceptually hash maps are unordered).

Common Variants:
- Two Sum (Store complements)\n- Frequency Maps (Anagrams, Majority Element)\n- Caching / Memoization\n- Design Hashmap/Hashset

General Tips & Best Practices:
- Use `collections.defaultdict` to avoid key errors.\n- Use `collections.Counter` for counting elements quickly.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List
from collections import Counter, defaultdict
import heapq
import random

class HashingSolutions:
    # -----------------------------------------------------------------------
    # 1. Two Sum (LC 1) — T1
    # Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.
    # Example: nums = [2,7,11,15], target = 9 → [0,1]
    # Constraints: 2 <= nums.length <= 10^4, 10^9 <= nums[i] <= 10^9, 10^9 <= target <= 10^9, Only one valid answer exists, Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Map to store number to its index
        seen = {}
        for i, num in enumerate(nums):
            # Check if complement exists in seen map
            if target - num in seen:
                return [seen[target - num], i]
            # Record current number and its index
            seen[num] = i
        return []

    # -----------------------------------------------------------------------
    # 2. Group Anagrams (LC 49) — T1
    # Given an array of strings strs, group the anagrams together. You can return the answer in any order.
    # Example: strs = ["eat","tea","tan","ate","nat","bat"] → [["bat"],["nat","tan"],["ate","eat","tea"]]
    # Constraints: 1 <= strs.length <= 10^4, 0 <= strs[i].length <= 100, strs[i] consists of lowercase English letters
    # Time: O(n * k log k), Space: O(n * k)
    # -----------------------------------------------------------------------
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Map from sorted tuple key to list of anagram strings
        groups = defaultdict(list)
        for s in strs:
            # Sort characters to form key
            key = tuple(sorted(s))
            groups[key].append(s)
        return list(groups.values())

    # -----------------------------------------------------------------------
    # 3. Top K Frequent Elements (LC 347) — T1
    # Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
    # Example: nums = [1,1,1,2,2,3], k = 2 → [1,2]
    # Constraints: 1 <= nums.length <= 10^5, 10^4 <= nums[i] <= 10^4, k is in the range [1, the number of unique elements in the array], It is guaranteed that the answer is unique, Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's, size
    # Time: O(n log k), Space: O(n)
    # -----------------------------------------------------------------------
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        # O(N log K) using heap
        return heapq.nlargest(k, count.keys(), key=count.get)

    # -----------------------------------------------------------------------
    # 4. Valid Anagram (LC 242) — T1
    # Given two strings s and t, return true if t is an anagram of s, and false otherwise.
    # Example: s = "anagram", t = "nagaram" → true
    # Constraints: 1 <= s.length, t.length <= 5 * 10^4, s and t consist of lowercase English letters, Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such, a case?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def isAnagram(self, s: str, t: str) -> bool:
        # Anagrams must be of equal length
        if len(s) != len(t): 
            return False
        # Compare character frequency counts
        return Counter(s) == Counter(t)

    # -----------------------------------------------------------------------
    # 5. Longest Consecutive Sequence (LC 128) — T1
    # Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence. You must write an algorithm that runs in O(n) time.
    # Example: nums = [100,4,200,1,3,2] → 4
    # Constraints: 0 <= nums.length <= 10^5, 10^9 <= nums[i] <= 10^9
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0

        for num in num_set:
            # Check if this is the start of a sequence
            if num - 1 not in num_set:
                length = 1
                while num + length in num_set:
                    length += 1
                longest = max(longest, length)
        return longest

    # -----------------------------------------------------------------------
    # 6. Subarray Sum Equals K (LC 560) — T1
    # Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k. A subarray is a contiguous non-empty sequence of elements within an array.
    # Example: nums = [1,1,1], k = 2 → 2
    # Constraints: 1 <= nums.length <= 2 * 10^4, 1000 <= nums[i] <= 1000, 10^7 <= k <= 10^7
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        curr_sum = 0
        # Map to store frequency of prefix sums, initialized with base case sum 0
        prefix_sums = {0: 1}
        for num in nums:
            # Add current number to running prefix sum
            curr_sum += num
            # Check if prefix sum that can form subarray of sum k exists
            if curr_sum - k in prefix_sums:
                count += prefix_sums[curr_sum - k]
            # Record frequency of current prefix sum
            prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1
        return count

class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    # -----------------------------------------------------------------------
    # 1. LRU Cache (LC 146) — T2
    # Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement the LRUCache class: key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key. The functions get and put must each run in O(1) average time complexity.
    # Constraints: 1 <= capacity <= 3000, 0 <= key <= 10^4, 0 <= value <= 10^5, At most 2 * 10^5 calls will be made to get and put
    # Time: O(1), Space: O(capacity)
    # -----------------------------------------------------------------------
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} # map key to node

        # Left=LRU, Right=most recent
        self.left, self.right = Node(0, 0), Node(0, 0)
        self.left.next, self.right.prev = self.right, self.left

    # Time: O(1), Space: O(1)
    def remove(self, node):
        """Removes a value from the underlying data structure when present."""
        # Unlink node by updating its neighbors' pointers
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    # Time: O(1), Space: O(1)
    def insert(self, node):
        """Inserts a value into the underlying data structure."""
        # Insert node just before the right sentinel node
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    # Time: O(1), Space: O(1)
    def get(self, key: int) -> int:
        # Check if key is present in cache
        if key in self.cache:
            # Make the node the most recently used: remove then insert at tail
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            # Return cached value
            return self.cache[key].val
        # Key not found
        return -1

    # Time: O(1), Space: O(1)
    def put(self, key: int, value: int) -> None:
        """Stores or updates the value associated with the requested key."""
        # Remove old node if key already exists
        if key in self.cache:
            self.remove(self.cache[key])
        # Create and insert the new node
        self.cache[key] = Node(key, value)
        self.insert(self.cache[key])

        # Evict least recently used key if capacity is exceeded
        if len(self.cache) > self.cap:
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]

class HashingSolutionsT2:
    # -----------------------------------------------------------------------
    # 2. Ransom Note (LC 383) — T2
    # Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise. Each letter in magazine can only be used once in ransomNote.
    # Example: ransomNote = "a", magazine = "b" → false
    # Constraints: 1 <= ransomNote.length, magazine.length <= 10^5, ransomNote and magazine consist of lowercase English letters
    # Time: O(n + m), Space: O(1)
    # -----------------------------------------------------------------------
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        # Get character counts for magazine
        count_mag = Counter(magazine)
        # Get character counts for ransomNote
        count_ran = Counter(ransomNote)
        # Verify that magazine provides enough of each required character
        for c in count_ran:
            if count_mag[c] < count_ran[c]:
                return False
        return True

    # -----------------------------------------------------------------------
    # 3. 4Sum II (LC 454) — T2
    # Given four integer arrays nums1, nums2, nums3, and nums4 all of length n, return the number of tuples (i, j, k, l) such that:
    # Example: nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2] → 2
    # Constraints: n == nums1.length, n == nums2.length, n == nums3.length, n == nums4.length, 1 <= n <= 200, 2^28 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 2^28
    # Time: O(n^2), Space: O(n^2)
    # -----------------------------------------------------------------------
    def fourSumCount(self, nums1: List[int], nums2: List[int], nums3: List[int], nums4: List[int]) -> int:
        # Frequency map for sums from first two arrays
        countMap = defaultdict(int)
        for a in nums1:
            for b in nums2:
                countMap[a + b] += 1

        # Count total tuples that sum to 0
        res = 0
        for c in nums3:
            for d in nums4:
                # Accumulate matching negated sum count
                res += countMap[-(c + d)]
        return res

class RandomizedSet:
    # -----------------------------------------------------------------------
    # 4. Insert Delete GetRandom O(1) (LC 380) — T2
    # Implement the RandomizedSet class: not present, false otherwise. present, false otherwise. least one element exists when this method is called). Each element must have the same probability of being returned. You must implement the functions of the class such that each function works in average O(1) time complexity.
    # Constraints: 2^31 <= val <= 2^31 - 1, At most 2 * 10^5 calls will be made to insert, remove, and getRandom, There will be at least one element in the data structure when getRandom is called
    # Time: O(1), Space: O(n)
    # -----------------------------------------------------------------------
    def __init__(self):
        self.numMap = {}
        self.numList = []

    # Time: O(1), Space: O(1)
    def insert(self, val: int) -> bool:
        """Inserts a value into the underlying data structure."""
        # Return False if the value is already present
        if val in self.numMap:
            return False
        # Record the index of the newly added value
        self.numMap[val] = len(self.numList)
        self.numList.append(val)
        return True

    # Time: O(1), Space: O(1)
    def remove(self, val: int) -> bool:
        """Removes a value from the underlying data structure when present."""
        # Return False if value is not in set
        if val not in self.numMap:
            return False
        idx = self.numMap[val]
        lastVal = self.numList[-1]
        # Move the last element to the slot of the deleted element
        self.numList[idx] = lastVal
        self.numList.pop()
        # Update index mapping for the swapped element
        self.numMap[lastVal] = idx
        del self.numMap[val]
        return True

    # Time: O(1), Space: O(1)
    
    def getRandom(self) -> int:
        return random.choice(self.numList)

class HashingSolutionsAdditional:
    # -----------------------------------------------------------------------
    # 7. Subarrays with K Different Integers (LC 992) — T1
    # Given an integer array nums and an integer k, return the number of good subarrays of nums. A good array is an array where the number of different integers in that array is exactly k. A subarray is a contiguous part of an array.
    # Example: nums = [1,2,1,2,3], k = 2 → 7
    # Constraints: 1 <= nums.length <= 2 * 10^4, 1 <= nums[i], k <= nums.length
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        def atMost(k):
            from collections import defaultdict
            count = defaultdict(int)
            res = 0
            l = 0
            # Expand right boundary of window
            for r in range(len(nums)):
                if count[nums[r]] == 0:
                    k -= 1
                count[nums[r]] += 1
                # Shrink left boundary of window if distinct values exceed k
                while k < 0:
                    count[nums[l]] -= 1
                    if count[nums[l]] == 0:
                        k += 1
                    l += 1
                # Add count of valid subarrays ending at r
                res += r - l + 1
            return res
        # Return exactly k as difference of atMost(k) and atMost(k-1)
        return atMost(k) - atMost(k - 1)

    # -----------------------------------------------------------------------
    # 8. Subarray Sums Divisible by K (LC 974) — T2
    # Given an integer array nums and an integer k, return the number of non-empty subarrays that have a sum divisible by k. A subarray is a contiguous part of an array.
    # Example: nums = [4,5,0,-2,-3,1], k = 5 → 7
    # Constraints: 1 <= nums.length <= 3 * 10^4, 10^4 <= nums[i] <= 10^4, 2 <= k <= 10^4
    # Time: O(n), Space: O(k)
    # -----------------------------------------------------------------------
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        # Map from remainder to its frequency, initialized with remainder 0
        count = {0: 1}
        prefix_sum = 0
        res = 0
        for num in nums:
            prefix_sum += num
            # Calculate remainder modulo k
            mod = prefix_sum % k
            # Add frequency of the matching prefix sum remainder
            if mod in count:
                res += count[mod]
                count[mod] += 1
            else:
                count[mod] = 1
        return res

    # -----------------------------------------------------------------------
    # 9. Continuous Subarray Sum (LC 523) — T2
    # Given an integer array nums and an integer k, return true if nums has a good subarray or false otherwise. A good subarray is a subarray where: Note that: multiple of k.
    # Example: nums = [23,2,4,6,7], k = 6 → true
    # Constraints: 1 <= nums.length <= 10^5, 0 <= nums[i] <= 10^9, 0 <= sum(nums[i]) <= 2^31 - 1, 1 <= k <= 2^31 - 1
    # Time: O(n), Space: O(k)
    # -----------------------------------------------------------------------
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        # Map from remainder to the earliest index it occurred
        rem_map = {0: -1}
        total = 0
        for i, n in enumerate(nums):
            total += n
            r = total % k
            # Store first index where remainder is seen
            if r not in rem_map:
                rem_map[r] = i
            # Check if index gap is at least 2
            elif i - rem_map[r] > 1:
                return True
        return False

    # -----------------------------------------------------------------------
    # 10. Max Number of K-Sum Pairs (LC 1679) — T2
    # You are given an integer array nums and an integer k. In one operation, you can pick two numbers from the array whose sum equals k and remove them from the array. Return the maximum number of operations you can perform on the array.
    # Example: nums = [1,2,3,4], k = 5 → 2
    # Constraints: 1 <= nums.length <= 10^5, 1 <= nums[i] <= 10^9, 1 <= k <= 10^9
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def maxOperations(self, nums: List[int], k: int) -> int:
        from collections import defaultdict
        # Count frequency of each number
        count = defaultdict(int)
        res = 0
        for num in nums:
            # Check if complement has a positive frequency
            if count[k - num] > 0:
                res += 1
                count[k - num] -= 1
            else:
                count[num] += 1
        return res

    # -----------------------------------------------------------------------
    # 11. Contiguous Array (LC 525) — T2
    # Given a binary array nums, return the maximum length of a contiguous subarray with an equal number of 0 and 1.
    # Example: nums = [0,1] → 2
    # Constraints: 1 <= nums.length <= 10^5, nums[i] is either 0 or 1
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def findMaxLength(self, nums: List[int]) -> int:
        count = 0
        res = 0
        # Map prefix sum difference (1s count - 0s count) to earliest index
        count_map = {0: -1}
        for i, num in enumerate(nums):
            # Treat 1 as +1 and 0 as -1
            count += 1 if num == 1 else -1
            if count in count_map:
                # Update max length when running count returns to a previously seen state
                res = max(res, i - count_map[count])
            else:
                count_map[count] = i
        return res

    # -----------------------------------------------------------------------
    # 12. Make Sum Divisible by P (LC 1590) — T2
    # Given an array of positive integers nums, remove the smallest subarray (possibly empty) such that the sum of the remaining elements is divisible by p. It is not allowed to remove the whole array. Return the length of the smallest subarray that you need to remove, or -1 if it's impossible. A subarray is defined as a contiguous block of elements in the array.
    # Example: nums = [3,1,4,2], p = 6 → 1
    # Constraints: 1 <= nums.length <= 10^5, 1 <= nums[i] <= 10^9, 1 <= p <= 10^9
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def minSubarray(self, nums: List[int], p: int) -> int:
        total = sum(nums)
        rem = total % p
        # If total sum is already divisible by p, return 0
        if rem == 0:
            return 0

        res = len(nums)
        cur = 0
        # Map prefix sum mod p to latest index
        rem_map = {0: -1}

        for i, num in enumerate(nums):
            cur = (cur + num) % p
            target = (cur - rem + p) % p
            # Check if target remainder prefix sum has been seen
            if target in rem_map:
                res = min(res, i - rem_map[target])
            # Store current index (we want the shortest, so overwrite to keep latest)
            rem_map[cur] = i

        return res if res < len(nums) else -1

class HashingSolutionsL4:
    # LC 205 — Isomorphic Strings
    # Details: Given two strings s and t, determine if they are isomorphic.
    # Two strings s and t are isomorphic if the characters in s can be replaced to get t.
    # All occurrences of a character must be replaced with another character while preserving
    # the order of characters. No two characters may map to the same character, but a character
    # may map to itself.
    # Example 1: s = "egg", t = "add" -> True
    # Example 2: s = "foo", t = "bar" -> False
    # Example 3: s = "paper", t = "title" -> True
    # Constraints: 1 <= s.length <= 5 * 10^4, s and t consist of any valid ASCII characters.
    # Time: O(n), Space: O(1) (bounded alphabet)
    """imp"""
    def isIsomorphic(self, s: str, t: str) -> bool:
        """Isomorphic Strings (LC 205). O(n)."""
        s_to_t = {}
        t_to_s = {}
        # Iterate over character pairs of both strings
        for cs, ct in zip(s, t):
            # Check mapping bijection consistency
            if s_to_t.get(cs, ct) != ct or t_to_s.get(ct, cs) != cs:
                return False
            s_to_t[cs] = ct
            t_to_s[ct] = cs
        return True

    # LC 290 — Word Pattern
    # Details: Given a pattern and a string s, find if s follows the same pattern.
    # "Follows" means a full match, such that there is a bijection between a letter in pattern
    # and a non-empty word in s.
    # Example 1: pattern = "abba", s = "dog cat cat dog" -> True
    # Example 2: pattern = "abba", s = "dog cat cat fish" -> False
    # Example 3: pattern = "aaaa", s = "dog cat cat dog" -> False
    # Constraints: 1 <= pattern.length <= 300, s contains only lowercase English letters and spaces.
    # Time: O(n), Space: O(n)
    """imp"""
    def wordPattern(self, pattern: str, s: str) -> bool:
        """Word Pattern (LC 290). O(n)."""
        words = s.split()
        # Word count must match pattern character count
        if len(pattern) != len(words):
            return False
        c_to_w = {}
        w_to_c = {}
        # Verify bijection between characters and words
        for c, w in zip(pattern, words):
            if c_to_w.get(c, w) != w or w_to_c.get(w, c) != c:
                return False
            c_to_w[c] = w
            w_to_c[w] = c
        return True

    # LC 609 — Find Duplicate File in System
    # Details: Given a list of directory info strings in the format
    # "root/d1/d2/.../dm f1.txt(f1_content) f2.txt(f2_content) ..."
    # return all groups of duplicate files (same content). A group must contain at least
    # two files.
    # Example: paths = ["root/a 1.txt(abcd) 2.txt(efgh)", "root/c 3.txt(abcd)"]
    # Output: [["root/a/1.txt","root/c/3.txt"]]
    # Constraints: 1 <= paths.length <= 2 * 10^4, each path string is valid.
    # Time: O(N) where N = total characters across all paths, Space: O(N)
    def findDuplicate(self, paths: List[str]) -> List[List[str]]:
        content_map = defaultdict(list)
        # Parse all path inputs
        for path in paths:
            parts = path.split()
            directory = parts[0]
            # Parse file name and content for each file entry
            for file_entry in parts[1:]:
                fname, content = file_entry.split('(')
                content = content[:-1]  # strip trailing ')'
                content_map[content].append(directory + '/' + fname)
        # Return only groups with at least two duplicate files
        return [v for v in content_map.values() if len(v) > 1]

    # LC 692 — Top K Frequent Words
    # Details: Given an array of strings words and an integer k, return the k most frequent
    # words. Return the answer sorted by frequency from highest to lowest. Words with the same
    # frequency should be sorted lexicographically.
    # Example 1: words = ["i","love","leetcode","i","love","coding"], k = 2 -> ["i","love"]
    # Example 2: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
    #            -> ["the","is","sunny","day"]
    # Constraints: 1 <= words.length <= 500, 1 <= words[i].length <= 10, words[i] is lowercase.
    # Time: O(n log k), Space: O(n)
    def topKFrequentWords(self, words: List[str], k: int) -> List[str]:
        """Top K Frequent Words (LC 692). O(n log k)."""
        # Count frequency of words
        count = Counter(words)
        # Sort keys by descending frequency and ascending lexicographical order
        return sorted(count.keys(), key=lambda w: (-count[w], w))[:k]



    # LC 554 — Brick Wall
    # Details: Given a rectangular brick wall represented as a list of rows (each row is a list
    # of brick widths), find a vertical line that crosses the fewest bricks. The line must not
    # cross the leftmost or rightmost edge. Return the minimum number of crossed bricks.
    # Example: wall = [[1,2,2,1],[3,1,2],[1,3,2],[2,4],[3,1,2],[1,3,1,1]] -> 2
    # Constraints: 1 <= wall.length <= 10^4, sum of each row is the same positive integer.
    # Time: O(n) where n = total bricks, Space: O(W) where W = wall width
    """imp"""
    def leastBricks(self, wall: List[List[int]]) -> int:
        """Brick Wall (LC 554). O(n) where n = total bricks."""
        gap_count = defaultdict(int)
        # Compute and record frequency of gap boundaries across brick rows
        for row in wall:
            pos = 0
            for brick in row[:-1]:  # exclude last brick to avoid right edge
                pos += brick
                gap_count[pos] += 1
        # Minimizing brick cuts is equivalent to maximizing gaps
        max_gaps = max(gap_count.values(), default=0)
        return len(wall) - max_gaps

    # LC 447 — Number of Boomerangs
    # Details: Given n points on a 2D plane, return the number of boomerangs. A boomerang is
    # a tuple (i, j, k) such that the distance from i to j equals the distance from i to k
    # (order of j and k matters).
    # Example: points = [[0,0],[1,0],[2,0]] -> 2
    # Constraints: n == points.length, 1 <= n <= 500, -10^4 <= points[i] <= 10^4.
    # Time: O(n^2), Space: O(n)
    """imp"""
    def numberOfBoomerangs(self, points: List[List[int]]) -> int:
        res = 0
        # Treat each point as a pivot
        for i, (x1, y1) in enumerate(points):
            dist_count = defaultdict(int)
            # Find squared Euclidean distances to all other points
            for j, (x2, y2) in enumerate(points):
                if i == j:
                    continue
                d = (x1 - x2) ** 2 + (y1 - y2) ** 2
                dist_count[d] += 1
            # Add count of permutations for each distance group
            for c in dist_count.values():
                res += c * (c - 1)
        return res

    # LC 890 — Find and Replace Pattern
    # Details: Given a list of strings words and a string pattern, return a list of words that
    # match the pattern. A word matches the pattern if there is a bijection between each letter
    # of the pattern and each letter in the word (same bijection rules as isomorphic strings).
    # Example: words = ["abc","deq","mee","aqq","dkd","ccc"], pattern = "abb"
    #          -> ["mee","aqq"]
    # Constraints: 1 <= pattern.length <= 20, all strings have the same length, lowercase only.
    # Time: O(N * L) where N = len(words), L = len(pattern), Space: O(L)
    def findAndReplacePattern(self, words: List[str], pattern: str) -> List[str]:
        """Find and Replace Pattern (LC 890). O(N * L) where N = len(words)."""
        def matches(word: str) -> bool:
            w_to_p, p_to_w = {}, {}
            # Verify bijection between word character and pattern character
            for wc, pc in zip(word, pattern):
                if w_to_p.get(wc, pc) != pc or p_to_w.get(pc, wc) != wc:
                    return False
                w_to_p[wc] = pc
                p_to_w[pc] = wc
            return True
        # Filter words matching pattern
        return [w for w in words if matches(w)]

    # LC 599 — Minimum Index Sum of Two Lists
    # Details: Given two arrays of strings list1 and list2, find all strings that appear in
    # both lists with the minimum index sum (index in list1 + index in list2). Return those
    # strings. If there is a tie, return all of them in any order.
    # Example: list1 = ["Shogun","Tapioca Express","Burger King","KFC"],
    #          list2 = ["Piatti","The Grill at Torrey Pines","Hungry Hunter Steakhouse","Shogun"]
    #          -> ["Shogun"]
    # Constraints: 1 <= list1.length, list2.length <= 1000, strings are lowercase English letters.
    # Time: O(n + m), Space: O(n)
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        """Minimum Index Sum of Two Lists (LC 599). O(n + m)."""
        # Map restaurant name to its index in list1
        index_map = {s: i for i, s in enumerate(list1)}
        res = []
        min_sum = float('inf')
        # Iterate over list2 and calculate index sums
        for j, s in enumerate(list2):
            if s in index_map:
                total = index_map[s] + j
                # Update minimum index sum and result list
                if total < min_sum:
                    min_sum = total
                    res = [s]
                elif total == min_sum:
                    res.append(s)
        return res


# LC 359 — Logger Rate Limiter (standalone class)
class Logger:
    def __init__(self):
        """Logger Rate Limiter (standalone class) (LC 359). Time: O(1) per call, Space: O(n) where n = distinct messages seen."""
        self._last_printed = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        # Check if enough time has passed since the last print of the message
        if timestamp - self._last_printed.get(message, float('-inf')) >= 10:
            self._last_printed[message] = timestamp
            return True
        return False


# Standalone class implementations for Design HashMap and Design HashSet (LC 706 / LC 705)
class MyHashMap:
    def __init__(self):
        """Design HashMap (LC 706). Time: O(n/k) average per operation, Space: O(n + k)."""
        self.size = 1009
        self.buckets = [[] for _ in range(self.size)]

    def _bucket(self, key):
        return self.buckets[key % self.size]

    def put(self, key: int, value: int) -> None:
        """Stores or updates the value associated with the requested key."""
        chain = self._bucket(key)
        # Update if key already exists in the chain
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        # Otherwise append new key-value pair to bucket chain
        chain.append((key, value))

    def get(self, key: int) -> int:
        """Returns the value associated with the requested key or index."""
        # Find key in the matching hash bucket chain
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        """Removes a value from the underlying data structure when present."""
        chain = self._bucket(key)
        # Delete entry if key exists in bucket chain
        for i, (k, v) in enumerate(chain):
            if k == key:
                del chain[i]
                return


class MyHashSet:
    def __init__(self):
        """Design HashSet (LC 705). Time: O(n/k) average per operation, Space: O(n + k)."""
        self.size = 1009
        self.buckets = [[] for _ in range(self.size)]

    def _bucket(self, key):
        return self.buckets[key % self.size]

    def add(self, key: int) -> None:
        """Adds a value to the underlying data structure."""
        chain = self._bucket(key)
        # Add key if it is not already in the bucket chain
        if key not in chain:
            chain.append(key)

    def contains(self, key: int) -> bool:
        # Check if key is present in matching bucket chain
        return key in self._bucket(key)

    def remove(self, key: int) -> None:
        """Removes a value from the underlying data structure when present."""
        chain = self._bucket(key)
        # Remove key from chain if it exists
        if key in chain:
            chain.remove(key)


if __name__ == "__main__":
    sol = HashingSolutions()
    sol2 = HashingSolutionsT2()
    sol3 = HashingSolutionsAdditional()
    sol4 = HashingSolutionsL4()

    # twoSum
    assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert sol.twoSum([3, 2, 4], 6) == [1, 2]

    # groupAnagrams
    res = sol.groupAnagrams(["eat","tea","tan","ate","nat","bat"])
    assert sorted([sorted(g) for g in res]) == [["ate","eat","tea"],["bat"],["nat","tan"]]

    # topKFrequent
    assert sorted(sol.topKFrequent([1,1,1,2,2,3], 2)) == [1, 2]

    # isAnagram
    assert sol.isAnagram("anagram", "nagaram") == True
    assert sol.isAnagram("rat", "car") == False

    # longestConsecutive
    assert sol.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert sol.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9

    # subarraySum
    assert sol.subarraySum([1, 1, 1], 2) == 2
    assert sol.subarraySum([1, 2, 3], 3) == 2

    # LRUCache
    lru = LRUCache(2)
    lru.put(1, 1); lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3)
    assert lru.get(2) == -1

    # canConstruct
    assert sol2.canConstruct("a", "b") == False
    assert sol2.canConstruct("aa", "aab") == True

    # fourSumCount
    assert sol2.fourSumCount([1,2],[-2,-1],[-1,2],[0,2]) == 2

    # RandomizedSet
    rs = RandomizedSet()
    assert rs.insert(1) == True
    assert rs.insert(1) == False
    assert rs.remove(2) == False
    assert rs.insert(2) == True
    val = rs.getRandom()
    assert val in [1, 2]
    assert rs.remove(1) == True
    assert rs.getRandom() == 2

    # subarraysWithKDistinct
    assert sol3.subarraysWithKDistinct([1,2,1,2,3], 2) == 7
    assert sol3.subarraysWithKDistinct([1,2,1,3,4], 3) == 3

    # subarraysDivByK
    assert sol3.subarraysDivByK([4, 5, 0, -2, -3, 1], 5) == 7

    # checkSubarraySum (multiple of k, length >= 2)
    assert sol3.checkSubarraySum([23, 2, 4, 6, 7], 6) == True
    assert sol3.checkSubarraySum([23, 2, 6, 4, 7], 13) == False

    # maxOperations
    assert sol3.maxOperations([1, 2, 3, 4], 5) == 2
    assert sol3.maxOperations([3, 1, 3, 4, 3], 6) == 1

    # findMaxLength (equal 0 and 1)
    assert sol3.findMaxLength([0, 1]) == 2
    assert sol3.findMaxLength([0, 1, 0]) == 2

    # isIsomorphic (LC 205)
    assert sol4.isIsomorphic("egg", "add") == True
    assert sol4.isIsomorphic("foo", "bar") == False
    assert sol4.isIsomorphic("paper", "title") == True
    assert sol4.isIsomorphic("ab", "aa") == False

    # wordPattern (LC 290)
    assert sol4.wordPattern("abba", "dog cat cat dog") == True
    assert sol4.wordPattern("abba", "dog cat cat fish") == False
    assert sol4.wordPattern("aaaa", "dog cat cat dog") == False

    # findDuplicate (LC 609)
    dup_res = sol4.findDuplicate(["root/a 1.txt(abcd) 2.txt(efgh)", "root/c 3.txt(abcd)"])
    assert len(dup_res) == 1
    assert sorted(dup_res[0]) == ["root/a/1.txt", "root/c/3.txt"]

    # topKFrequentWords (LC 692)
    assert sol4.topKFrequentWords(["i","love","leetcode","i","love","coding"], 2) == ["i","love"]
    assert sol4.topKFrequentWords(["the","day","is","sunny","the","the","the","sunny","is","is"], 4) == ["the","is","sunny","day"]

    # Logger (LC 359)
    logger = Logger()
    assert logger.shouldPrintMessage(1, "foo") == True
    assert logger.shouldPrintMessage(2, "bar") == True
    assert logger.shouldPrintMessage(3, "foo") == False
    assert logger.shouldPrintMessage(8, "bar") == False
    assert logger.shouldPrintMessage(10, "foo") == False
    assert logger.shouldPrintMessage(11, "foo") == True

    # leastBricks (LC 554)
    wall = [[1,2,2,1],[3,1,2],[1,3,2],[2,4],[3,1,2],[1,3,1,1]]
    assert sol4.leastBricks(wall) == 2
    assert sol4.leastBricks([[1],[1],[1]]) == 3

    # numberOfBoomerangs (LC 447)
    assert sol4.numberOfBoomerangs([[0,0],[1,0],[2,0]]) == 2
    assert sol4.numberOfBoomerangs([[1,1],[2,2],[3,3]]) == 2

    # findAndReplacePattern (LC 890)
    assert sorted(sol4.findAndReplacePattern(["abc","deq","mee","aqq","dkd","ccc"], "abb")) == ["aqq","mee"]

    # findRestaurant (LC 599)
    assert sol4.findRestaurant(
        ["Shogun","Tapioca Express","Burger King","KFC"],
        ["Piatti","The Grill at Torrey Pines","Hungry Hunter Steakhouse","Shogun"]
    ) == ["Shogun"]
    assert sorted(sol4.findRestaurant(["Shogun","Tapioca Express","Burger King","KFC","Piatti"],
                                       ["KFC","Shogun","Burger King"])) == ["Shogun"]

    # MyHashMap (LC 706)
    hm = MyHashMap()
    hm.put(1, 1); hm.put(2, 2)
    assert hm.get(1) == 1
    assert hm.get(3) == -1
    hm.put(2, 1)
    assert hm.get(2) == 1
    hm.remove(2)
    assert hm.get(2) == -1

    # MyHashSet (LC 705)
    hs = MyHashSet()
    hs.add(1); hs.add(2)
    assert hs.contains(1) == True
    assert hs.contains(3) == False
    hs.add(2)
    assert hs.contains(2) == True
    hs.remove(2)
    assert hs.contains(2) == False

    # subarraySum already verified above (LC 560 exists)

    print("All hashing tests passed.")
