class Solution:
    def towerOfHanoi(self, n: int, source: str, auxiliary: str, target: str) -> None:
        """
        Problem: Tower of Hanoi
        Difficulty: Medium
        Time Complexity: O(2^n)
        Space Complexity: O(n)
        """
        if n == 1:
            print(f"Move disk 1 from {source} to {target}")
            return
        
        self.towerOfHanoi(n - 1, source, target, auxiliary)
        print(f"Move disk {n} from {source} to {target}")
        self.towerOfHanoi(n - 1, auxiliary, source, target)

if __name__ == "__main__":
    sol = Solution()
    sol.towerOfHanoi(3, 'A', 'B', 'C')
