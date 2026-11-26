def recursive_bubble_sort(arr, n=None):
    """
    Recursive Bubble Sort Algorithm
    :param arr: List of elements to be sorted
    :param n: Size of the current unsorted portion of the array
    """
    if n is None:
        n = len(arr)

    # Base case: If the size of the array is 1, it's already sorted
    if n == 1:
        return

    # Perform one pass of bubble sort
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            # Swap if the current element is greater than the next
            arr[i], arr[i + 1] = arr[i + 1], arr[i]

    # Recursive call for the rest of the array (excluding the last element)
    recursive_bubble_sort(arr, n - 1)


# Example usage
if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", arr)
    recursive_bubble_sort(arr)
    print("Sorted array:", arr)