def four_sum(nums, target):
    nums.sort()
    n = len(nums)
    result = set()
    pair_sums = {}

    # Store all pairs of sums in a hash map
    for i in range(n):
        for j in range(i + 1, n):
            pair_sum = nums[i] + nums[j]
            if pair_sum not in pair_sums:
                pair_sums[pair_sum] = []
            pair_sums[pair_sum].append((i, j))

    # Iterate through the array to find quadruplets
    for i in range(n):
        for j in range(i + 1, n):
            remaining = target - (nums[i] + nums[j])
            if remaining in pair_sums:
                for pair in pair_sums[remaining]:
                    k, l = pair
                    if k > j:  # Ensure indices are in the correct order
                        result.add((nums[i], nums[j], nums[k], nums[l]))

    return [list(quad) for quad in result]

# Example usage
if __name__ == "__main__":
    nums = [1, 0, -1, 0, -2, 2]
    target = 0
    print(four_sum(nums, target))
