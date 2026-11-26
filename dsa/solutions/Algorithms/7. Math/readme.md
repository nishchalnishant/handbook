# Math Algorithms Overview

Mathematical algorithms often involve number theory, combinatorics, and geometry.

## Concepts
- **Primes**: Sieve of Eratosthenes.
- **GCD/LCM**: Euclidean Algorithm.
- **Modulo Arithmetic**: (a + b) % m.

---

## Problems & Solutions

### Easy
1. **[GCD and LCM](Easy/gcd_lcm.py)**
   - Euclidean algorithm.
2. **[Check Prime](Easy/is_prime.py)**
   - Basic O(sqrt(n)) check.
3. **[Power of Two](Easy/power_of_two.py)**
   - Check if number is power of 2.
4. **[Excel Sheet Column Title](Easy/excel_sheet_column.py)**
   - Convert number to column title.

### Medium
1. **[Count Primes](Medium/count_primes.py)**
   - Sieve of Eratosthenes.
2. **[Pow(x, n)](../5.%20Divide%20and%20concuer/Medium/pow_x_n.py)**
   - Fast Exponentiation.
3. **[Factorial Trailing Zeroes](Medium/trailing_zeroes.py)**
   - Count trailing zeroes in n!.

### Hard
1. **[Max Points on a Line](Hard/max_points_line.py)**
   - Geometry / GCD slopes.

---

## Tips for Interviews
- **Overflow**: be careful with large numbers (Python handles automatically, but good to know).
- **0/1 Edge Cases**: Always check 0, 1, negatives.