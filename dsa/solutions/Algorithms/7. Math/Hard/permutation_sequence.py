class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        """
        Problem: Permutation Sequence
        Difficulty: Hard
        Time Complexity: O(n^2)
        """
        fact = [1] * n
        for i in range(1, n):
            fact[i] = i * fact[i - 1]
            
        nums = [str(i) for i in range(1, n + 1)]
        k -= 1
        res = ""
        
        for i in range(n - 1, -1, -1):
            idx = k // fact[i]
            k %= fact[i]
            res += nums.pop(idx)
            
        return res
