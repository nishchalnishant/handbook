class Solution:
    def countPrimes(self, n: int) -> int:
        """
        Problem: Count Primes (Sieve of Eratosthenes)
        Difficulty: Medium
        Time Complexity: O(n log log n)
        Space Complexity: O(n)
        """
        if n <= 2: return 0
        
        primes = [True] * n
        primes[0] = primes[1] = False
        
        for i in range(2, int(n**0.5) + 1):
            if primes[i]:
                # Mark multiples
                primes[i*i : n : i] = [False] * len(primes[i*i : n : i])
                
        return sum(primes)
