from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        Problem: Two Sum II - Input Array Is Sorted
        Pattern: Two Pointers - Converging
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        left, right = 0, len(numbers) - 1
        
        while left < right:
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                return [left + 1, right + 1] # 1-indexed
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return []

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.twoSum([2,7,11,15], 9)) # Expected: [1, 2]
