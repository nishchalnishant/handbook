# Longest Common Subsequence (LCS)

## Introduction
The LCS pattern involves finding the longest subsequence present in two sequences.

## Core Recursion Tree (Match 'A')
```mermaid
graph TD
    A["LCS('ABC', 'ACD')"] --> B["1 + LCS('BC', 'CD') [Match 'A']"]
```

---

## Similar Problems

### 1. Longest Common Substring
**Recursion Tree (Match 'A')**:
```mermaid
graph TD
    A["LCS('ABC', 'ADC')"] --> B["1 + LCS('BC', 'DC') [Match 'A']"]
    C["Non-Match 'B','D'"] --> D["Length: 0"]
```

### 2. Edit Distance
**Recursion Tree (i: idx of s1, j: idx of s2)**:
```mermaid
graph TD
    A["ED(i, j)"] --> B["Replace: 1 + ED(i-1, j-1)"]
    A --> C["Delete: 1 + ED(i-1, j)"]
    A --> D["Insert: 1 + ED(i, j-1)"]
```

### 3. Longest Palindromic Subsequence
**Recursion Tree**: (Same as LCS of string and its reverse).

### 4. Shortest Common Supersequence
**Recursion Tree**:
```mermaid
graph TD
    A["SCS('ABC', 'ABD')"] --> B["Match 'A': 'A' + SCS('BC', 'BD')"]
    A --> C["Mis: 'A'+SCS('BC', 'ABD') OR 'A'+SCS('ABC', 'BD')"]
```

### 5. Distinct Subsequences
**Recursion Tree (s='rabbbit', t='rabbit')**:
```mermaid
graph TD
    A["Count('rabbbit', 'rabbit')"] --> B["Match 'r': Count('abbbit', 'abbit')"]
    B --> C["Skip 'a': ..."]
    B --> D["Take 'a': Count('bbbit', 'bbit')"]
```

### 6. Wildcard Matching
**Recursion Tree (s='aa', p='a*')**:
```mermaid
graph TD
    A["Match 'a*','aa'"] --> B["Skip *: match('aa', '')"]
    A --> C["Use *: match('a', 'a*')"]
```

### 7. Regular Expression Matching
**Recursion Tree (s='aa', p='a*')**:
```mermaid
graph TD
    A["Match 'a*','aa'"] --> B["Zero 'a': match('aa', '')"]
    A --> C["One+ 'a': match('a', 'a*')"]
```
*(Preceding char dependency logic)*
