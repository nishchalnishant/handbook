def find_number_of_lis(nums):
    """
    Problem: Find the number of longest increasing subsequences.
    
    Approach: LIS Pattern
    - lengths[i] = length of LIS ending at i
    - counts[i] = number of LIS ending at i
    - If nums[i] > nums[j]:
        - if lengths[j] + 1 > lengths[i]: update length and reset count
        - if lengths[j] + 1 == lengths[i]: add counts[j] to counts[i]
    
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    """
    if not nums: return 0
    n = len(nums)
    lengths = [1] * n
    counts = [1] * n
    
    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                if lengths[j] + 1 > lengths[i]:
                    lengths[i] = lengths[j] + 1
                    counts[i] = counts[j]
                elif lengths[j] + 1 == lengths[i]:
                    counts[i] += counts[j]
                    
    max_len = max(lengths)
    return sum(c for l, c in zip(lengths, counts) if l == max_len)

# Example Usage
if __name__ == "__main__":
    nums = [1, 3, 5, 4, 7]
    print(f"Number of LIS: {find_number_of_lis(nums)}")
