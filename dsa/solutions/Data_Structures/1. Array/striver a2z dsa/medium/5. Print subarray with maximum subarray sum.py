# Python Program to print subarray with maximum sum using nested loops

# Function to find the subarray with maximum sum
def maxSumSubarray(arr):
    
    # start and end of max sum subarray
    resStart = 0
    resEnd = 0
  
    # Initialize the maximum subarray sum with the first element
    maxSum = arr[0]

    for i in range(len(arr)):
        
        # Initialize current subarray sum with 0
        currSum = 0
        for j in range(i, len(arr)):
            currSum += arr[j]
            
            # If current subarray has greater sum than maximum sum subarray,
            # then update the start and end of maximum sum subarray
            if currSum > maxSum:
                maxSum = currSum
                resStart = i
                resEnd = j
  
    res = []
    for i in range(resStart, resEnd + 1):
        res.append(arr[i])
    return res


arr = [2, 3, -8, 7, -1, 2, 3]
res = maxSumSubarray(arr)
  
for num in res:
    print(num, end=" ")
print()
