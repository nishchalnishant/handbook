from sys import *
from collections import *
from math import *

def largestElement_1(arr: [], n: int) -> int:

    # Write your code from here.
    return max(arr)

def largestElement_2(arr: [], n: int) -> int:
    maxx=0
    for i in range(len(arr)):
        if arr[i]> maxx:
            maxx=arr[i]
    return maxx


arr=[1,2,3,4]
print(largestElement_1(arr,len(arr)))