def longest_increasing_subsequence(nums):
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # Initialize DP array with 1, as each element is an LIS of length 1

    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)  # The length of the LIS is the maximum value in the DP array

# Example usage
if __name__ == "__main__":
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print("Length of Longest Increasing Subsequence:", longest_increasing_subsequence(nums))