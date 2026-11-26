def recursive_insertion_sort(arr, n):
    """
    Recursive function to perform insertion sort on an array.

    Parameters:
    arr (list): The array to be sorted.
    n (int): The size of the array to be sorted.

    Returns:
    None: The array is sorted in place.
    """
    # Base case: If the array has one or no elements, it's already sorted
    if n <= 1:
        return

    # Sort the first n-1 elements
    recursive_insertion_sort(arr, n - 1)

    # Insert the last element at its correct position in the sorted array
    last = arr[n - 1]
    j = n - 2

    # Shift elements of the sorted part of the array to the right
    while j >= 0 and arr[j] > last:
        arr[j + 1] = arr[j]
        j -= 1

    # Place the last element at its correct position
    arr[j + 1] = last


# Example usage
if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6]
    print("Original array:", arr)
    recursive_insertion_sort(arr, len(arr))
    print("Sorted array:", arr)