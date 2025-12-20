from typing import List

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Problem: Sort Colors (Dutch National Flag)
        Pattern: Two Pointers - Converging (3 Pointers technically)
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        # low points to the end of 0s, mid points to current element, high points to start of 2s
        low, mid, high = 0, 0, len(nums) - 1
        
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else: # nums[mid] == 2
                nums[high], nums[mid] = nums[mid], nums[high]
                high -= 1
                # Don't increment mid, as swapped element from high needs to be checked

# Test
if __name__ == "__main__":
    sol = Solution()
    arr = [2,0,2,1,1,0]
    sol.sortColors(arr)
    print(arr) # Expected: [0,0,1,1,2,2]
