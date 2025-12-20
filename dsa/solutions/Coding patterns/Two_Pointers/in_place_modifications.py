from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Problem: Remove Duplicates from Sorted Array
        Pattern: Two Pointers - In-place
        """
        if not nums: return 0
        write_ptr = 1
        for read_ptr in range(1, len(nums)):
            if nums[read_ptr] != nums[read_ptr - 1]:
                nums[write_ptr] = nums[read_ptr]
                write_ptr += 1
        return write_ptr

    def moveZeroes(self, nums: List[int]) -> None:
        """
        Problem: Move Zeroes
        Pattern: Two Pointers - In-place
        """
        write_ptr = 0
        for read_ptr in range(len(nums)):
            if nums[read_ptr] != 0:
                nums[write_ptr], nums[read_ptr] = nums[read_ptr], nums[write_ptr]
                write_ptr += 1 # Only increment write_ptr when we write a non-zero

    def rotate(self, nums: List[int], k: int) -> None:
        """
        Problem: Rotate Array
        Pattern: Two Pointers (Reverse method)
        """
        k %= len(nums)
        self.reverse(nums, 0, len(nums) - 1)
        self.reverse(nums, 0, k - 1)
        self.reverse(nums, k, len(nums) - 1)
    
    def reverse(self, nums: List[int], start: int, end: int) -> None:
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

# Test
if __name__ == "__main__":
    sol = Solution()
    
    # Remove Duplicates
    arr1 = [1,1,2]
    k = sol.removeDuplicates(arr1)
    print(f"Remove Dups: {arr1[:k]}") # [1,2]
    
    # Move Zeroes
    arr2 = [0,1,0,3,12]
    sol.moveZeroes(arr2)
    print(f"Move Zeroes: {arr2}") # [1,3,12,0,0]
    
    # Rotate
    arr3 = [1,2,3,4,5,6,7]
    sol.rotate(arr3, 3)
    print(f"Rotate: {arr3}") # [5,6,7,1,2,3,4]
