# Greedy Algorithms Overview

Greedy algorithms make the locally optimal choice at each step with the hope of finding a global optimum.

## Concepts
- **Greedy Choice Property**: Local optimal -> Global optimal.
- **Optimal Substructure**: Problem can be broken down.

---

## Problems & Solutions

### Easy
1. **[Assign Cookies](Easy/assign_cookies.py)**
   - Satisfy children with minimum size cookies.
2. **[Lemonade Change](Easy/lemonade_change.py)**
   - Provide correct change with limited bills.

### Medium
1. **[Jump Game](Medium/jump_game.py)**
   - Can you reach the last index?
2. **[Gas Station](Medium/gas_station.py)**
   - Complete circuit around gas stations.
3. **[Activity Selection](Medium/activity_selection.py)**
   - Maximum non-overlapping intervals.
4. **[Fractional Knapsack](Medium/fractional_knapsack.py)**
   - Maximize value with fractional items.

### Hard
1. **[Candy](Hard/candy.py)**
   - Distribute candy with rating constraints.

---

## Tips for Interviews
- **Prove Optimality**: Greedy doesn't always work (e.g., 0/1 Knapsack). Ensure greedy choice is safe.
- **Sorting**: Often requires sorting input first (e.g., by end time, by value/weight).
