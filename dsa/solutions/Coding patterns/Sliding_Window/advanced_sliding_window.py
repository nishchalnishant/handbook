from typing import List
from collections import Counter

class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        """
        Problem: Fruit Into Baskets (Longest Substring with At Most 2 Distinct Characters)
        Pattern: Sliding Window - Variable Size
        """
        count = Counter()
        left = 0
        max_fruits = 0
        
        for right in range(len(fruits)):
            count[fruits[right]] += 1
            
            while len(count) > 2:
                count[fruits[left]] -= 1
                if count[fruits[left]] == 0:
                    del count[fruits[left]]
                left += 1
                
            max_fruits = max(max_fruits, right - left + 1)
            
        return max_fruits

    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        """
        Problem: Longest Substring with At Most K Distinct Characters
        Pattern: Sliding Window - Variable Size
        """
        count = Counter()
        left = 0
        max_len = 0
        
        for right, char in enumerate(s):
            count[char] += 1
            
            while len(count) > k:
                count[s[left]] -= 1
                if count[s[left]] == 0:
                    del count[s[left]]
                left += 1
                
            max_len = max(max_len, right - left + 1)
            
        return max_len

    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        """
        Problem: Subarrays with K Different Integers
        Pattern: Sliding Window - Exact K is tricky. Formula: atMostK(k) - atMostK(k-1).
        """
        return self.atMostK(nums, k) - self.atMostK(nums, k - 1)
    
    def atMostK(self, nums: List[int], k: int) -> int:
        count = Counter()
        left = 0
        res = 0
        
        for right in range(len(nums)):
            if count[nums[right]] == 0:
                k -= 1
            count[nums[right]] += 1
            
            while k < 0:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    k += 1
                left += 1
            
            res += right - left + 1
        return res

# Test
if __name__ == "__main__":
    sol = Solution()
    print(f"Fruit Baskets: {sol.totalFruit([1,2,1])}") # 3
    print(f"K Distinct Subarrays: {sol.subarraysWithKDistinct([1,2,1,2,3], 2)}") # 7
