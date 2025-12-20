# Graph Traversal 🕸️

## Description
Graph algorithms involve exploring nodes (vertices) and edges to solve problems related to connectivity, paths, and cycles.

## Strategies

### 1. Depth First Search (DFS)
- **Concept**: Explore as deep as possible along each branch before backtracking.
- **Use Case**: Detecting cycles, topological sort, finding connected components, solving mazes.
- **Problems**:
    - Number of Islands
    - Max Area of Island
    - Course Schedule (Cycle Detection)
    - Clone Graph
    - Pacific Atlantic Water Flow
    - Surrounded Regions

### 2. Breadth First Search (BFS)
- **Concept**: Explore neighbor nodes first then move to next level neighbors.
- **Use Case**: Shortest path in unweighted graphs.
- **Problems**:
    - Rotting Oranges
    - Word Ladder
    - 01 Matrix

### 3. Union-Find (Disjoint Set Union)
- **Concept**: Efficiently track valid sets of elements partitioned into disjoint (non-overlapping) subsets.
- **Use Case**: Kruskal's MST algorithm, cycle detection in undirected graphs, connecting components online.
- **Problems**:
    - Redundant Connection
    - Number of Operations to Make Network Connected
    - Graph Valid Tree

### 4. Shortest Path Algorithms
- **Dijkstra's**: Weighted graphs with non-negative weights (Priority Queue).
- **Bellman-Ford**: Weighted graphs with negative weights (detects negative cycles).
- **Problems**:
    - Network Delay Time
    - Cheapest Flights Within K Stops

### 5. Topological Sort
- **Concept**: Linear ordering of vertices such that for every directed edge u -> v, u comes before v. (Using Kahn's Algorithm/BFS or DFS).
- **Use Case**: Task scheduling / dependencies.
- **Problems**:
    - Course Schedule II
