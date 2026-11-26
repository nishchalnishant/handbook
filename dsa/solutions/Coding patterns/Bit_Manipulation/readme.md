# Bit Manipulation 🧬

## Description
Bit manipulation involves manipulating individual bits of integers to solve problems efficiently, often in O(1) space.

## Strategies

### 1. XOR Properties
- **Concept**: `a ^ a = 0`, `a ^ 0 = a`, `a ^ b = b ^ a`. Useful for finding unique elements.
- **Problems**:
    - Single Number
    - Missing Number

### 2. Counting Bits
- **Concept**: Brian Kernighan’s algorithm (`n & (n-1)` clears the lowest set bit).
- **Problems**:
    - Number of 1 Bits (Hamming Weight)
    - Counting Bits
    - Reverse Bits

### 3. Power of Two
- **Concept**: A number is a power of 2 if it has exactly one bit is set. `(n & (n-1)) == 0`.
- **Problems**:
    - Power of Two
    - Power of Four

### 4. Bit Masking
- **Concept**: Use a bitmask to represent a set of elements (especially useful in DP when N is small).
- **Problems**:
    - Subsets
    - Maximum Product of Word Lengths
    - Sum of Two Integers
