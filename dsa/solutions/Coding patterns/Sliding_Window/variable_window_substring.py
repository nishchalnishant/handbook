from typing import List

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Problem: Longest Substring Without Repeating Characters
        Pattern: Sliding Window - Variable Size
        """
        char_index = {}
        left = 0
        max_len = 0
        
        for right, char in enumerate(s):
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1
            char_index[char] = right
            max_len = max(max_len, right - left + 1)
            
        return max_len

    def characterReplacement(self, s: str, k: int) -> int:
        """
        Problem: Longest Repeating Character Replacement
        Pattern: Sliding Window - Variable Size
        """
        count = {}
        left = 0
        max_freq = 0
        max_len = 0
        
        for right in range(len(s)):
            count[s[right]] = count.get(s[right], 0) + 1
            max_freq = max(max_freq, count[s[right]])
            
            # (Window size - max_freq) is the number of chars to replace
            # If greater than k, we need to shrink window
            while (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1
                
            max_len = max(max_len, right - left + 1)
            
        return max_len

    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """
        Problem: Minimum Size Subarray Sum
        Pattern: Sliding Window - Variable Size
        """
        min_len = float('inf')
        left = 0
        current_sum = 0
        
        for right in range(len(nums)):
            current_sum += nums[right]
            
            while current_sum >= target:
                min_len = min(min_len, right - left + 1)
                current_sum -= nums[left]
                left += 1
                
        return min_len if min_len != float('inf') else 0

# Test
if __name__ == "__main__":
    sol = Solution()
    print(f"Longest Substr: {sol.lengthOfLongestSubstring('abcabcbb')}") # 3
    print(f"Char Replacement: {sol.characterReplacement('ABAB', 2)}") # 4
    print(f"Min Subarray: {sol.minSubArrayLen(7, [2,3,1,2,4,3])}") # 2
