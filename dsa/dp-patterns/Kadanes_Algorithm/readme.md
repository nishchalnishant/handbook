# Kadane's Algorithm

## Introduction
Kadane's Algorithm is an efficient method to find the maximum sum subarray.

## Core Recursion Tree (Max sum ending at i)
```mermaid
graph TD
    A["State(i)"] --> B["Start New: arr[i]"]
    A --> C["Extend: arr[i] + State(i-1)"]
```

---

## Similar Problems

### 1. Maximum Circular Subarray Sum
**Recursion Tree**:
```mermaid
graph TD
    A["Result"] --> B["Kadane(arr)"]
    A --> C["Total - MinKadane(arr)"]
```

### 2. Maximum Product Subarray
**Recursion Tree (State at i)**:
```mermaid
graph TD
    A["State(i)"] --> B["Max: max(arr[i], arr[i]*prevMax, arr[i]*prevMin)"]
    A --> C["Min: min(arr[i], arr[i]*prevMax, arr[i]*prevMin)"]
```

### 3. Best Time to Buy and Sell Stock
**Recursion Tree (State: i)**:
```mermaid
graph TD
    A["Day i"] --> B["Profit = Current - MinPriceSeen"]
    A --> C["Update MinPriceSeen"]
```

### 4. Stock II
**Recursion Tree**:
```mermaid
graph TD
    A["Day i"] --> B["If i > i-1: Profit += (i - i-1)"]
```

### 5. Stock III (2 Transactions)
**Recursion Tree**:
```mermaid
graph TD
    A["Split at i"] --> B["MaxProfit(0, i)"]
    A --> C["MaxProfit(i, n-1)"]
```

### 6. Max Subarray One Deletion
**Recursion Tree (i-th element)**:
```mermaid
graph TD
    A["State i"] --> B["Skip one: Forward(i-1) + Backward(i+1)"]
    A --> C["Normal: Kadane(i)"]
```
*(Visualization of skip-one logic)*
