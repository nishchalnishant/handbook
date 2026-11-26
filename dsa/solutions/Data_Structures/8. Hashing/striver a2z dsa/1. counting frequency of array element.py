def count_frequency(arr):
    # Create an empty dictionary to store frequencies
    frequency = {}

    # Iterate through the array
    for num in arr:
        # Increment the count for each element
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    return frequency

# Example usage
if __name__ == "__main__":
    arr = [1, 2, 2, 3, 1, 4, 2, 3, 5]
    result = count_frequency(arr)
    print("Element frequencies:", result)