def insertion_sort(arr):
    """
    Perform insertion sort on the given list.

    Insertion sort is a simple sorting algorithm that builds the final sorted array one item at a time.
    It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort.

    Time Complexity:
    - Best case: O(n) [when the array is already sorted]
    - Worst case: O(n^2) [when the array is sorted in reverse order]
    - Average case: O(n^2)

    Space Complexity: O(1) [in-place sorting]

    Parameters:
    arr (list): The list of elements to be sorted.

    Returns:
    None: The input list is sorted in place.
    """
    n = len(arr)
    for i in range(1, n):
        key = arr[i]  # The element to be inserted in the sorted portion
        j = i - 1

        # Move elements of arr[0..i-1], that are greater than key, to one position ahead of their current position
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        # Place the key in its correct position
        arr[j + 1] = key


# Example usage
if __name__ == "__main__":
    data = [12, 11, 13, 5, 6]
    print("Original array:", data)
    insertion_sort(data)
    print("Sorted array:", data)