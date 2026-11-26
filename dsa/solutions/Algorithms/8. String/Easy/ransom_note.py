from collections import Counter

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        """
        Problem: Ransom Note
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        cnt_ransom = Counter(ransomNote)
        cnt_mag = Counter(magazine)
        
        for char, count in cnt_ransom.items():
            if cnt_mag[char] < count:
                return False
        return True
