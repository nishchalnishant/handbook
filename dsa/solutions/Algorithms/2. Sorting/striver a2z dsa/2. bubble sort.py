def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        # Track if any swapping happens
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap the elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no swapping happens, the array is already sorted
        if not swapped:
            break

# Example usage
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    print("Unsorted array:", data)
    bubble_sort(data)
    print("Sorted array:", data)