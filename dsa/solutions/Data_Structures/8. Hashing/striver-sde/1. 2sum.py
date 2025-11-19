def two_sum(nums, target):
    """
    Finds two numbers in the list that add up to the target.

    :param nums: List[int] - List of integers
    :param target: int - Target sum
    :return: List[int] - Indices of the two numbers
    """
    num_to_index = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    
    return []

# Example usage
if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    result = two_sum(nums, target)
    print("Indices:", result)