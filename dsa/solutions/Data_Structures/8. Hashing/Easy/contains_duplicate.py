from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        """
        Problem: Contains Duplicate
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        hashset = set()
        for n in nums:
            if n in hashset:
                return True
            hashset.add(n)
        return False
