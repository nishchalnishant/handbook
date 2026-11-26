"""
Union Find (Disjoint Set) patterns — Google L3/L4 interview prep.

NO CLASS — use flat arrays. Write cold in ~6 lines:

    parent = list(range(n))   # each node is its own root
    rank = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression (halving)
            x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a == b: return False           # already same component
        if rank[a] < rank[b]: a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]: rank[a] += 1
        return True

Track components separately: start at n, decrement on every successful union().
For problems with a known target node (like LC 778), just call find() to check.
"""

from typing import List
import collections

class UnionFindSolutions:
    # -----------------------------------------------------------------------
    # 1. Number of Connected Components (LC 323) — T2
    # You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph. Return the number of connected components in the graph.
    # Example: n = 5, edges = [[0,1],[1,2],[3,4]] → 2
    # Constraints: 1 <= n <= 2000
    # Time: O(E * α(N)), Space: O(N)
    # -----------------------------------------------------------------------
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return False
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1
            return True

        components = n
        for u, v in edges:
            if union(u, v):
                components -= 1
        return components

    # -----------------------------------------------------------------------
    # 2. Redundant Connection (LC 684) — T1
    # In this problem, a tree is an undirected graph that is connected and has no cycles. You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph. Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.
    # Example: edges = [[1,2],[1,3],[2,3]] → [2,3]
    # Constraints: n == edges.length, 3 <= n <= 1000, edges[i].length == 2, 1 <= ai < bi <= edges.length, ai != bi, There are no repeated edges, The given graph is connected
    # Time: O(E * α(N)), Space: O(N)
    # -----------------------------------------------------------------------
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges) + 1   # nodes are 1-indexed
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return False
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1
            return True

        for u, v in edges:
            if not union(u, v):
                return [u, v]
        return []

    # -----------------------------------------------------------------------
    # 3. Graph Valid Tree (LC 261) — T2
    # Given n nodes labeled from 0 to n-1 and a list of undirected edges, write a function to check whether these edges make up a valid tree.
    # Time: O(E * α(N)), Space: O(N)
    # -----------------------------------------------------------------------
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return False
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1
            return True

        for u, v in edges:
            if not union(u, v):
                return False
        return True

    # -----------------------------------------------------------------------
    # 4. Accounts Merge (LC 721) — T2
    # Given a list of accounts where each element accounts[i] is a list of strings, where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account. Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name. After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.
    # Example: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com → [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.
    # Constraints: 1 <= accounts.length <= 1000, 2 <= accounts[i].length <= 10, 1 <= accounts[i][j].length <= 30, accounts[i][0] consists of English letters, accounts[i][j] (for j > 0) is a valid email
    # Time: O(N * E * α(N) + N * E * log(E)), Space: O(N * E)
    # -----------------------------------------------------------------------
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        n = len(accounts)
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: 
                return
            if rank[a] < rank[b]: 
                a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: 
                rank[a] += 1

        emailToAcc = {}
        for i, a in enumerate(accounts):
            for e in a[1:]:
                if e in emailToAcc:
                    union(i, emailToAcc[e])
                else:
                    emailToAcc[e] = i

        emailGroup = collections.defaultdict(list)
        for e, i in emailToAcc.items():
            emailGroup[find(i)].append(e)

        res = []
        for i, emails in emailGroup.items():
            res.append([accounts[i][0]] + sorted(emails))
        return res
    # -----------------------------------------------------------------------
    # 5. Kruskal's MST (T2) — Sort edges by weight, union-find to avoid cycles
    # Find the Minimum Spanning Tree (MST) of a weighted undirected graph using Kruskal's algorithm. Given n nodes and a list of edges with weights, return the sum of weights of the edges in the MST.
    # Example: n = 4, edges = [[0,1,1],[1,2,2],[2,3,3],[0,3,4]] → 6
    # Constraints: 1 <= n <= 10^4
    # Time: O(E log E), Space: O(N)
    # -----------------------------------------------------------------------
    def minimumSpanningTree(self, n: int, edges: List[List[int]]) -> int:
        edges.sort(key=lambda e: e[2])
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return False
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1
            return True

        total, used = 0, 0
        for u, v, w in edges:
            if union(u, v):
                total += w
                used += 1
                if used == n - 1:
                    break
        return total if used == n - 1 else -1

    # -----------------------------------------------------------------------
    # 6. Number of Provinces (LC 547) — T2
    # There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c. A province is a group of directly or indirectly connected cities and no other cities outside of the group. You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the i^th city and the j^th city are directly connected, and isConnected[i][j] = 0 otherwise. Return the total number of provinces.
    # Example: isConnected = [[1,1,0],[1,1,0],[0,0,1]] → 2
    # Constraints: 1 <= n <= 200, n == isConnected.length, n == isConnected[i].length, isConnected[i][j] is 1 or 0, isConnected[i][i] == 1, isConnected[i][j] == isConnected[j][i]
    # Time: O(n^2 * α(n)), Space: O(n)
    # -----------------------------------------------------------------------
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return False
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1
            return True

        components = n
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1:
                    if union(i, j):
                        components -= 1
        return components

    # -----------------------------------------------------------------------
    # 8. Smallest String with Swaps (LC 1202)
    # You are given a string s, and an array of pairs of indices in the string pairs where pairs[i] = [a, b] indicates 2 indices(0-indexed) of the string. You can swap the characters at any pair of indices in the given pairs any number of times. Return the lexicographically smallest string that s can be changed to after using the swaps.
    # Time: O(N log N + E * α(N)), Space: O(N)
    # -----------------------------------------------------------------------
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        n = len(s)
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1

        for a, b in pairs:
            union(a, b)

        groups = collections.defaultdict(list)
        for i in range(n):
            groups[find(i)].append(i)

        result = list(s)
        for indices in groups.values():
            chars = sorted(s[i] for i in indices)
            for i, idx in enumerate(sorted(indices)):
                result[idx] = chars[i]
        return "".join(result)

    # -----------------------------------------------------------------------
    # 9. Satisfiability of Equality Equations (LC 990)
    # You are given an array of strings equations that represent relationships between variables where each string equations[i] is of length 4 and takes one of two forms: "xi==yi" or "xi!=yi". Return true if it is possible to assign integers to variable names so as to satisfy all the given equations, or false otherwise.
    # Time: O(N * α(26)), Space: O(26)
    # -----------------------------------------------------------------------
    def equationsPossible(self, equations: List[str]) -> bool:
        parent = list(range(26))
        rank = [0] * 26

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1

        for eq in equations:
            if eq[1] == '=':
                union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))
        for eq in equations:
            if eq[1] == '!':
                if find(ord(eq[0]) - ord('a')) == find(ord(eq[3]) - ord('a')):
                    return False
        return True

    # -----------------------------------------------------------------------
    # 10. Evaluate Division — weighted union-find variant (LC 399)
    # You are given an array of variable pairs equations and an array of real numbers values, where equations[i] = [Ai, Bi] and values[i] represent the equation Ai / Bi = values[i]. Each Ai or Bi is a string that represents a single variable. You are also given some queries, where queries[j] = [Cj, Dj] represents the jth query where you must find the answer for Cj / Dj = ?. Return the answers to all queries.
    # Time: O((E + Q) * α(N)), Space: O(N)
    # -----------------------------------------------------------------------
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        # weighted DSU: weight[x] = x / parent[x] (ratio to parent)
        parent = {}
        weight = {}

        def find(x):
            if parent[x] != x:
                root, w = find(parent[x])
                parent[x] = root
                weight[x] *= w      # compress weight all the way to root
            return parent[x], weight[x]

        def union(x, y, val):
            if x not in parent: parent[x] = x; weight[x] = 1.0
            if y not in parent: parent[y] = y; weight[y] = 1.0
            rx, wx = find(x)
            ry, wy = find(y)
            if rx == ry: return
            # x/y = val → rx/ry = val * wy / wx
            parent[rx] = ry
            weight[rx] = val * wy / wx

        for (a, b), val in zip(equations, values):
            union(a, b, val)

        results = []
        for c, d in queries:
            if c not in parent or d not in parent:
                results.append(-1.0)
            else:
                rc, wc = find(c)
                rd, wd = find(d)
                results.append(wc / wd if rc == rd else -1.0)
        return results

    # -----------------------------------------------------------------------
    # 11. Most Stones Removed with Same Row or Column (LC 947)
    # On a 2D plane, we place n stones at some integer coordinate points. Each coordinate point may have at most one stone. A stone can be removed if it shares either the same row or the same column as another stone that has not been removed. Return the largest possible number of stones that can be removed.
    # Time: O(N * α(N)), Space: O(N)
    # -----------------------------------------------------------------------
    def removeStones(self, stones: List[List[int]]) -> int:
        n = len(stones)
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1

        row_rep, col_rep = {}, {}
        for i, (r, c) in enumerate(stones):
            if r in row_rep: union(i, row_rep[r])
            else: row_rep[r] = i
            if c in col_rep: union(i, col_rep[c])
            else: col_rep[c] = i

        components = len({find(i) for i in range(n)})
        return n - components

    # -----------------------------------------------------------------------
    # 12. Number of Operations to Make Network Connected (LC 1319)
    # There are n computers numbered from 0 to n-1 connected by ethernet cables connections forming a network where connections[i] = [ai, bi] represents a connection between computers ai and bi. Any computer can reach any other computer directly or indirectly through the network. You can extract certain cables between two directly connected computers, and place them between any pair of disconnected computers to make them directly connected. Return the minimum number of times you need to do this in order to make all the computers connected. If it is not possible, return -1.
    # Time: O(E * α(N)), Space: O(N)
    # -----------------------------------------------------------------------
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        if len(connections) < n - 1:
            return -1
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a, b = find(a), find(b)
            if a == b: return False
            if rank[a] < rank[b]: a, b = b, a
            parent[b] = a
            if rank[a] == rank[b]: rank[a] += 1
            return True

        components = n
        for u, v in connections:
            if union(u, v):
                components -= 1
        return components - 1


