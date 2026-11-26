# Greedy Algorithms 💰

## Description
Greedy algorithms make the locally optimal choice at each step with the hope of finding a global optimum. They are often used for optimization problems like maximizing profit or minimizing count.

## Strategies

### 1. Interval Scheduling
- **Concept**: Sort intervals by **end time** (usually) to maximize the number of non-overlapping intervals.
- **Problems**:
    - Non-overlapping Intervals
    - Minimum Number of Arrows to Burst Balloons
    - Merge Intervals (Sort by start time)
    - Meeting Rooms II

### 2. Jump Game (Reachability)
- **Concept**: at each step, track the maximum index reachable. If you can reach the end, return true.
- **Problems**:
    - Jump Game
    - Jump Game II

### 3. Stock Trading
- **Concept**: Buy locally low, sell locally high.
- **Problems**:
    - Best Time to Buy and Sell Stock II

### 4. String Partitioning
- **Concept**: Extend the current partition as far as necessary to include all occurrences of characters within it.
- **Problems**:
    - Partition Labels
    - Candy
    - Gas Station
