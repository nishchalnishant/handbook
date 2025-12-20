# Graph Overview 🕸️

A Graph consists of vertices (nodes) and edges. It can be Directed/Undirected and Weighted/Unweighted.

## Topics Covered

### 1. Representations
- **Adjacency Matrix**: `M[i][j]` (Space O(V^2)).
- **Adjacency List**: `List[i]` contains neighbors (Space O(V+E)).

### 2. Traversals
- **BFS (Breadth-First Search)**: Shortest path in unweighted graph (Queue).
- **DFS (Depth-First Search)**: Exploring paths, cycle detection (Stack/Recursion).

### 3. Algorithms
- **Topological Sort**: Order nodes in DAG (Kahn's / DFS).
- **Union Find (DSU)**: Connected components, cycle detection.
- **Dijkstra**: Shortest path in weighted graph (Priority Queue).

---

## Problems & Solutions

### Medium
1. **[Number of Islands](Medium/number_of_islands.py)**
   - Count connected components (DFS/BFS).
2. **[Clone Graph](Medium/clone_graph.py)**
   - Deep copy of graph (DFS/BFS + HashMap).
3. **[Pacific Atlantic Water Flow](Medium/pacific_atlantic.py)**
   - Water flow to oceans (DFS/BFS from borders).
4. **[Course Schedule](Medium/course_schedule.py)**
   - Detect cycle in DAG (Topological Sort / DFS).
5. **[Longest Consecutive Sequence](Medium/longest_consecutive.py)**
   - Find longest sequence (HashSet / Union Find).
6. **[Graph Valid Tree](Medium/graph_valid_tree.py)**
   - Check if graph is fully connected and acyclic.
7. **[Number of Connected Components in an Undirected Graph](Medium/count_components.py)**
   - Count connected components (Union Find/DFS).

### Hard
1. **[Word Ladder](Hard/word_ladder.py)**
   - Shortest transformation sequence (BFS).
2. **[Alien Dictionary](Hard/alien_dictionary.py)**
   - Derive order of characters (Topological Sort).

---

## Tips for Interviews
- **BFS**: Best for shortest path in unweighted graphs.
- **DFS**: Good for exhaustive search, cycle detection.
- **Union Find**: Great for dynamic connectivity problems.
- **Topological Sort**: Key for dependency resolution (build systems, course prerequisites).