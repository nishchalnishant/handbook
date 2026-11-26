def binary_search(arr, x):
    """
    Perform binary search to find the index of x in a sorted array.

    :param arr: List[int] - The sorted array
    :param x: int - The target value to search for
    :return: int - The index of x if found, otherwise -1
    """
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    return -1

# Example usage
if __name__ == "__main__":
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 7
    result = binary_search(sorted_array, target)
    if result != -1:
        print(f"Element {target} found at index {result}.")
    else:
        print(f"Element {target} not found in the array.")