if __name__ == "__main__":
    sol = UnionFindSolutions()

    # findRedundantConnection
    assert sol.findRedundantConnection([[1,2],[1,3],[2,3]]) == [2,3]
    assert sol.findRedundantConnection([[1,2],[2,3],[3,4],[1,4],[1,5]]) == [1,4]

    # accountsMerge
    accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],
                ["John","johnsmith@mail.com","john00@mail.com"],
                ["Mary","mary@mail.com"],
                ["John","johnnybravo@mail.com"]]
    result = sol.accountsMerge(accounts)
    assert len(result) == 3

    # validTree
    assert sol.validTree(5, [[0,1],[0,2],[0,3],[1,4]]) == True
    assert sol.validTree(5, [[0,1],[1,2],[2,3],[1,3],[1,4]]) == False

    # countComponents
    assert sol.countComponents(5, [[0,1],[1,2],[3,4]]) == 2
    assert sol.countComponents(4, [[2,3],[1,2],[1,3]]) == 2

    # smallestStringWithSwaps
    assert sol.smallestStringWithSwaps("dcab", [[0,3],[1,2]]) == "bacd"
    assert sol.smallestStringWithSwaps("dcab", [[0,3],[1,2],[0,2]]) == "abcd"
    assert sol.smallestStringWithSwaps("cba", [[0,1],[1,2]]) == "abc"

    # equationsPossible
    assert sol.equationsPossible(["a==b","b!=a"]) == False
    assert sol.equationsPossible(["b==a","a==b"]) == True
    assert sol.equationsPossible(["a==b","b==c","a==c"]) == True
    assert sol.equationsPossible(["a==b","b!=c","b==c"]) == False

    # calcEquation
    assert sol.calcEquation([["a","b"],["b","c"]], [2.0,3.0], [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]) == [6.0, 0.5, -1.0, 1.0, -1.0]

    # removeStones
    assert sol.removeStones([[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]) == 5
    assert sol.removeStones([[0,0],[0,2],[1,1],[2,0],[2,2]]) == 3
    assert sol.removeStones([[0,0]]) == 0

    # makeConnected
    assert sol.makeConnected(4, [[0,1],[0,2],[1,2]]) == 1
    assert sol.makeConnected(6, [[0,1],[0,2],[0,3],[1,2],[1,3]]) == 2
    assert sol.makeConnected(6, [[0,1],[0,2],[0,3],[1,2]]) == -1

    print("All union-find tests passed.")
