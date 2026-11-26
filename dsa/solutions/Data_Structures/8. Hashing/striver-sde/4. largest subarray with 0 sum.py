def largest_subarray_with_zero_sum(arr):
    # Dictionary to store the prefix sum and its index
    prefix_sum_map = {}
    max_length = 0
    prefix_sum = 0

    for i in range(len(arr)):
        prefix_sum += arr[i]

        # If prefix sum is 0, update max_length
        if prefix_sum == 0:
            max_length = i + 1

        # If prefix sum is already in the map, calculate the subarray length
        if prefix_sum in prefix_sum_map:
            max_length = max(max_length, i - prefix_sum_map[prefix_sum])
        else:
            # Store the prefix sum with its index
            prefix_sum_map[prefix_sum] = i

    return max_length


# Example usage
if __name__ == "__main__":
    arr = [1, 2, -3, 3, 1, -4, 2, -2]
    print("Length of the largest subarray with 0 sum:", largest_subarray_with_zero_sum(arr))