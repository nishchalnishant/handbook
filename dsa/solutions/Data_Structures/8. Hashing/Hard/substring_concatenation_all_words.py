from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        """
        Problem: Substring with Concatenation of All Words
        Difficulty: Hard
        Time Complexity: O(n * m * len)
        Space Complexity: O(m * len)
        """
        if not s or not words: return []
        
        word_len = len(words[0])
        total_len = len(words) * word_len
        word_count = {}
        
        for w in words:
            word_count[w] = word_count.get(w, 0) + 1
            
        res = []
        for i in range(len(s) - total_len + 1):
            sub = s[i : i + total_len]
            seen = {}
            for j in range(0, total_len, word_len):
                curr_word = sub[j : j + word_len]
                if curr_word in word_count:
                    seen[curr_word] = seen.get(curr_word, 0) + 1
                    if seen[curr_word] > word_count[curr_word]:
                        break
                else:
                    break
            else:
                res.append(i)
        return res
