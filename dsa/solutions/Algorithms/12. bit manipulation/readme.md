# Bit Manipulation Overview 0️⃣1️⃣

Manipulating individual bits.

## Concepts
- **AND (&)**: Clear bits / Check if bit is set.
- **OR (|)**: Set bits.
- **XOR (^)**: Toggle bits / Find unique (a ^ a = 0).
- **Shift (<<, >>)**: Multiply/Divide by 2.

---

## Problems & Solutions

### Easy
1. **[Single Number](Easy/single_number.py)**
   - Find element appearing once (others twice).
2. **[Counting Bits](Easy/counting_bits.py)**
   - Count 1s from 0 to n.
3. **[Number of 1 Bits](Easy/number_of_1_bits.py)**
   - Hamming Weight.
4. **[Missing Number](Easy/missing_number.py)**
   - Find missing in [0, n].
5. **[Reverse Bits](Easy/reverse_bits.py)**
   - Reverse binary representation.

### Medium
1. **[Sum of Two Integers](Medium/sum_two_integers.py)**
   - Add without + or -.

---

## Tips for Interviews
- **XOR Trick**: `a ^ b ^ a = b`.
- **Set/Unset**: `n & (n-1)` removes lowest set bit.
