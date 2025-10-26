# Selection Sort Algorithm in Python

def selection_sort(arr):
    """
    Sorts an array using the selection sort algorithm.

    Parameters:
    arr (list): The list of elements to be sorted.

    Returns:
    None: The input list is sorted in place.
    """
    n = len(arr)
    for i in range(n - 1):
        # Assume the first unsorted element is the smallest
        min_index = i
        for j in range(i + 1, n):
            # Find the index of the smallest element in the unsorted part
            if arr[j] < arr[min_index]:
                min_index = j
        # Swap the smallest element with the first unsorted element
        arr[i], arr[min_index] = arr[min_index], arr[i]

# Example usage
if __name__ == "__main__":
    data = [64, 25, 12, 22, 11]
    print("Unsorted array:", data)
    selection_sort(data)
    print("Sorted array:", data)