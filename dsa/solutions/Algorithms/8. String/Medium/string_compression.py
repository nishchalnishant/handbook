from typing import List

class Solution:
    def compress(self, chars: List[str]) -> int:
        """
        Problem: String Compression
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        i = 0
        index = 0
        
        while i < len(chars):
            j = i
            while j < len(chars) and chars[j] == chars[i]:
                j += 1
            
            chars[index] = chars[i]
            index += 1
            
            if j - i > 1:
                count = str(j - i)
                for c in count:
                    chars[index] = c
                    index += 1
            i = j
        return index
