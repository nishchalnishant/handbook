from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """
        Problem: Longest Consecutive Sequence
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        numSet = set(nums)
        longest = 0
        
        for n in nums:
            # Check if start of sequence
            if (n - 1) not in numSet:
                length = 0
                while (n + length) in numSet:
                    length += 1
                longest = max(length, longest)
                
        return longest
