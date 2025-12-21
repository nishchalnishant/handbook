"""
Easy Recursion Problems
-----------------------
This file contains solutions to 10 common easy recursion problems.
"""

# 1. Factorial
# Calculate n!
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# 2. Fibonacci
# Find the n-th Fibonacci number
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 3. Sum of Digits
# Find the sum of digits of a number
def sum_of_digits(n):
    if n < 10:
        return n
    return (n % 10) + sum_of_digits(n // 10)

# 4. Power (x, n)
# Calculate x^n
def power(x, n):
    if n == 0:
        return 1
    if n < 0:
        return 1 / power(x, -n)
    return x * power(x, n - 1)

# 5. Reverse a String
# Reverse a given string recursively
def reverse_string(s):
    if len(s) == 0:
        return s
    return reverse_string(s[1:]) + s[0]

# 6. Palindrome Check
# Check if a string is a palindrome
def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])

# 7. Count Set Bits
# Count the number of 1s in the binary representation of a number
def count_set_bits(n):
    if n == 0:
        return 0
    return (n & 1) + count_set_bits(n >> 1)

# 8. Array Sum
# Calculate the sum of elements in an array
def array_sum(arr):
    if not arr:
        return 0
    return arr[0] + array_sum(arr[1:])

# 9. Binary Search
# Implement binary search recursively
def binary_search(arr, low, high, x):
    if high >= low:
        mid = (high + low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        return -1

# 10. Length of String
# Find the length of a string recursively
def string_length(s):
    if not s:
        return 0
    return 1 + string_length(s[1:])

if __name__ == "__main__":
    # Sample Test Cases
    print(f"Factorial(5): {factorial(5)}")           # Expect 120
    print(f"Fibonacci(7): {fibonacci(7)}")           # Expect 13
    print(f"Sum of digits(1234): {sum_of_digits(1234)}") # Expect 10
    print(f"Power(2, 5): {power(2, 5)}")             # Expect 32
    print(f"Reverse 'hello': {reverse_string('hello')}") # Expect 'olleh'
    print(f"Is 'radar' palindrome? {is_palindrome('radar')}") # Expect True
    print(f"Count set bits(15): {count_set_bits(15)}")   # Expect 4
    print(f"Array sum [1, 2, 3, 4, 5]: {array_sum([1, 2, 3, 4, 5])}") # Expect 15
    arr = [2, 3, 4, 10, 40]
    print(f"Binary Search 10 in {arr}: {binary_search(arr, 0, len(arr)-1, 10)}") # Expect 3
    print(f"Length of 'recursion': {string_length('recursion')}") # Expect 9
