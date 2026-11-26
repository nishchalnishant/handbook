from typing import List

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        """
        Problem: Count of Smaller Numbers After Self
        Difficulty: Hard
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        if not nums: return []
        
        counts = [0] * len(nums)
        indexed_nums = list(enumerate(nums)) # (index, value)
        
        def merge_sort(enum):
            mid = len(enum) // 2
            if mid:
                left, right = merge_sort(enum[:mid]), merge_sort(enum[mid:])
                for i in range(len(enum) - 1, -1, -1):
                    if not right or (left and left[-1][1] > right[-1][1]):
                        counts[left[-1][0]] += len(right)
                        enum[i] = left.pop()
                    else:
                        enum[i] = right.pop()
            return enum
            
        merge_sort(indexed_nums)
        return counts
