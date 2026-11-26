# Merge Sort Algorithm
# Merge Sort is a divide-and-conquer algorithm that splits the array into halves,
# recursively sorts them, and then merges the sorted halves.

def merge_sort(arr):
    # Base case: If the array has one or no elements, it is already sorted
    if len(arr) <= 1:
        return arr

    # Step 1: Divide the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Step 2: Recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    # Step 3: Merge the sorted halves
    return merge(left_sorted, right_sorted)

def merge(left, right):
    # Merge two sorted arrays into one sorted array
    merged = []
    i = j = 0

    # Compare elements from both arrays and add the smaller one to the merged array
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Add any remaining elements from the left array
    while i < len(left):
        merged.append(left[i])
        i += 1

    # Add any remaining elements from the right array
    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged

# Example usage
if __name__ == "__main__":
    array = [38, 27, 43, 3, 9, 82, 10]
    print("Original array:", array)
    sorted_array = merge_sort(array)
    print("Sorted array:", sorted_array)