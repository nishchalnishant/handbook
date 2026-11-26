"""
Recursion & Backtracking patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Forgetting to make a deep copy when appending the path to the result (`res.append(path[:])` instead of `res.append(path)`).\n- Not removing the element after the recursive call (the 'backtrack' step).\n- Not passing the correct `start` index to avoid permutations when combinations are needed.

Common Variants:
- Subsets / Subsets II (with duplicates)\n- Permutations / Permutations II\n- Combination Sum (I, II, III)\n- Word Search / N-Queens

General Tips & Best Practices:
- Sort the input array first if you need to skip duplicates.\n- Draw the state-space tree to understand what `path` and `start` should represent.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List

class RecursionBacktrackingSolutions:
    # -----------------------------------------------------------------------
    # 1. Word Search (LC 79) — T1
    # Given an m x n grid of characters board and a string word, return true if word exists in the grid. The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.
    # Example: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED" → true
    # Constraints: m == board.length, n = board[i].length, 1 <= m, n <= 6, 1 <= word.length <= 15, board and word consists of only lowercase and uppercase English letters, Follow up: Could you use search pruning to make your solution faster with a larger board?
    # Time: O(m * n * 4^len(word)), Space: O(len(word))
    # -----------------------------------------------------------------------
    def exist(self, board: List[List[str]], word: str) -> bool:
        """Word Search (LC 79): Use DFS backtracking starting from every cell that matches word[0]."""
        ROWS, COLS = len(board), len(board[0])
        # Use a set to track cells in the current DFS path to prevent re-use.
        path = set()
        def dfs(r, c, i):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: successfully matched the entire word.
            if i == len(word):
                return True
            # Reject if out of bounds, mismatching character, or already visited in current path.
            if (r < 0 or c < 0 or r >= ROWS or c >= COLS or
                word[i] != board[r][c] or (r, c) in path):
                return False
            # Mark the current cell as visited.
            path.add((r, c))
            # Explore all 4 adjacent directions.
            res = (dfs(r + 1, c, i + 1) or
                   dfs(r - 1, c, i + 1) or
                   dfs(r, c + 1, i + 1) or
                   dfs(r, c - 1, i + 1))
            # Backtrack: remove the current cell from the path.
            path.remove((r, c))
            return res
        # Try starting DFS from every cell in the grid.
        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0): return True
        return False

    # -----------------------------------------------------------------------
    # 2. Generate Parentheses (LC 22) — T1
    # Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
    # Example: n = 3 → ["((()))","(()())","(())()","()(())","()()()"]
    # Constraints: 1 <= n <= 8
    # Time: O(4^n / sqrt(n)), Space: O(n)
    # -----------------------------------------------------------------------
    def generateParenthesis(self, n: int) -> List[str]:
        stack = []
        res = []
        def backtrack(openN, closedN):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: reached valid combinations of length 2*n.
            if openN == closedN == n:
                res.append("".join(stack))
                return
            # Add an open parenthesis if we have remaining open parentheses.
            if openN < n:
                stack.append("(")
                backtrack(openN + 1, closedN)
                # Backtrack to try other combinations.
                stack.pop()
            # Add a close parenthesis only if it doesn't exceed open parentheses.
            if closedN < openN:
                stack.append(")")
                backtrack(openN, closedN + 1)
                # Backtrack to try other combinations.
                stack.pop()
        # Begin backtracking starting with 0 open and 0 close parenthesis.
        backtrack(0, 0)
        return res

class RecursionBacktrackingSolutionsT2:
    # -----------------------------------------------------------------------
    # 3. Subsets (LC 78) — T2
    # Given an integer array nums of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.
    # Example: nums = [1,2,3] → [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
    # Constraints: 1 <= nums.length <= 10, 10 <= nums[i] <= 10, All the numbers of nums are unique
    # Time: O(n * 2^n), Space: O(n)
    # -----------------------------------------------------------------------
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """Subsets (LC 78): Use DFS with an index pointer."""
        res = []
        subset = []
        def dfs(i):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: reached the end of the array, add copy of subset.
            if i >= len(nums):
                res.append(subset.copy())
                return
            # Branch 1: Include nums[i] in the subset.
            subset.append(nums[i])
            dfs(i + 1)
            # Branch 2: Exclude nums[i] from the subset (backtrack).
            subset.pop()
            dfs(i + 1)
        # Begin DFS from the first element.
        dfs(0)
        return res

    # -----------------------------------------------------------------------
    # 4. Subsets II (LC 90) — T2
    # Given an integer array nums that may contain duplicates, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.
    # Example: nums = [1,2,2] → [[],[1],[1,2],[1,2,2],[2],[2,2]]
    # Constraints: 1 <= nums.length <= 10, 10 <= nums[i] <= 10
    # Time: O(n * 2^n), Space: O(n)
    # -----------------------------------------------------------------------
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res = []
        # Sort nums to group duplicates together.
        nums.sort()
        def backtrack(i, subset):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: reached the end of the array, add copy of subset.
            if i == len(nums):
                res.append(subset[::])
                return
            # Choice 1: Include nums[i] in the subset.
            subset.append(nums[i])
            backtrack(i + 1, subset)
            # Choice 2: Exclude nums[i] from the subset (backtrack).
            subset.pop()
            # Skip all duplicate elements at the current level.
            while i + 1 < len(nums) and nums[i] == nums[i + 1]:
                i += 1
            backtrack(i + 1, subset)
        # Begin backtracking from index 0.
        backtrack(0, [])
        return res

    # -----------------------------------------------------------------------
    # 5. Permutations (LC 46) — T2
    # Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.
    # Example: nums = [1,2,3] → [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    # Constraints: 1 <= nums.length <= 6, 10 <= nums[i] <= 10, All the integers of nums are unique
    # Time: O(n * n!), Space: O(n)
    # -----------------------------------------------------------------------
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        # Base case: single element has only one permutation.
        if len(nums) == 1:
            return [nums[:]]
        # Generate permutations by rotating elements.
        for i in range(len(nums)):
            # Remove the first element from the remaining pool.
            n = nums.pop(0)
            # Find all permutations of the remaining elements.
            perms = self.permute(nums)
            # Append the removed element to each generated permutation.
            for perm in perms:
                perm.append(n)
            res.extend(perms)
            # Re-add the removed element to restore state.
            nums.append(n)
        return res

    # -----------------------------------------------------------------------
    # 6. Permutations II (LC 47) — T2
    # Given a collection of numbers, nums, that might contain duplicates, return all possible unique permutations in any order.
    # Example: nums = [1,2,3] → [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    # Constraints: 1 <= nums.length <= 8, 10 <= nums[i] <= 10
    # Time: O(n * n!), Space: O(n)
    # -----------------------------------------------------------------------
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        res = []
        perm = []
        # Count frequencies of each number to naturally handle duplicates.
        count = {n: 0 for n in nums}
        for n in nums:
            count[n] += 1
        def dfs():
            """Depth-first-search helper for the enclosing solution."""
            # Base case: permutation length matches input size.
            if len(perm) == len(nums):
                res.append(perm.copy())
                return
            # Explore each unique number in the frequency map.
            for n in count:
                if count[n] > 0:
                    perm.append(n)
                    count[n] -= 1
                    dfs()
                    # Backtrack: restore count and pop from permutation.
                    count[n] += 1
                    perm.pop()
        # Begin DFS generation.
        dfs()
        return res

    # -----------------------------------------------------------------------
    # 7. Combination Sum (LC 39) — T2
    # Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order. The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different. The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.
    # Example: candidates = [2,3,6,7], target = 7 → [[2,2,3],[7]]
    # Constraints: 1 <= candidates.length <= 30, 2 <= candidates[i] <= 40, All elements of candidates are distinct, 1 <= target <= 40
    # Time: O(2^(target/min(candidates))), Space: O(target/min(candidates))
    # -----------------------------------------------------------------------
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        def dfs(i, cur, total):
            """Depth-first-search helper for the enclosing solution."""
            # Target reached, append a copy of current combination.
            if total == target:
                res.append(cur.copy())
                return
            # Stop if index is out of bounds or running sum exceeds target.
            if i >= len(candidates) or total > target:
                return
            # Choice 1: Include candidates[i] (can be repeated).
            cur.append(candidates[i])
            dfs(i, cur, total + candidates[i])
            # Choice 2: Exclude candidates[i] (backtrack).
            cur.pop()
            dfs(i + 1, cur, total)
        # Start search from the first candidate.
        dfs(0, [], 0)
        return res

    # -----------------------------------------------------------------------
    # 8. Combination Sum II (LC 40) — T2
    # Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sum to target. Each number in candidates may only be used once in the combination. Note: The solution set must not contain duplicate combinations.
    # Constraints: 1 <= candidates.length <= 100, 1 <= candidates[i] <= 50, 1 <= target <= 30
    # Time: O(2^n), Space: O(n)
    # -----------------------------------------------------------------------
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        # Sort candidates to handle duplicates easily.
        candidates.sort()
        res = []
        def backtrack(cur, pos, target):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Target sum achieved.
            if target == 0:
                res.append(cur.copy())
                return
            # Prune path if target sum is exceeded.
            if target <= 0:
                return
            prev = -1
            # Try adding candidates starting from position pos.
            for i in range(pos, len(candidates)):
                # Skip duplicate elements at the same recursion depth.
                if candidates[i] == prev:
                    continue
                cur.append(candidates[i])
                # Recurse with i+1 since each element can only be used once.
                backtrack(cur, i + 1, target - candidates[i])
                # Backtrack.
                cur.pop()
                prev = candidates[i]
        # Begin backtracking search.
        backtrack([], 0, target)
        return res

    # -----------------------------------------------------------------------
    # 10. Palindrome Partitioning (LC 131) — T2
    # Given a string s, partition s such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of s.
    # Example: s = "aab" → [["a","a","b"],["aa","b"]]
    # Constraints: 1 <= s.length <= 16, s contains only lowercase English letters
    # Time: O(n * 2^n), Space: O(n)
    # -----------------------------------------------------------------------
    def partition(self, s: str) -> List[List[str]]:
        res = []
        part = []
        def dfs(i):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: reached the end of the string, record partition.
            if i >= len(s):
                res.append(part.copy())
                return
            # Explore all possible substring partitions starting from index i.
            for j in range(i, len(s)):
                # If substring s[i:j+1] is a palindrome, recurse on the suffix.
                if self.isPali(s, i, j):
                    part.append(s[i : j + 1])
                    dfs(j + 1)
                    # Backtrack to explore other partitions.
                    part.pop()
        # Begin DFS search.
        dfs(0)
        return res

    def isPali(self, s, l, r):
        """Returns whether is pali holds for the provided input."""
        # Check matching characters from outside in.
        while l < r:
            if s[l] != s[r]: return False
            l, r = l + 1, r - 1
        return True

    # -----------------------------------------------------------------------
    # 11. Letter Combinations of a Phone Number (LC 17) — T2
    # Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order. A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.
    # Example: digits = "23" → ["ad","ae","af","bd","be","bf","cd","ce","cf"]
    # Constraints: 1 <= digits.length <= 4, digits[i] is a digit in the range ['2', '9']
    # Time: O(4^n * n), Space: O(n)
    # -----------------------------------------------------------------------
    def letterCombinations(self, digits: str) -> List[str]:
        res = []
        digitToChar = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "qprs", "8": "tuv", "9": "wxyz"
        }
        def backtrack(i, curStr):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: combination length matches input digit length.
            if len(curStr) == len(digits):
                res.append(curStr)
                return
            # Map current digit to mapped characters.
            for c in digitToChar[digits[i]]:
                # Recurse with the next digit and new string prefix.
                backtrack(i + 1, curStr + c)
        # Avoid running search if input string is empty.
        if digits:
            backtrack(0, "")
        return res

    # -----------------------------------------------------------------------
    # 12. Combinations (LC 77) — T2
    # Given two integers n and k, return all possible combinations of k numbers chosen from the range [1, n]. You may return the answer in any order.
    # Example: n = 4, k = 2 → [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
    # Constraints: 1 <= n <= 20, 1 <= k <= n
    # Time: O(k * C(n, k)), Space: O(k)
    # -----------------------------------------------------------------------
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        def backtrack(start, comb):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: combination length reaches k.
            if len(comb) == k:
                res.append(comb.copy())
                return
            # Choose numbers from start to n.
            for i in range(start, n + 1):
                comb.append(i)
                # Recurse to build combination.
                backtrack(i + 1, comb)
                # Backtrack.
                comb.pop()
        # Begin backtracking from number 1.
        backtrack(1, [])
        return res

    # -----------------------------------------------------------------------
    # 13. Target Sum (LC 494) — T2
    # You are given an integer array nums and an integer target. You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums and then concatenate all the integers. to build the expression "+2-1". Return the number of different expressions that you can build, which evaluates to target.
    # Example: nums = [1,1,1,1,1], target = 3 → 5
    # Constraints: 1 <= nums.length <= 20, 0 <= nums[i] <= 1000, 0 <= sum(nums[i]) <= 1000, 1000 <= target <= 1000
    # Time: O(n * sum(nums)), Space: O(n * sum(nums))
    # -----------------------------------------------------------------------
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        dp = {}
        def backtrack(i, total):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: processed all numbers. Return 1 if target sum reached, else 0.
            if i == len(nums): return 1 if total == target else 0
            # Return cached result if already computed.
            if (i, total) in dp: return dp[(i, total)]
            # Recurse by trying both addition and subtraction.
            dp[(i, total)] = (backtrack(i + 1, total + nums[i]) +
                              backtrack(i + 1, total - nums[i]))
            return dp[(i, total)]
        # Begin backtracking from index 0 with initial sum 0.
        return backtrack(0, 0)

    # -----------------------------------------------------------------------
    # 16. Combination Sum III (LC 216) — T2
    # Find all valid combinations of k numbers that sum up to n such that the following conditions are true: Return a list of all possible valid combinations. The list must not contain the same combination twice, and the combinations may be returned in any order.
    # Example: k = 3, n = 7 → [[1,2,4]]
    # Constraints: 2 <= k <= 9, 1 <= n <= 60
    # Time: O(C(9, k) * k), Space: O(k)
    # -----------------------------------------------------------------------
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        res = []
        def backtrack(start, comb, total):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: if we selected k elements, save if sum equals n.
            if len(comb) == k:
                if total == n:
                    res.append(comb.copy())
                return
            # Select unique numbers from start to 9.
            for i in range(start, 10):
                # Prune tree if current sum exceeds target n.
                if total + i > n:
                    break
                comb.append(i)
                # Recurse.
                backtrack(i + 1, comb, total + i)
                # Backtrack.
                comb.pop()
        # Begin backtracking from number 1.
        backtrack(1, [], 0)
        return res

    # -----------------------------------------------------------------------
    # 17. Letter Case Permutation (LC 784) — T2
    # Given a string s, you can transform every letter individually to be lowercase or uppercase to create another string. Return a list of all possible strings we could create. Return the output in any order.
    # Example: s = "a1b2" → ["a1b2","a1B2","A1b2","A1B2"]
    # Constraints: 1 <= s.length <= 12, s consists of lowercase English letters, uppercase English letters, and digits
    # Time: O(2^n * n), Space: O(n)
    # -----------------------------------------------------------------------
    def letterCasePermutation(self, s: str) -> List[str]:
        res = []
        def backtrack(i, cur_str):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: reached the end of the string.
            if i == len(s):
                res.append(cur_str)
                return
            # If the current character is a letter, branch into lower and upper case options.
            if s[i].isalpha():
                backtrack(i + 1, cur_str + s[i].lower())
                backtrack(i + 1, cur_str + s[i].upper())
            # Otherwise, digits are appended deterministically.
            else:
                backtrack(i + 1, cur_str + s[i])
        # Begin backtracking search from index 0.
        backtrack(0, "")
        return res

class RecursionBacktrackingSolutionsT3:
    # -----------------------------------------------------------------------
    # 19. Beautiful Arrangement (LC 526)
    # Suppose you have n integers labeled 1 through n. A permutation of those n integers perm is called beautiful if for every i (1-indexed), either perm[i] is divisible by i, or i is divisible by perm[i]. Given an integer n, return the number of the beautiful arrangements that you can construct.
    # Example: n = 2 → 2
    # Constraints: 1 <= n <= 15
    # Time: O(k) where k is the number of valid arrangements, Space: O(n)
    # -----------------------------------------------------------------------
    def countArrangement(self, n: int) -> int:
        visited = [False] * (n + 1)
        self._count = 0
        def backtrack(pos):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: placed all n integers.
            if pos > n:
                self._count += 1
                return
            # Try placing each unused integer from 1 to n.
            for num in range(1, n + 1):
                # Check if it satisfies the beautiful arrangement condition.
                if not visited[num] and (num % pos == 0 or pos % num == 0):
                    # Mark as used and recurse.
                    visited[num] = True
                    backtrack(pos + 1)
                    # Backtrack: mark as unused.
                    visited[num] = False
        # Begin backtracking from position 1.
        backtrack(1)
        return self._count


    # -----------------------------------------------------------------------
    # 21. Restore IP Addresses (LC 93)
    # A valid IP address consists of exactly four integers separated by single dots where each integer is between 0 and 255 (inclusive) with no leading zeros. Given a string s containing only digits, return all valid IP addresses that can be formed by inserting dots into s.
    # Example: s = "25525511135" → ["255.255.11.135","255.255.111.35"]
    # Constraints: 1 <= s.length <= 20, s consists of digits only
    # Time: O(1) — at most 3^4 = 81 splits to check, Space: O(1)
    # -----------------------------------------------------------------------
    def restoreIpAddresses(self, s: str) -> List[str]:
        res = []
        def backtrack(start, parts):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: 4 segments placed.
            if len(parts) == 4:
                # If the entire string is consumed, we have a valid IP.
                if start == len(s):
                    res.append('.'.join(parts))
                return
            # Try segment lengths 1, 2, and 3 starting from position start.
            for length in range(1, 4):
                # Ensure the segment does not go out of bounds.
                if start + length > len(s):
                    break
                segment = s[start:start + length]
                # Leading zeros: a segment starting with '0' is invalid if length > 1.
                if len(segment) > 1 and segment[0] == '0':
                    break
                # Value check: must not exceed 255.
                if int(segment) > 255:
                    break
                # Choose: append segment.
                parts.append(segment)
                # Recurse for the next segment.
                backtrack(start + length, parts)
                # Backtrack: pop segment.
                parts.pop()
        # Initialize backtracking from start index 0 and empty parts.
        backtrack(0, [])
        return res

    # -----------------------------------------------------------------------
    # 22. Gray Code (LC 89)
    # An n-bit gray code sequence is a sequence of 2^n integers where every integer is in the inclusive range [0, 2^n - 1], begins with 0, each successive pair of values differs by exactly one bit, and the first and last values also differ by exactly one bit. Given an integer n, return any valid n-bit gray code sequence.
    # Example: n = 2 → [0,1,3,2]
    # Constraints: 1 <= n <= 16
    # Time: O(2^n), Space: O(2^n)
    # -----------------------------------------------------------------------
    def grayCode(self, n: int) -> List[int]:
        return [i ^ (i >> 1) for i in range(1 << n)]

    # -----------------------------------------------------------------------
    # 23. Matchsticks to Square (LC 473)
    # You are given an integer array matchsticks where matchsticks[i] is the length of the ith matchstick. You want to use all the matchsticks to make one square. Do not break any stick, but you can link them up. Return true if you can make this square and false otherwise.
    # Example: matchsticks = [1,1,2,2,2] → true
    # Constraints: 1 <= matchsticks.length <= 15, 1 <= matchsticks[i] <= 10^8
    # Time: O(4^n), Space: O(n)
    # -----------------------------------------------------------------------
    def makesquare(self, matchsticks: List[int]) -> bool:
        total = sum(matchsticks)
        # Total sum of matchsticks must be divisible by 4.
        if total % 4 != 0:
            return False
        target = total // 4
        # Sort descending to fail early on large matchsticks that exceed targets.
        matchsticks.sort(reverse=True)
        # Initialize the lengths of the 4 square sides.
        sides = [0] * 4

        def backtrack(i):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: all matchsticks successfully placed.
            if i == len(matchsticks):
                # Verify that all 4 sides equal the target.
                return sides[0] == sides[1] == sides[2] == target
            # Track side lengths tried at this recursion depth to skip duplicates.
            seen = set()
            for s in range(4):
                # Symmetrical pruning: if this side sum was already tried, skip.
                if sides[s] in seen:
                    continue
                # If current matchstick fits on side s, try placing it.
                if sides[s] + matchsticks[i] <= target:
                    seen.add(sides[s])
                    # Choose: add matchstick.
                    sides[s] += matchsticks[i]
                    # Recurse.
                    if backtrack(i + 1):
                        return True
                    # Backtrack: remove matchstick.
                    sides[s] -= matchsticks[i]
            return False

        return backtrack(0)

    # -----------------------------------------------------------------------
    # 24. Partition to K Equal Sum Subsets (LC 698)
    # Given an integer array nums and an integer k, return true if it is possible to divide this array into k non-empty subsets whose sums are all equal.
    # Example: nums = [4,3,2,3,5,2,1], k = 4 → true
    # Constraints: 1 <= k <= len(nums) <= 16, 1 <= nums[i] <= 10^4, The frequency of each element is in the range [1, 4]
    # Time: O(k * 2^n), Space: O(n)
    # -----------------------------------------------------------------------
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        total = sum(nums)
        # Total sum of elements must be divisible by k.
        if total % k != 0:
            return False
        target = total // k
        # Sort descending to try largest elements first for early branch pruning.
        nums.sort(reverse=True)
        # If the largest number is greater than target, partition is impossible.
        if nums[0] > target:
            return False
        # Initialize the current sums of k subsets/buckets.
        buckets = [0] * k

        def backtrack(i):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: all numbers have been placed in buckets.
            if i == len(nums):
                return True
            # Track bucket sums already tried at this decision step to avoid redundancy.
            seen = set()
            for j in range(k):
                # Symmetrical pruning: skip if a bucket with the same sum was already processed.
                if buckets[j] in seen:
                    continue
                # Try placing nums[i] in bucket j.
                if buckets[j] + nums[i] <= target:
                    seen.add(buckets[j])
                    # Choose: add number to bucket.
                    buckets[j] += nums[i]
                    # Recurse.
                    if backtrack(i + 1):
                        return True
                    # Backtrack: remove number from bucket.
                    buckets[j] -= nums[i]
            return False

        return backtrack(0)

    # -----------------------------------------------------------------------
    # 26. Strobogrammatic Number II (LC 247)
    # Given an integer n, return all the strobogrammatic numbers that are of length n. A strobogrammatic number is a number that looks the same when rotated 180 degrees (upside down).
    # Example: n = 2 → ["11","69","88","96"]
    # Constraints: 1 <= n <= 14
    # Time: O(5^(n/2)), Space: O(5^(n/2))
    # -----------------------------------------------------------------------
    def findStrobogrammatic(self, n: int) -> List[str]:
        def helper(n, total):
            """Helper routine used by the enclosing solution."""
            # Base cases: empty string for even lengths, center digits for odd lengths.
            if n == 0:
                return [""]
            if n == 1:
                return ["0", "1", "8"]
            # Recursively generate inner strobogrammatic numbers of length n-2.
            middles = helper(n - 2, total)
            result = []
            # Wrap inner numbers with valid outer pairs.
            for mid in middles:
                for left, right in [('1', '1'), ('6', '9'), ('8', '8'), ('9', '6')]:
                    result.append(left + mid + right)
                # Outer '0...0' is only valid if we are not at the outermost level.
                if n != total:
                    result.append('0' + mid + '0')
            return result
        # Kickoff helper with length n and target total.
        return helper(n, n)

    # -----------------------------------------------------------------------
    # 27. Generalized Abbreviation (LC 320)
    # A word's generalized abbreviation can be constructed by replacing any combination of non-overlapping, non-adjacent substrings with their respective lengths. Given a string word, return a list of all the possible generalized abbreviations of word.
    # Example: word = "word" → ["4","3d","2r1","2rd","1o2","1o1d","1or1","1ord","w3","w2d","w1r1","w1rd","wo2","wo1d","wor1","word"]
    # Constraints: 1 <= word.length <= 15
    # Time: O(2^n), Space: O(n)
    # -----------------------------------------------------------------------
    def generateAbbreviations(self, word: str) -> List[str]:
        res = []
        def backtrack(i, current, count):
            """Backtracking helper that explores candidate states for the enclosing solution."""
            # Base case: reached end of the word.
            if i == len(word):
                # Append final count if any accumulated abbreviation remains.
                res.append(current + (str(count) if count > 0 else ""))
                return
            # Choice 1: Abbreviate current character (increment running count).
            backtrack(i + 1, current, count + 1)
            # Choice 2: Keep current character (flush count and append current char).
            backtrack(i + 1, current + (str(count) if count > 0 else "") + word[i], 0)
        # Begin backtracking from index 0.
        backtrack(0, "", 0)
        return res

    # -----------------------------------------------------------------------
    # 28. Count Numbers with Unique Digits (LC 357)
    # Given an integer n, return the count of all numbers with unique digits x where 0 <= x < 10^n.
    # Example: n = 2 → 91
    # Constraints: 0 <= n <= 8
    # Time: O(1) — bounded by n <= 8 and 10 digits, Space: O(n)
    # -----------------------------------------------------------------------
    def countNumbersWithUniqueDigits(self, n: int) -> int:
        # Base case: 10^0 = 1 number (0).
        if n == 0:
            return 1
        # Initialize result with count for n=1 (10 numbers: 0 to 9).
        result = 10
        # Permutations of first digit (9 choices: 1-9).
        unique_digits = 9
        # Choices for subsequent positions (9, 8, 7...).
        available_digits = 9
        # Calculate permutations for lengths 2 up to n (capped at 10).
        for i in range(2, min(n, 10) + 1):
            unique_digits *= available_digits
            result += unique_digits
            available_digits -= 1
        return result


if __name__ == "__main__":
    sol = RecursionBacktrackingSolutions()
    sol2 = RecursionBacktrackingSolutionsT2()

    # exist
    board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    assert sol.exist(board, "ABCCED") == True
    assert sol.exist(board, "SEE") == True
    assert sol.exist(board, "ABCB") == False

    # generateParenthesis
    res = sol.generateParenthesis(3)
    assert len(res) == 5
    assert "((()))" in res and "(()())" in res

    # subsets
    res = sorted([sorted(s) for s in sol2.subsets([1, 2, 3])])
    assert res == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

    # subsetsWithDup
    res = sorted([sorted(s) for s in sol2.subsetsWithDup([1, 2, 2])])
    assert res == [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]

    # permute
    res = sorted(sol2.permute([1, 2, 3]))
    assert len(res) == 6
    assert [1, 2, 3] in res

    # permuteUnique
    res = sorted(sol2.permuteUnique([1, 1, 2]))
    assert len(res) == 3
    assert [1, 1, 2] in res

    # combinationSum
    res = sorted([sorted(c) for c in sol2.combinationSum([2, 3, 6, 7], 7)])
    assert res == [[2, 2, 3], [7]]

    # combinationSum2
    res = sorted([sorted(c) for c in sol2.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)])
    assert res == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]

    # partition (palindrome partitioning)
    res = sorted([sorted(p) for p in sol2.partition("aab")])
    assert ["a", "a", "b"] in [sorted(p) for p in sol2.partition("aab")]
    assert ["aa", "b"] in sol2.partition("aab")

    # letterCombinations
    res = sorted(sol2.letterCombinations("23"))
    assert res == sorted(["ad","ae","af","bd","be","bf","cd","ce","cf"])
    assert sol2.letterCombinations("") == []

    # combine
    res = sorted([sorted(c) for c in sol2.combine(4, 2)])
    assert res == [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]

    # findTargetSumWays
    assert sol2.findTargetSumWays([1, 1, 1, 1, 1], 3) == 5
    assert sol2.findTargetSumWays([1], 1) == 1

    # combinationSum3
    res = sorted([sorted(c) for c in sol2.combinationSum3(3, 7)])
    assert res == [[1, 2, 4]]

    sol3 = RecursionBacktrackingSolutionsT3()

    # countArrangement (Beautiful Arrangement)
    assert sol3.countArrangement(1) == 1
    assert sol3.countArrangement(2) == 2

    # restoreIpAddresses
    res = sorted(sol3.restoreIpAddresses("25525511135"))
    assert res == sorted(["255.255.11.135", "255.255.111.35"])
    assert sol3.restoreIpAddresses("0000") == ["0.0.0.0"]

    # grayCode
    res = sol3.grayCode(2)
    assert res[0] == 0
    assert len(res) == 4
    for i in range(len(res) - 1):
        assert bin(res[i] ^ res[i + 1]).count('1') == 1
    assert bin(res[-1] ^ res[0]).count('1') == 1

    # makesquare (Matchsticks to Square)
    assert sol3.makesquare([1, 1, 2, 2, 2]) == True
    assert sol3.makesquare([3, 3, 3, 3, 4]) == False

    # canPartitionKSubsets
    assert sol3.canPartitionKSubsets([4, 3, 2, 3, 5, 2, 1], 4) == True
    assert sol3.canPartitionKSubsets([1, 2, 3, 4], 3) == False

    # findStrobogrammatic
    res = sorted(sol3.findStrobogrammatic(2))
    assert res == sorted(["11", "69", "88", "96"])
    res = sorted(sol3.findStrobogrammatic(1))
    assert res == sorted(["0", "1", "8"])

    # generateAbbreviations
    res = sol3.generateAbbreviations("word")
    assert len(res) == 16
    assert "word" in res
    assert "4" in res

    # countNumbersWithUniqueDigits
    assert sol3.countNumbersWithUniqueDigits(0) == 1
    assert sol3.countNumbersWithUniqueDigits(2) == 91

    print("All recursion/backtracking tests passed.")
