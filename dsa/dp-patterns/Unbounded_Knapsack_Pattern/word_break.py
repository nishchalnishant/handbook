def word_break(s, wordDict):
    """
    Problem: Leetcode 139. Segment string s into dictionary words.
    
    Approach: Unbounded Knapsack / DP
    - dp[i] = True if s[0...i-1] can be segmented.
    - dp[i] = any(dp[j] and s[j...i-1] in dict) for j < i.
    
    Time Complexity: O(N^2) (or O(N^2 * K) depending on string slice)
    Space Complexity: O(N)
    """
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
                
    return dp[n]

# Example Usage
if __name__ == "__main__":
    s = "leetcode"
    words = ["leet", "code"]
    print(f"Can break: {word_break(s, words)}")
