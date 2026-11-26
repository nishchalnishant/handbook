"""
Maximum Product Subarray using Dynamic Programming

This algorithm finds the maximum product of a contiguous subarray in a given array.
It uses dynamic programming to keep track of the maximum and minimum products at each step,
as the minimum product can become the maximum when multiplied by a negative number.
"""

def max_product_subarray(nums):
    if not nums:
        return 0

    # Initialize variables to store the maximum product, minimum product, and result
    max_product = nums[0]
    min_product = nums[0]
    result = nums[0]

    # Iterate through the array starting from the second element
    for i in range(1, len(nums)):
        num = nums[i]

        # If the current number is negative, swap max_product and min_product
        if num < 0:
            max_product, min_product = min_product, max_product

        # Update max_product and min_product
        max_product = max(num, max_product * num)
        min_product = min(num, min_product * num)

        # Update the result with the maximum product found so far
        result = max(result, max_product)

    return result

# Example usage
if __name__ == "__main__":
    nums = [2, 3, -2, 4]
    print("Maximum Product Subarray:", max_product_subarray(nums))