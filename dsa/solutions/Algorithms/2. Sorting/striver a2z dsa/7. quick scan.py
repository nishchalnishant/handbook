# Quick Scan Algorithm
# This is a simplified implementation of the Quick Sort algorithm.
# It sorts an array by partitioning it into smaller subarrays based on a pivot element.

def quick_scan(arr):
    """
    Function to perform quick scan (quick sort) on an array.
    :param arr: List of integers to be sorted
    :return: Sorted list of integers
    """
    # Base case: If the array has 0 or 1 element, it is already sorted
    if len(arr) <= 1:
        return arr

    # Choose the pivot element (here, we choose the last element)
    pivot = arr[-1]

    # Partition the array into two subarrays:
    # - left: Elements less than or equal to the pivot
    # - right: Elements greater than the pivot
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]

    # Recursively apply quick_scan to the left and right subarrays
    # Combine the sorted left subarray, pivot, and sorted right subarray
    return quick_scan(left) + [pivot] + quick_scan(right)

# Example usage
if __name__ == "__main__":
    # Input array
    array = [10, 7, 8, 9, 1, 5]
    print("Original array:", array)

    # Perform quick scan
    sorted_array = quick_scan(array)
    print("Sorted array:", sorted_array)