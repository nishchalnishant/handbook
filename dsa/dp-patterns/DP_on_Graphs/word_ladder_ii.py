def find_ladders(beginWord, endWord, wordList):
    """
    Problem: Leetcode 126. Find all shortest transformation sequences.
    
    Approach: BFS to find min depth + Backtracking/DFS to finding paths.
    - Standard Graph problem, often grouped with 'DP on Graphs' due to state transitions.
    
    Time Complexity: O(M^2 * N) (BFS) + Path reconstruction
    Space Complexity: O(M^2 * N)
    """
    word_set = set(wordList)
    if endWord not in word_set: return []
    
    # Check simple BFS first
    import collections
    layer = {beginWord: [[beginWord]]}
    
    while layer:
        new_layer = collections.defaultdict(list)
        for w in layer:
            if w == endWord:
                return layer[w]
            
            for i in range(len(w)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    new_w = w[:i] + c + w[i+1:]
                    if new_w in word_set:
                        for path in layer[w]:
                            new_layer[new_w].append(path + [new_w])
                            
        word_set -= set(new_layer.keys())
        layer = new_layer
        
    return []

# Example Usage
if __name__ == "__main__":
    begin = "hit"
    end = "cog"
    words = ["hot","dot","dog","lot","log","cog"]
    print(f"Shortest ladders: {find_ladders(begin, end, words)}")
