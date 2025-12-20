def rob_ii(nums):
    """
    Problem: House Robber but houses are in a circle.
    
    Approach:
    - If efficient to rob houses 0 to N-2 (exclude last).
    - Or houses 1 to N-1 (exclude first).
    - Result is max of both cases.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    
    def simple_rob(arr):
        prev2, prev1 = 0, 0
        for x in arr:
            curr = max(prev1, prev2 + x)
            prev2 = prev1
            prev1 = curr
        return prev1
        
    return max(simple_rob(nums[:-1]), simple_rob(nums[1:]))

# Example Usage
if __name__ == "__main__":
    nums = [2, 3, 2]
    print(f"Max robbed: {rob_ii(nums)}")
