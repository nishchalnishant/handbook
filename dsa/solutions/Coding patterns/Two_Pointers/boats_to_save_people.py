from typing import List

class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        """
        Problem: Boats to Save People
        Pattern: Two Pointers - Converging (Greedy)
        Time Complexity: O(n log n) due to sorting
        Space Complexity: O(1)
        """
        people.sort()
        left, right = 0, len(people) - 1
        boats = 0
        
        while left <= right:
            # Try to pair lightest with heaviest
            if people[left] + people[right] <= limit:
                left += 1
            # Heaviest always gets on a boat (either alone or paired)
            right -= 1
            boats += 1
            
        return boats

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.numRescueBoats([3,2,2,1], 3)) # Expected: 3
