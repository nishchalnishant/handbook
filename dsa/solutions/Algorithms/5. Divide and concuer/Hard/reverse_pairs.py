from typing import List

class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        """
        Problem: Reverse Pairs
        Difficulty: Hard
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        def merge_sort(start, end):
            if start >= end:
                return 0
            
            mid = (start + end) // 2
            cnt = merge_sort(start, mid) + merge_sort(mid + 1, end)
            
            # Count pairs
            j = mid + 1
            for i in range(start, mid + 1):
                while j <= end and nums[i] > 2 * nums[j]:
                    j += 1
                cnt += (j - (mid + 1))
            
            # Merge
            nums[start:end+1] = sorted(nums[start:end+1])
            return cnt
            
        return merge_sort(0, len(nums) - 1)
