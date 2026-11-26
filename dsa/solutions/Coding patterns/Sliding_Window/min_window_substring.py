from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Problem: Minimum Window Substring
        Pattern: Sliding Window - Variable Size
        Time Complexity: O(n)
        Space Complexity: O(1) (since char set is limited)
        """
        if not t or not s: return ""
        
        target_count = Counter(t)
        window_count = Counter()
        
        have, need = 0, len(target_count)
        res, res_len = [-1, -1], float("inf")
        
        left = 0
        for right in range(len(s)):
            char = s[right]
            window_count[char] += 1
            
            if char in target_count and window_count[char] == target_count[char]:
                have += 1
                
            while have == need:
                # Update result if this window is smaller
                if (right - left + 1) < res_len:
                    res = [left, right]
                    res_len = (right - left + 1)
                
                # Shrink from left
                window_count[s[left]] -= 1
                if s[left] in target_count and window_count[s[left]] < target_count[s[left]]:
                    have -= 1
                left += 1
                
        left, right = res
        return s[left : right + 1] if res_len != float("inf") else ""

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.minWindow("ADOBECODEBANC", "ABC")) # Expected: "BANC"
