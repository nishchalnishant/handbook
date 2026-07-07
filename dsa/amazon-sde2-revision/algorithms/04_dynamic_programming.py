"""
Dynamic Programming patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Getting the base cases wrong or missing edge cases (like empty strings or arrays).\n- Index out of bounds when looking at `dp[i-1]` or `dp[i][j-1]`.\n- Using 2D DP when 1D (state compression) is sufficient, wasting O(N) space.

Common Variants:
- 1D DP (Climbing Stairs, House Robber)\n- 2D DP (Unique Paths, Edit Distance)\n- Knapsack 0/1 (Partition Equal Subset Sum)\n- Subsequence (Longest Increasing Subsequence)

General Tips & Best Practices:
- Always start with top-down memoization (easier to come up with during interviews).\n- Convert to bottom-up tabular DP if you need to optimize space.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


# Quick lookup: pattern → progression exemplars + related L4 problems
CORE_DP_PATTERNS = {
    "1-D Linear": {
        "progression": ["Climbing Stairs (LC 70)", "House Robber (LC 198)", "Decode Ways (LC 91)"],
        "more_examples": [
            "House Robber II (LC 213)",
            "Min Cost Climbing Stairs (LC 746)",
            "Maximum Product Subarray (LC 152)",
            "Delete and Earn (LC 740)",
        ],
        "how_to_identify": "Given a 1D array or a number, the solution at step i only depends on a few immediately preceding steps (like i-1, i-2). Often asks for max/min or total ways to reach the end. Key question: 'What choice do I have at this current element?'",
    },
    "2-D Grid": {
        "progression": ["Unique Paths (LC 62)", "Maximal Square (LC 221)"],
        "more_examples": [
            "Unique Paths II (LC 63)",
            "Minimum Path Sum (LC 64)",
            "Triangle (LC 120)",
            "Maximal Rectangle (LC 85)",
        ],
        "how_to_identify": "The input is a 2D matrix/grid. You can only move in restricted directions (e.g., right and down). The state at (r, c) depends purely on adjacent previous cells like (r-1, c) and (r, c-1).",
    },
    "2-D String": {
        "progression": ["Edit Distance (LC 72)", "Longest Common Subsequence (LC 1143)", "Word Break (LC 139)"],
        "more_examples": [
            "Interleaving String (LC 97)",
            "Distinct Subsequences (LC 115)",
            "Longest Palindromic Subsequence (LC 516)",
            "Minimum Insertions for Palindrome (LC 1312)",
        ],
        "how_to_identify": "You are usually given two strings, one string and a dictionary (list of strings), or asked to find subsequences/palindromes within one string. State is typically dp[i][j]. (Note: If given 3+ strings, it usually becomes a 3D+ DP or requires a Trie, but the core 'matching/edit' logic remains similar).",
    },
    "Knapsack": {
        "progression": [
            "Coin Change (LC 322)",
            "Partition Equal Subset Sum (LC 416)",
            "Target Sum (LC 494)",
        ],
        "more_examples": [
            "Coin Change II (LC 518)",
            "Last Stone Weight II (LC 1049)",
            "Combination Sum IV (LC 377)",
        ],
        "how_to_identify": "You have a set of items with values/weights, and a 'target capacity' or 'target sum'. The core decision at every step is 'take it or leave it'. If items can be reused, it's Unbounded Knapsack.",
    },
    "Interval": {
        "progression": ["Burst Balloons (LC 312)"],
        "more_examples": [
            "Predict the Winner (LC 486)",
            "Stone Game (LC 877)",
            "Stone Game II (LC 1140)",
            "Minimum Cost to Cut a Stick (LC 1547)",
            "Job Scheduling (LC 1235)",
        ],
        "how_to_identify": "The problem asks for an optimal value over a continuous subsegment (interval) of the array. The DP state is dp[left][right]. The transition involves testing all 'split points' k between left and right.",
    },
}


# =============================================================================
# DP PROGRESSION — recursion → memo → tabulation (grouped by pattern)
# =============================================================================

class DPProgression:
    """Recursion → memo → tabulation for core L4 exemplars (grouped by pattern)."""

    @staticmethod
    def _is_valid_two_digit_decode(first: str, second: str) -> bool:
        """True when first+second forms a valid two-digit code (10–26)."""
        if first == "1":
            return True
        if first == "2" and second in "0123456":
            return True
        return False

    # ==================================================================
    # PATTERN 1: 1-D LINEAR DP
    # ------------------------------------------------------------------
    # State: dp[i] from dp[i-1], dp[i-2]. Core L4 building blocks.
    #
    # ★ Progression: Climbing Stairs, House Robber, Decode Ways
    # More examples: House Robber II, Min Cost Climbing Stairs,
    #                Max Product Subarray, Delete and Earn → see LinearDP
    # ==================================================================

    # ==================================================================
    # 1. CLIMBING STAIRS (LC 70)
    # ------------------------------------------------------------------
    # PROBLEM: +1 or +2 steps per move. Count ways to reach step n.
    # STATE:   ways_at_step[i] = ways to stand on step i
    # RECURRENCE: ways[i] = ways[i-1] + ways[i-2]
    # ==================================================================

    # STAGE 1 — Pure recursion (O(2^n), recomputes overlapping subproblems)
    def climb_stairs_recursion(self, n: int) -> int:
        # Base: 1 way to be on step 1; 2 ways to be on step 2.
        if n <= 2:
            return n
        ways_from_one_below = self.climb_stairs_recursion(n - 1)
        ways_from_two_below = self.climb_stairs_recursion(n - 2)
        return ways_from_one_below + ways_from_two_below

    # STAGE 2 — Top-down memo (O(n), dict cache avoids recomputation)
    def climb_stairs_memo(self, n: int) -> int:
        cache: Dict[int, int] = {}

        def ways_to_reach(step: int) -> int:
            if step <= 2:
                return step
            if step not in cache:
                from_one = ways_to_reach(step - 1)
                from_two = ways_to_reach(step - 2)
                cache[step] = from_one + from_two
            return cache[step]

        return ways_to_reach(n)

    # STAGE 3 — Bottom-up tabulation (O(n) time, O(1) space)
    def climb_stairs_tabulation(self, n: int) -> int:
        ways_at_prev_step = 1  # standing on step 1
        ways_at_curr_step = 1  # also step 1 before loop advances
        for _ in range(n - 1):
            ways_at_next_step = ways_at_curr_step + ways_at_prev_step
            ways_at_prev_step = ways_at_curr_step
            ways_at_curr_step = ways_at_next_step
        return ways_at_curr_step

    # ==================================================================
    # 2. HOUSE ROBBER (LC 198)
    # ------------------------------------------------------------------
    # PROBLEM: Max money robbing non-adjacent houses.
    # RECURRENCE: best[i] = max(nums[i]+best[i+2], best[i+1])
    # ==================================================================

    # STAGE 1 — Pure recursion
    def rob_recursion(self, nums: List[int]) -> int:
        def best_from(house_index: int) -> int:
            if house_index >= len(nums):
                return 0
            money_if_rob = nums[house_index] + best_from(house_index + 2)
            money_if_skip = best_from(house_index + 1)
            return max(money_if_rob, money_if_skip)

        return best_from(0)

    # STAGE 2 — Top-down memo
    def rob_memo(self, nums: List[int]) -> int:
        memo: Dict[int, int] = {}

        def best_from(house_index: int) -> int:
            if house_index >= len(nums):
                return 0
            if house_index not in memo:
                rob_this = nums[house_index] + best_from(house_index + 2)
                skip_this = best_from(house_index + 1)
                memo[house_index] = max(rob_this, skip_this)
            return memo[house_index]

        return best_from(0)

    # STAGE 3 — Bottom-up tabulation
    def rob_tabulation(self, nums: List[int]) -> int:
        best_two_back = 0
        best_one_back = 0
        for house_value in nums:
            best_if_rob = house_value + best_two_back
            best_if_skip = best_one_back
            best_up_to_here = max(best_if_rob, best_if_skip)
            best_two_back = best_one_back
            best_one_back = best_up_to_here
        return best_one_back

    # ==================================================================
    # 4. DECODE WAYS (LC 91)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def num_decodings_recursion(self, s: str) -> int:
        def ways_from(index: int) -> int:
            if index == len(s):
                return 1
            if s[index] == "0":
                return 0
            total = ways_from(index + 1)
            if index + 1 < len(s):
                if self._is_valid_two_digit_decode(s[index], s[index + 1]):
                    total += ways_from(index + 2)
            return total

        return ways_from(0)

    # STAGE 2 — Top-down memo
    def num_decodings_memo(self, s: str) -> int:
        memo: Dict[int, int] = {}

        def ways_from(index: int) -> int:
            if index == len(s):
                return 1
            if s[index] == "0":
                return 0
            if index not in memo:
                total = ways_from(index + 1)
                if index + 1 < len(s):
                    if self._is_valid_two_digit_decode(s[index], s[index + 1]):
                        total += ways_from(index + 2)
                memo[index] = total
            return memo[index]

        return ways_from(0)

    # STAGE 3 — Bottom-up tabulation
    def num_decodings_tabulation(self, s: str) -> int:
        n = len(s)
        ways_from = [0] * (n + 1)
        ways_from[n] = 1
        for index in range(n - 1, -1, -1):
            if s[index] == "0":
                ways_from[index] = 0
                continue
            ways_single_digit = ways_from[index + 1]
            ways_two_digit = 0
            if index + 1 < n:
                if self._is_valid_two_digit_decode(s[index], s[index + 1]):
                    ways_two_digit = ways_from[index + 2]
            ways_from[index] = ways_single_digit + ways_two_digit
        return ways_from[0]

    # ==================================================================
    # PATTERN 2: 2-D GRID DP
    # ------------------------------------------------------------------
    # State: dp[row][col] from top/left neighbors on a matrix.
    #
    # ★ Progression: Unique Paths, Maximal Square
    # More examples: Unique Paths II, Min Path Sum, Triangle,
    #                Maximal Rectangle → see GridDP
    # ==================================================================

    # ==================================================================
    # 5. UNIQUE PATHS (LC 62)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def unique_paths_recursion(self, m: int, n: int) -> int:
        def paths_from(row: int, col: int) -> int:
            if row == m - 1 and col == n - 1:
                return 1
            if row >= m or col >= n:
                return 0
            paths_going_down = paths_from(row + 1, col)
            paths_going_right = paths_from(row, col + 1)
            return paths_going_down + paths_going_right

        return paths_from(0, 0)

    # STAGE 2 — Top-down memo
    def unique_paths_memo(self, m: int, n: int) -> int:
        memo: Dict[Tuple[int, int], int] = {}

        def paths_from(row: int, col: int) -> int:
            if row == m - 1 and col == n - 1:
                return 1
            if row >= m or col >= n:
                return 0
            if (row, col) not in memo:
                down = paths_from(row + 1, col)
                right = paths_from(row, col + 1)
                memo[(row, col)] = down + right
            return memo[(row, col)]

        return paths_from(0, 0)

    # STAGE 3 — Bottom-up tabulation
    def unique_paths_tabulation(self, m: int, n: int) -> int:
        paths_in_row = [1] * n
        for row in range(1, m):
            paths_in_new_row = [1] * n
            for col in range(n - 2, -1, -1):
                paths_from_right = paths_in_new_row[col + 1]
                paths_from_above = paths_in_row[col]
                paths_in_new_row[col] = paths_from_right + paths_from_above
            paths_in_row = paths_in_new_row
        return paths_in_row[0]

    # ==================================================================
    # 11. MAXIMAL SQUARE (LC 221)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def maximal_square_recursion(self, matrix: List[List[str]]) -> int:
        if not matrix:
            return 0
        rows, cols = len(matrix), len(matrix[0])
        max_side = 0

        def square_side_at(row: int, col: int) -> int:
            if row >= rows or col >= cols:
                return 0
            if matrix[row][col] == "0":
                return 0
            side_below = square_side_at(row + 1, col)
            side_right = square_side_at(row, col + 1)
            side_diagonal = square_side_at(row + 1, col + 1)
            return 1 + min(side_below, side_right, side_diagonal)

        for row in range(rows):
            for col in range(cols):
                max_side = max(max_side, square_side_at(row, col))
        return max_side * max_side

    # STAGE 2 — Top-down memo
    def maximal_square_memo(self, matrix: List[List[str]]) -> int:
        if not matrix:
            return 0
        rows, cols = len(matrix), len(matrix[0])
        cache: Dict[Tuple[int, int], int] = {}

        def square_side_at(row: int, col: int) -> int:
            if row >= rows or col >= cols:
                return 0
            if (row, col) in cache:
                return cache[(row, col)]
            if matrix[row][col] == "0":
                cache[(row, col)] = 0
                return 0
            side_below = square_side_at(row + 1, col)
            side_right = square_side_at(row, col + 1)
            side_diagonal = square_side_at(row + 1, col + 1)
            cache[(row, col)] = 1 + min(side_below, side_right, side_diagonal)
            return cache[(row, col)]

        square_side_at(0, 0)
        max_side = max(cache.values()) if cache else 0
        return max_side * max_side

    # STAGE 3 — Bottom-up tabulation
    def maximal_square_tabulation(self, matrix: List[List[str]]) -> int:
        if not matrix:
            return 0
        rows, cols = len(matrix), len(matrix[0])
        side_len = [[0] * (cols + 1) for _ in range(rows + 1)]
        max_side = 0
        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                if matrix[row - 1][col - 1] == "0":
                    continue
                from_above = side_len[row - 1][col]
                from_left = side_len[row][col - 1]
                from_diagonal = side_len[row - 1][col - 1]
                side_len[row][col] = 1 + min(from_above, from_left, from_diagonal)
                max_side = max(max_side, side_len[row][col])
        return max_side * max_side

    # ==================================================================
    # PATTERN 3: 2-D STRING DP
    # ------------------------------------------------------------------
    # State: dp[i][j] over two string indices (edit, LCS, segmentation).
    #
    # ★ Progression: Edit Distance, LCS, Word Break
    # More examples: Interleaving String, Distinct Subsequences,
    #                LPS, Min Insertions → see StringDP
    # ==================================================================

    # ==================================================================
    # 6. EDIT DISTANCE (LC 72)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def min_distance_recursion(self, word1: str, word2: str) -> int:
        def edits(i: int, j: int) -> int:
            if i == len(word1):
                return len(word2) - j
            if j == len(word2):
                return len(word1) - i
            if word1[i] == word2[j]:
                return edits(i + 1, j + 1)
            cost_delete = 1 + edits(i + 1, j)
            cost_insert = 1 + edits(i, j + 1)
            cost_replace = 1 + edits(i + 1, j + 1)
            return min(cost_delete, cost_insert, cost_replace)

        return edits(0, 0)

    # STAGE 2 — Top-down memo
    def min_distance_memo(self, word1: str, word2: str) -> int:
        memo: Dict[Tuple[int, int], int] = {}

        def edits(i: int, j: int) -> int:
            if i == len(word1):
                return len(word2) - j
            if j == len(word2):
                return len(word1) - i
            if (i, j) not in memo:
                if word1[i] == word2[j]:
                    memo[(i, j)] = edits(i + 1, j + 1)
                else:
                    cost_delete = 1 + edits(i + 1, j)
                    cost_insert = 1 + edits(i, j + 1)
                    cost_replace = 1 + edits(i + 1, j + 1)
                    memo[(i, j)] = min(cost_delete, cost_insert, cost_replace)
            return memo[(i, j)]

        return edits(0, 0)

    # STAGE 3 — Bottom-up tabulation
    def min_distance_tabulation(self, word1: str, word2: str) -> int:
        rows = len(word1) + 1
        cols = len(word2) + 1
        edits_needed = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            edits_needed[i][cols - 1] = len(word1) - i
        for j in range(cols):
            edits_needed[rows - 1][j] = len(word2) - j
        for i in range(len(word1) - 1, -1, -1):
            for j in range(len(word2) - 1, -1, -1):
                if word1[i] == word2[j]:
                    edits_needed[i][j] = edits_needed[i + 1][j + 1]
                else:
                    delete_from_word1 = 1 + edits_needed[i + 1][j]
                    insert_into_word1 = 1 + edits_needed[i][j + 1]
                    replace_char = 1 + edits_needed[i + 1][j + 1]
                    edits_needed[i][j] = min(
                        delete_from_word1, insert_into_word1, replace_char
                    )
        return edits_needed[0][0]

    # ==================================================================
    # 7. LONGEST COMMON SUBSEQUENCE (LC 1143)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def lcs_recursion(self, text1: str, text2: str) -> int:
        def lcs_len(i: int, j: int) -> int:
            if i == len(text1) or j == len(text2):
                return 0
            if text1[i] == text2[j]:
                return 1 + lcs_len(i + 1, j + 1)
            skip_in_text1 = lcs_len(i + 1, j)
            skip_in_text2 = lcs_len(i, j + 1)
            return max(skip_in_text1, skip_in_text2)

        return lcs_len(0, 0)

    # STAGE 2 — Top-down memo
    def lcs_memo(self, text1: str, text2: str) -> int:
        memo: Dict[Tuple[int, int], int] = {}

        def lcs_len(i: int, j: int) -> int:
            if i == len(text1) or j == len(text2):
                return 0
            if (i, j) not in memo:
                if text1[i] == text2[j]:
                    memo[(i, j)] = 1 + lcs_len(i + 1, j + 1)
                else:
                    skip_in_text1 = lcs_len(i + 1, j)
                    skip_in_text2 = lcs_len(i, j + 1)
                    memo[(i, j)] = max(skip_in_text1, skip_in_text2)
            return memo[(i, j)]

        return lcs_len(0, 0)

    # STAGE 3 — Bottom-up tabulation
    def lcs_tabulation(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        lcs_len = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if text1[i] == text2[j]:
                    lcs_len[i][j] = 1 + lcs_len[i + 1][j + 1]
                else:
                    without_text1_char = lcs_len[i + 1][j]
                    without_text2_char = lcs_len[i][j + 1]
                    lcs_len[i][j] = max(without_text1_char, without_text2_char)
        return lcs_len[0][0]

    # ==================================================================
    # 9. WORD BREAK (LC 139)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def word_break_recursion(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)

        def can_split_from(start: int) -> bool:
            if start == len(s):
                return True
            for end in range(start + 1, len(s) + 1):
                piece = s[start:end]
                if piece in words and can_split_from(end):
                    return True
            return False

        return can_split_from(0)

    # STAGE 2 — Top-down memo
    def word_break_memo(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        memo: Dict[int, bool] = {}

        def can_split_from(start: int) -> bool:
            if start == len(s):
                return True
            if start in memo:
                return memo[start]
            for end in range(start + 1, len(s) + 1):
                piece = s[start:end]
                if piece in words and can_split_from(end):
                    memo[start] = True
                    return True
            memo[start] = False
            return False

        return can_split_from(0)

    # STAGE 3 — Bottom-up tabulation
    def word_break_tabulation(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        n = len(s)
        can_split_from = [False] * (n + 1)
        can_split_from[n] = True
        for start in range(n - 1, -1, -1):
            for word in words:
                word_len = len(word)
                end = start + word_len
                if end > n:
                    continue
                if s[start:end] != word:
                    continue
                if can_split_from[end]:
                    can_split_from[start] = True
                    break
        return can_split_from[0]

    # ==================================================================
    # PATTERN 4: KNAPSACK DP
    # ------------------------------------------------------------------
    # 0/1 subset sum, unbounded coin change, +/- counting.
    #
    # ★ Progression: Coin Change, Partition Equal Subset Sum, Target Sum
    # More examples: Coin Change II, Last Stone Weight II,
    #                Combination Sum IV → see KnapsackDP
    # ==================================================================

    # ==================================================================
    # 3. COIN CHANGE (LC 322)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def coin_change_recursion(self, coins: List[int], amount: int) -> int:
        IMPOSSIBLE = amount + 1

        def min_coins_for(remaining: int) -> int:
            if remaining == 0:
                return 0
            if remaining < 0:
                return IMPOSSIBLE
            best = IMPOSSIBLE
            for coin in coins:
                with_this_coin = 1 + min_coins_for(remaining - coin)
                best = min(best, with_this_coin)
            return best

        answer = min_coins_for(amount)
        return -1 if answer == IMPOSSIBLE else answer

    # STAGE 2 — Top-down memo
    def coin_change_memo(self, coins: List[int], amount: int) -> int:
        IMPOSSIBLE = amount + 1
        memo: Dict[int, int] = {}

        def min_coins_for(remaining: int) -> int:
            if remaining == 0:
                return 0
            if remaining < 0:
                return IMPOSSIBLE
            if remaining not in memo:
                best = IMPOSSIBLE
                for coin in coins:
                    with_this_coin = 1 + min_coins_for(remaining - coin)
                    best = min(best, with_this_coin)
                memo[remaining] = best
            return memo[remaining]

        answer = min_coins_for(amount)
        return -1 if answer == IMPOSSIBLE else answer

    # STAGE 3 — Bottom-up tabulation
    def coin_change_tabulation(self, coins: List[int], amount: int) -> int:
        IMPOSSIBLE = amount + 1
        min_coins = [IMPOSSIBLE] * (amount + 1)
        min_coins[0] = 0
        for target in range(1, amount + 1):
            for coin in coins:
                if target - coin < 0:
                    continue
                candidate = 1 + min_coins[target - coin]
                min_coins[target] = min(min_coins[target], candidate)
        return -1 if min_coins[amount] == IMPOSSIBLE else min_coins[amount]

    # ==================================================================
    # 8. PARTITION EQUAL SUBSET SUM (LC 416)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def can_partition_recursion(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 == 1:
            return False
        target = total // 2

        def can_make(index: int, current_sum: int) -> bool:
            if current_sum == target:
                return True
            if index == len(nums) or current_sum > target:
                return False
            include = can_make(index + 1, current_sum + nums[index])
            exclude = can_make(index + 1, current_sum)
            return include or exclude

        return can_make(0, 0)

    # STAGE 2 — Top-down memo
    def can_partition_memo(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 == 1:
            return False
        target = total // 2
        memo: Dict[Tuple[int, int], bool] = {}

        def can_make(index: int, current_sum: int) -> bool:
            if current_sum == target:
                return True
            if index == len(nums) or current_sum > target:
                return False
            key = (index, current_sum)
            if key not in memo:
                include = can_make(index + 1, current_sum + nums[index])
                exclude = can_make(index + 1, current_sum)
                memo[key] = include or exclude
            return memo[key]

        return can_make(0, 0)

    # STAGE 3 — Bottom-up tabulation
    def can_partition_tabulation(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 == 1:
            return False
        target = total // 2
        can_make_sum = [False] * (target + 1)
        can_make_sum[0] = True
        for num in nums:
            for s in range(target, num - 1, -1):
                if can_make_sum[s - num]:
                    can_make_sum[s] = True
        return can_make_sum[target]

    # ==================================================================
    # 10. TARGET SUM (LC 494)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def target_sum_recursion(self, nums: List[int], target: int) -> int:
        def count_ways(index: int, running_sum: int) -> int:
            if index == len(nums):
                return 1 if running_sum == target else 0
            add_sign = count_ways(index + 1, running_sum + nums[index])
            subtract_sign = count_ways(index + 1, running_sum - nums[index])
            return add_sign + subtract_sign

        return count_ways(0, 0)

    # STAGE 2 — Top-down memo
    def target_sum_memo(self, nums: List[int], target: int) -> int:
        memo: Dict[Tuple[int, int], int] = {}

        def count_ways(index: int, running_sum: int) -> int:
            if index == len(nums):
                return 1 if running_sum == target else 0
            key = (index, running_sum)
            if key not in memo:
                add_sign = count_ways(index + 1, running_sum + nums[index])
                subtract_sign = count_ways(index + 1, running_sum - nums[index])
                memo[key] = add_sign + subtract_sign
            return memo[key]

        return count_ways(0, 0)

    # STAGE 3 — Bottom-up tabulation
    def target_sum_tabulation(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        if (total + target) % 2 != 0:
            return 0
        if abs(target) > total:
            return 0
        subset_sum_needed = (total + target) // 2
        ways_to_sum = [0] * (subset_sum_needed + 1)
        ways_to_sum[0] = 1
        for num in nums:
            for s in range(subset_sum_needed, num - 1, -1):
                ways_to_sum[s] += ways_to_sum[s - num]
        return ways_to_sum[subset_sum_needed]

    # ==================================================================
    # PATTERN 5: INTERVAL DP
    # ------------------------------------------------------------------
    # State: dp[left][right] over a range; burst balloons is the L4 exemplar.
    #
    # ★ Progression: Burst Balloons
    # More examples: Predict the Winner, Stone Game I/II,
    #                Min Cost Cut Stick, Job Scheduling → see IntervalDP
    # ==================================================================

    # ==================================================================
    # 12. BURST BALLOONS / MAX COINS (LC 312)
    # ==================================================================

    # STAGE 1 — Pure recursion
    def max_coins_recursion(self, nums: List[int]) -> int:
        padded = [1] + nums + [1]

        def max_score(left: int, right: int) -> int:
            if left + 1 >= right:
                return 0
            best = 0
            for last_burst in range(left + 1, right):
                coins = (
                    padded[left] * padded[last_burst] * padded[right]
                    + max_score(left, last_burst)
                    + max_score(last_burst, right)
                )
                best = max(best, coins)
            return best

        return max_score(0, len(padded) - 1)

    # STAGE 2 — Top-down memo
    def max_coins_memo(self, nums: List[int]) -> int:
        padded = [1] + nums + [1]
        memo: Dict[Tuple[int, int], int] = {}

        def max_score(left: int, right: int) -> int:
            if left + 1 >= right:
                return 0
            if (left, right) in memo:
                return memo[(left, right)]
            best = 0
            for last_burst in range(left + 1, right):
                coins = (
                    padded[left] * padded[last_burst] * padded[right]
                    + max_score(left, last_burst)
                    + max_score(last_burst, right)
                )
                best = max(best, coins)
            memo[(left, right)] = best
            return best

        return max_score(0, len(padded) - 1)

    # STAGE 3 — Bottom-up tabulation
    def max_coins_tabulation(self, nums: List[int]) -> int:
        padded = [1] + nums + [1]
        n = len(padded)
        max_score = [[0] * n for _ in range(n)]
        for interval_len in range(3, n + 1):
            for left in range(0, n - interval_len + 1):
                right = left + interval_len - 1
                best_for_interval = 0
                for last_burst in range(left + 1, right):
                    burst_coins = padded[left] * padded[last_burst] * padded[right]
                    left_part = max_score[left][last_burst]
                    right_part = max_score[last_burst][right]
                    candidate = burst_coins + left_part + right_part
                    best_for_interval = max(best_for_interval, candidate)
                max_score[left][right] = best_for_interval
        return max_score[0][n - 1]


# REFERENCE SOLUTIONS BY PATTERN (Google L4 scope)
# =============================================================================

# =============================================================================
# PATTERN 1: 1-D LINEAR DP
# =============================================================================
# State: dp[i] depends on a few prior indices (i-1, i-2, ...).
# ★ Progression: Climbing Stairs, House Robber, Decode Ways
# More examples: House Robber II, Min Cost Climbing Stairs, Max Product Subarray,
#                Delete and Earn

class LinearDP:
    """Reference solutions — LinearDP."""

    def climbStairs(self, n: int) -> int:
        """Climbing Stairs (LC 70)."""
        return DPProgression().climb_stairs_tabulation(n)

    # -------------------------------------------------------------------------
    # 4. House Robber (LC 198) — T2
    # Max money from non-adjacent houses; can't rob two adjacent on same night.
    # Example: nums=[1,2,3,1] → 4  (rob idx 0 + idx 2)
    # Constraints: 1 <= nums.length <= 100, 0 <= nums[i] <= 400
    # Time: O(n), Space: O(1)
    # -------------------------------------------------------------------------
    def rob(self, nums: List[int]) -> int:
        """House Robber (LC 198)."""
        return DPProgression().rob_tabulation(nums)

    # -------------------------------------------------------------------------
    # 5. House Robber II (LC 213) — T2
    # Houses in a circle; cannot rob both first and last. Return max profit.
    # Example: nums=[2,3,2] → 3  (can't rob first+last since adjacent)
    # Constraints: 1 <= nums.length <= 100, 0 <= nums[i] <= 1000
    # Time: O(n), Space: O(1)
    # -------------------------------------------------------------------------
    def robII(self, nums: List[int]) -> int:
        """House Robber II (LC 213): circular street — cannot rob both first and last."""
        if len(nums) == 1:
            return nums[0]
        skip_first = self.rob(nums[1:])
        skip_last = self.rob(nums[:-1])
        return max(skip_first, skip_last)

    # -------------------------------------------------------------------------
    # 6. Decode Ways (LC 91) — T2
    # A message containing letters from A-Z can be encoded into numbers using the following mapping:
    # 'A' -> "1", 'B' -> "2", ..., 'Z' -> "26"
    # To decode an encoded message, all the digits must be grouped then mapped back into letters
    # using the reverse of the mapping above (there may be multiple ways).
    # For example, "11106" can be mapped into:
    # - "AAJF" with the grouping (1 1 10 6)
    # - "KJF" with the grouping (11 10 6)
    # Note that the grouping (1 11 06) is invalid because "06" cannot be mapped into 'F' since "6" is different from "06".
    # Given a string s containing only digits, return the number of ways to decode it.
    # Example: s="226" → 3  ("BZ", "VF", or "BBF")
    # Constraints: 1 <= s.length <= 100, s contains only digits
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def numDecodings(self, s: str) -> int:
        """Decode Ways (LC 91)."""
        return DPProgression().num_decodings_tabulation(s)

    # -------------------------------------------------------------------------
    # Min Cost Climbing Stairs (LC 746) — same 1-D linear recurrence
    # Pay cost[i] to leave step i; reach the top with minimum total cost.
    # Example: cost=[10,15,20] → 15
    # -------------------------------------------------------------------------
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # Append 0 for the top step.
        cost.append(0)
        # Traverse backwards and update costs in-place.
        for i in range(len(cost) - 3, -1, -1):
            cost[i] += min(cost[i + 1], cost[i + 2])
        # Return min cost starting at index 0 or index 1.
        return min(cost[0], cost[1])

    # -------------------------------------------------------------------------
    # Delete and Earn (LC 740) — House Robber on value indices
    # Pick a number x → earn all copies of x, but cannot pick x-1 or x+1.
    # Example: nums=[3,4,2] → 6  (take all 2s and all 4s)
    # -------------------------------------------------------------------------
    def deleteAndEarn(self, nums: List[int]) -> int:
        """Same pattern as House Robber: aggregate points per value, then"""
        if not nums:
            return 0
        max_val = max(nums)
        points_by_value = [0] * (max_val + 1)
        for num in nums:
            points_by_value[num] += num
        best_two_back = 0
        best_one_back = 0
        for value in range(max_val + 1):
            earn_this_value = points_by_value[value]
            best_if_take = earn_this_value + best_two_back
            best_if_skip = best_one_back
            best_up_to_value = max(best_if_take, best_if_skip)
            best_two_back = best_one_back
            best_one_back = best_up_to_value
        return best_one_back

    # -------------------------------------------------------------------------
    # Maximum Product Subarray (LC 152) — track running max AND min
    # Example: nums=[2,3,-2,4] → 6
    # -------------------------------------------------------------------------
    def maxProduct(self, nums: List[int]) -> int:
        # Initialize result with max element in case array has all negatives.
        res = max(nums)
        cur_min, cur_max = 1, 1
        for n in nums:
            # Zero resets the running products.
            if n == 0:
                cur_min, cur_max = 1, 1
                continue
            # Track old cur_max before updating.
            tmp = cur_max * n
            # Update running max and min products.
            cur_max = max(n * cur_max, n * cur_min, n)
            cur_min = min(tmp, n * cur_min, n)
            # Maintain global maximum product.
            res = max(res, cur_max)
        return res


# =============================================================================
# PATTERN 2: 2-D GRID DP
# =============================================================================
# State: dp[row][col] from cell above and/or left.
# ★ Progression: Unique Paths, Maximal Square
# More examples: Unique Paths II, Min Path Sum, Triangle, Maximal Rectangle

class GridDP:
    """Reference solutions — GridDP."""

    def uniquePaths(self, m: int, n: int) -> int:
        """Unique Paths (LC 62)."""
        return DPProgression().unique_paths_tabulation(m, n)

    # -------------------------------------------------------------------------
    # 14. Unique Paths II (LC 63) — T2
    # Like Unique Paths but grid has obstacles (1=obstacle, 0=free).
    # Example: obstacleGrid=[[0,0,0],[0,1,0],[0,0,0]] → 2
    # Constraints: 1 <= m, n <= 100, obstacleGrid[i][j] is 0 or 1
    # Time: O(m*n), Space: O(n)
    # -------------------------------------------------------------------------
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        M, N = len(obstacleGrid), len(obstacleGrid[0])
        # dp[c] stores path counts for column c of the current row.
        dp = [0] * N
        # Base case: 1 path to reach the destination initially.
        dp[N-1] = 1
        # Traverse rows and columns in reverse.
        for r in reversed(range(M)):
            for c in reversed(range(N)):
                # If obstacle, no paths can go through this cell.
                if obstacleGrid[r][c]:
                    dp[c] = 0
                elif c + 1 < N:
                    # Accumulate paths from below (dp[c]) and from the right (dp[c+1]).
                    dp[c] = dp[c] + dp[c+1]
        return dp[0]

    # -------------------------------------------------------------------------
    # 15. Interleaving String (LC 97) — T2
    # Return true if s3 is formed by interleaving s1 and s2 (preserving order).
    # Example: s1="aabcc", s2="dbbca", s3="aadbbcbcac" → True
    # Constraints: 0 <= s1.length, s2.length <= 100, s3.length <= 200
    # Time: O(m*n), Space: O(m*n)
    # -------------------------------------------------------------------------
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        # dp[c] stores min path sums for current row columns.
        dp = [0] * n
        dp[0] = grid[0][0]
        # Initialize first row prefix sums.
        for c in range(1, n):
            dp[c] = dp[c - 1] + grid[0][c]
        # Update dp row by row.
        for r in range(1, m):
            # First column can only come from above.
            dp[0] += grid[r][0]
            for c in range(1, n):
                # Update with min of coming from above (dp[c]) or left (dp[c-1]).
                dp[c] = grid[r][c] + min(dp[c], dp[c - 1])
        return dp[n - 1]

    # -------------------------------------------------------------------------
    # 33. Triangle (LC 120) — T2
    # Min path sum from apex to base of triangle; move to adjacent in row below.
    # Time: O(n^2), Space: O(n)
    # -------------------------------------------------------------------------
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        """Triangle (LC 120): Bottom-up DP starting from the second-to-last row."""
        # Initialize dp with a copy of bottom row values.
        dp = triangle[-1][:]
        # Traverse rows bottom-up.
        for r in range(len(triangle) - 2, -1, -1):
            for i in range(len(triangle[r])):
                # Current cost is cell cost + min of two adjacent options below.
                dp[i] = triangle[r][i] + min(dp[i], dp[i + 1])
        return dp[0]

    # -------------------------------------------------------------------------
    # 34. Maximal Rectangle (LC 85) — T3
    # Largest rectangle of 1s in binary matrix; use histogram DP + stack.
    # Time: O(m*n), Space: O(n)
    # -------------------------------------------------------------------------
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        """Maximal Square (LC 221): largest square of 1s; return area."""
        return DPProgression().maximal_square_tabulation(matrix)
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        n = len(matrix[0])
        heights = [0] * n
        max_area = 0
        for row in matrix:
            for c in range(n):
                heights[c] = heights[c] + 1 if row[c] == '1' else 0
            # Largest rectangle in histogram
            stack = []
            for i, h in enumerate(heights + [0]):
                while stack and heights[stack[-1]] > h:
                    height = heights[stack.pop()]
                    width = i if not stack else i - stack[-1] - 1
                    max_area = max(max_area, height * width)
                stack.append(i)
        return max_area

    # -------------------------------------------------------------------------
    # 35. Longest Turbulent Subarray (LC 978) — T2
    # Longest subarray where comparisons alternate between > and <.
    # Time: O(n), Space: O(1)
    # -------------------------------------------------------------------------
# =============================================================================
# PATTERN 3: 2-D STRING DP
# =============================================================================
# State: dp[i][j] over prefixes/suffixes of one or two strings.
# ★ Progression: Edit Distance, LCS, Word Break
# More examples: Interleaving String, Distinct Subsequences,
#                Longest Palindromic Subsequence, Min Insertions for Palindrome

class StringDP:
    """Reference solutions — StringDP."""

    def minDistance(self, word1: str, word2: str) -> int:
        """Edit Distance (LC 72)."""
        return DPProgression().min_distance_tabulation(word1, word2)

    # -------------------------------------------------------------------------
    # 13. Unique Paths (LC 62) — T2
    # Robot moves only right/down on m×n grid; return # paths to bottom-right.
    # Example: m=3, n=7 → 28
    # Constraints: 1 <= m, n <= 100
    # Time: O(m*n), Space: O(n)
    # -------------------------------------------------------------------------
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """Longest Common Subsequence (LC 1143)."""
        return DPProgression().lcs_tabulation(text1, text2)

    # -------------------------------------------------------------------------
    # 22. Longest Palindromic Subsequence (LC 516) — T2
    # Return the length of the longest palindromic subsequence in s.
    # Example: s="bbbab" → 4  ("bbbb")
    # Constraints: 1 <= s.length <= 1000, s consists of lowercase letters
    # Time: O(n^2), Space: O(n)
    # -------------------------------------------------------------------------
    def longestPalindromeSubseq(self, s: str) -> int:
        return self.longestCommonSubsequence(s, s[::-1])

    # -------------------------------------------------------------------------
    # 23. Combination Sum IV (LC 377) — T2
    # Count ordered sequences from nums that sum to target (permutations count).
    # Example: nums=[1,2,3], target=4 → 7
    # Constraints: 1 <= nums.length <= 200, 1 <= target <= 1000
    # Time: O(target * len(nums)), Space: O(target)
    # -------------------------------------------------------------------------
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        # Length check.
        if len(s1) + len(s2) != len(s3): return False
        # dp[i][j] represents if s1[i:] and s2[j:] can form s3[i+j:].
        dp = [[False] * (len(s2) + 1) for i in range(len(s1) + 1)]
        # Base case: empty suffixes.
        dp[len(s1)][len(s2)] = True
        # Traverse in reverse.
        for i in range(len(s1), -1, -1):
            for j in range(len(s2), -1, -1):
                # If current character of s1 matches s3, check transitions.
                if i < len(s1) and s1[i] == s3[i + j] and dp[i + 1][j]:
                    dp[i][j] = True
                # If current character of s2 matches s3, check transitions.
                if j < len(s2) and s2[j] == s3[i + j] and dp[i][j + 1]:
                    dp[i][j] = True
        return dp[0][0]

    # -------------------------------------------------------------------------
    # 16. House Robber III (LC 337) — T2
    # Max money from binary tree; cannot rob directly-linked parent-child nodes.
    # Example: root=[3,2,3,null,3,null,1] → 7  (3+3+1)
    # Constraints: 1 <= tree nodes <= 10^4, 0 <= Node.val <= 10^4
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """Word Break (LC 139): can s be split into dictionary words?"""
        return DPProgression().word_break_tabulation(s, wordDict)

    # -------------------------------------------------------------------------
    # Distinct Subsequences (LC 115) — 2-D string DP (space-optimized 1-D)
    # -------------------------------------------------------------------------
    def numDistinct(self, s: str, t: str) -> int:
        # dp[i][j] = number of distinct subsequences of s[:i] which equals t[:j]
        m, n = len(s), len(t)
        # We can space optimize this to a 1D array
        dp = [0] * (n + 1)
        dp[0] = 1 # Empty string t is a subsequence of any string s 1 time

        for i in range(1, m + 1):
            # Iterate backwards to avoid using updated values from the same row
            for j in range(n, 0, -1):
                if s[i - 1] == t[j - 1]:
                    dp[j] += dp[j - 1]

        return dp[n]

    # -------------------------------------------------------------------------
    # Minimum Insertions for Palindrome (LC 1312) — n - LPS(s)
    # -------------------------------------------------------------------------
    def minInsertions(self, s: str) -> int:
        n = len(s)
        # Reversed string t.
        t = s[::-1]
        # dp[i][j] will store the LCS of s[:i] and t[:j].
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        # Populate 2D grid bottom-up.
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                # If characters match, increment.
                if s[i - 1] == t[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    # Otherwise, carry over max from adjacent subproblems.
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        # Min insertions is total length minus LPS length.
        return n - dp[n][n]


# =============================================================================
# PATTERN 4: KNAPSACK DP (0/1 and unbounded)
# =============================================================================
# 0/1: each item once — iterate items, update sums backwards.
# Unbounded: unlimited coins — iterate amounts forward per coin type.
# ★ Progression: Coin Change, Partition Equal Subset Sum, Target Sum
# More examples: Coin Change II, Last Stone Weight II, Combination Sum IV

class KnapsackDP:
    """Reference solutions — KnapsackDP."""

    def coinChange(self, coins: List[int], amount: int) -> int:
        """Coin Change (LC 322)."""
        return DPProgression().coin_change_tabulation(coins, amount)

    # -------------------------------------------------------------------------
    # 10. Coin Change II (LC 518) — T2
    # Count # combinations (unlimited coins) that sum to amount; return 0 if none.
    # Example: amount=5, coins=[1,2,5] → 4  (5; 2+2+1; 2+1+1+1; 1+1+1+1+1)
    # Constraints: 1 <= coins.length <= 300, 0 <= amount <= 5000
    # Time: O(amount * len(coins)), Space: O(amount)
    # -------------------------------------------------------------------------
    def change(self, amount: int, coins: List[int]) -> int:
        """Coin Change II (LC 518): count combinations (not orderings) summing to amount."""
        ways_to_make = [0] * (amount + 1)
        ways_to_make[0] = 1
        for coin in coins:
            for target in range(coin, amount + 1):
                ways_without_this_coin = ways_to_make[target - coin]
                ways_to_make[target] += ways_without_this_coin
        return ways_to_make[amount]

    # -------------------------------------------------------------------------
    # 11. Longest Increasing Subsequence (LC 300) — T2
    # Return the length of the longest strictly increasing subsequence.
    # Example: nums=[10,9,2,5,3,7,101,18] → 4  ([2,3,7,101])
    # Constraints: 1 <= nums.length <= 2500, -10^4 <= nums[i] <= 10^4
    # Time: O(n log n), Space: O(n)
    # -------------------------------------------------------------------------
    def canPartition(self, nums: List[int]) -> bool:
        """Partition Equal Subset Sum (LC 416)."""
        return DPProgression().can_partition_tabulation(nums)

    # -------------------------------------------------------------------------
    # 8. Target Sum (LC 494) — T2
    # Assign +/- to each number; count expressions that evaluate to target.
    # Example: nums=[1,1,1,1,1], target=3 → 5
    # Constraints: 1 <= nums.length <= 20, 0 <= nums[i] <= 1000
    # Time: O(n * sum), Space: O(n * sum)
    # -------------------------------------------------------------------------
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        """Target Sum (LC 494)."""
        return DPProgression().target_sum_tabulation(nums, target)

    # -------------------------------------------------------------------------
    # 9. Coin Change I (LC 322) — T2
    # Fewest coins to make amount; return -1 if impossible.
    # Example: coins=[1,2,5], amount=11 → 3  (5+5+1)
    # Constraints: 1 <= coins.length <= 12, 0 <= amount <= 10^4
    # Time: O(amount * len(coins)), Space: O(amount)
    # -------------------------------------------------------------------------
    def lastStoneWeightII(self, stones: List[int]) -> int:
        stoneSum = sum(stones)
        target = stoneSum // 2
        # dp[j] is True if subset sum j is achievable.
        dp = [False] * (target + 1)
        # Base case: sum 0 is always achievable.
        dp[0] = True
        currMax = 0
        for stone in stones:
            # Update achievable sums backwards (0/1 Knapsack style).
            for j in range(target, stone - 1, -1):
                dp[j] = dp[j] or dp[j - stone]
                if dp[j]:
                    currMax = max(currMax, j)
        # Result is difference between two parts.
        return stoneSum - 2 * currMax

    # -------------------------------------------------------------------------
    # 21. Longest Common Subsequence (LC 1143) — T2
    # Return length of the LCS of text1 and text2 (non-contiguous, ordered).
    # Example: text1="abcde", text2="ace" → 3  ("ace")
    # Constraints: 1 <= text1.length, text2.length <= 1000
    # Time: O(m*n), Space: O(m*n)
    # -------------------------------------------------------------------------
    def combinationSum4(self, nums: List[int], target: int) -> int:
        # dp[total] will hold number of permutations summing to total.
        dp = {0: 1}
        # Compute ways for each target sum.
        for total in range(1, target + 1):
            dp[total] = 0
            for n in nums:
                # Add ways to reach (total - n).
                dp[total] += dp.get(total - n, 0)
        return dp[target]


# =============================================================================
# PATTERN 5: SUBSEQUENCE DP
# =============================================================================
# Longest increasing subsequence — patience sorting + binary search.

class SubsequenceDP:
    """Reference solutions — SubsequenceDP."""

    def lengthOfLIS(self, nums: List[int]) -> int:
        import bisect
        # tails holds smallest tail elements for each increasing subsequence length.
        tails = []
        for x in nums:
            # Find insertion index for x in sorted list of tails.
            i = bisect.bisect_left(tails, x)
            # If x is larger than all elements, append to extend LIS.
            if i == len(tails):
                tails.append(x)
            else:
                # Otherwise replace to optimize future expansions.
                tails[i] = x
        return len(tails)


# =============================================================================
# PATTERN 6: STOCK DP (state machine)
# =============================================================================
# Track buy/sell states across days; at most k transactions.

class StockDP:
    """Reference solutions — StockDP."""

    def maxProfitII(self, prices: List[int]) -> int:
        profit = 0
        # Iterate over prices day by day.
        for i in range(1, len(prices)):
            # If price went up, add profit difference (greedy).
            if prices[i] > prices[i-1]:
                profit += (prices[i] - prices[i-1])
        return profit

    def maxProfitIII(self, prices: List[int]) -> int:
        if not prices:
            return 0
        # buy1, buy2 initialized to negative of first day's price.
        buy1, sell1 = -prices[0], 0
        buy2, sell2 = -prices[0], 0
        # Single pass to update all four states.
        for price in prices[1:]:
            # Best cost after first buy.
            buy1 = max(buy1, -price)
            # Best profit after first sell.
            sell1 = max(sell1, buy1 + price)
            # Best net after second buy.
            buy2 = max(buy2, sell1 - price)
            # Best profit after second sell.
            sell2 = max(sell2, buy2 + price)
        return sell2


# =============================================================================
# PATTERN 7: INTERVAL DP
# =============================================================================
# State: dp[left][right] over contiguous ranges; fill by increasing length.
# ★ Progression: Burst Balloons
# More examples: Predict the Winner, Stone Game I/II,
#                Min Cost Cut Stick, Job Scheduling

class IntervalDP:
    """Reference solutions — IntervalDP."""

    def maxCoins(self, nums: List[int]) -> int:
        """Burst Balloons (LC 312)."""
        return DPProgression().max_coins_tabulation(nums)
    def predictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)
        # dp[i][j] = max score difference (cur_player - other) for nums[i..j]
        dp = [[0] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = nums[i]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])
        return dp[0][n-1] >= 0

    # -------------------------------------------------------------------------
    # Stone Game (LC 877) — interval DP (Alice always wins; show DP approach)
    # Both play optimally from ends of piles; return true if Alice wins.
    # Example: piles=[5,3,4,5] → True
    # Constraints: 2 <= piles.length <= 500
    # Time: O(n^2), Space: O(n)
    # -------------------------------------------------------------------------
    def stoneGame(self, piles: List[int]) -> bool:
        n = len(piles)
        # dp[i] stores the score advantage starting at pile i for current length.
        dp = piles[:]
        # Compute transitions for subarray lengths from 2 to n.
        for length in range(2, n + 1):
            new_dp = [0] * n
            for i in range(n - length + 1):
                j = i + length - 1
                # Choose left pile (piles[i]) or right pile (piles[j]) subtract opponent score.
                new_dp[i] = max(piles[i] - dp[i+1], piles[j] - dp[i])
            dp = new_dp
        return dp[0] > 0

    # -------------------------------------------------------------------------
    # Stone Game II (LC 1140) — DP with M state
    # Alice goes first; on turn take 1..2M piles; return max stones Alice gets.
    # Example: piles=[5,3,4,5] → 10
    # Constraints: 2 <= piles.length <= 100, 1 <= piles[i] <= 10^4
    # Time: O(n^2), Space: O(n^2)
    # -------------------------------------------------------------------------
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)
        stones_remaining_from = piles[:]
        for i in range(n - 2, -1, -1):
            stones_remaining_from[i] += stones_remaining_from[i + 1]

        memo: Dict[Tuple[int, int], int] = {}

        def score_from(pile_index: int, max_take: int) -> int:
            if pile_index >= n:
                return 0
            state = (pile_index, max_take)
            if state in memo:
                return memo[state]
            if pile_index + 2 * max_take >= n:
                memo[state] = stones_remaining_from[pile_index]
                return memo[state]
            best_score = 0
            for piles_taken in range(1, 2 * max_take + 1):
                opponent_score = score_from(
                    pile_index + piles_taken,
                    max(max_take, piles_taken),
                )
                my_score = stones_remaining_from[pile_index] - opponent_score
                best_score = max(best_score, my_score)
            memo[state] = best_score
            return best_score

        return score_from(0, 1)

    def minCost(self, n: int, cuts: List[int]) -> int:
        # Sort cuts and add virtual cuts at boundaries 0 and n.
        cuts = sorted([0] + cuts + [n])
        m = len(cuts)
        # dp[i][j] stores the min cost to make all cuts between cuts[i] and cuts[j].
        dp = [[0] * m for _ in range(m)]
        # Solve for increasing interval lengths.
        for length in range(2, m):
            for i in range(m - length):
                j = i + length
                dp[i][j] = float('inf')
                # Try all intermediate cuts k.
                for k in range(i + 1, j):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i])
        return dp[0][m - 1]

    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        import bisect
        jobs = sorted(zip(endTime, startTime, profit))
        # dp[i] = max profit using first i jobs (1-indexed)
        dp = [0] * (len(jobs) + 1)
        end_times = [0] + [j[0] for j in jobs]
        for i, (end, start, p) in enumerate(jobs, 1):
            # Latest job that ends <= start of current job
            j = bisect.bisect_right(end_times, start, 0, i) - 1
            dp[i] = max(dp[i - 1], dp[j] + p)
        return dp[len(jobs)]


# =============================================================================
# PATTERN 8: TREE DP
# =============================================================================
# Post-order on tree: return (rob_root, skip_root) per node.

class TreeDP:
    """Reference solutions — TreeDP."""

    def robIII(self, root) -> int:
        def dfs(root):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: empty tree.
            if not root: return [0, 0]
            # Recursively solve for left and right subtrees.
            leftPair = dfs(root.left)
            rightPair = dfs(root.right)
            # If we rob root, we cannot rob left/right children (use leftPair[1] / rightPair[1]).
            withRoot = root.val + leftPair[1] + rightPair[1]
            # If we skip root, take max of either option for left and right children.
            withoutRoot = max(leftPair) + max(rightPair)
            return [withRoot, withoutRoot]
        # Return max value starting from root.
        return max(dfs(root))


# =============================================================================
# PROBLEM CATALOG — grouped by pattern
# =============================================================================

PRACTICE_QUESTIONS = [
    {"id": 1, "pattern": "1-D Linear", "lc": 70, "name": "Climbing Stairs", "progression": True},
    {"id": 2, "pattern": "1-D Linear", "lc": 198, "name": "House Robber", "progression": True},
    {"id": 3, "pattern": "1-D Linear", "lc": 91, "name": "Decode Ways", "progression": True},
    {"id": 4, "pattern": "1-D Linear", "lc": 213, "name": "House Robber II", "progression": False},
    {"id": 5, "pattern": "1-D Linear", "lc": 746, "name": "Min Cost Climbing Stairs", "progression": False},
    {"id": 6, "pattern": "1-D Linear", "lc": 152, "name": "Maximum Product Subarray", "progression": False},
    {"id": 44, "pattern": "1-D Linear", "lc": 740, "name": "Delete and Earn", "progression": False},
    {"id": 7, "pattern": "2-D Grid", "lc": 62, "name": "Unique Paths", "progression": True},
    {"id": 8, "pattern": "2-D Grid", "lc": 63, "name": "Unique Paths II", "progression": False},
    {"id": 9, "pattern": "2-D Grid", "lc": 64, "name": "Minimum Path Sum", "progression": False},
    {"id": 10, "pattern": "2-D Grid", "lc": 120, "name": "Triangle", "progression": False},
    {"id": 11, "pattern": "2-D Grid", "lc": 221, "name": "Maximal Square", "progression": True},
    {"id": 12, "pattern": "2-D Grid", "lc": 85, "name": "Maximal Rectangle", "progression": False},
    {"id": 13, "pattern": "2-D String", "lc": 72, "name": "Edit Distance", "progression": True},
    {"id": 14, "pattern": "2-D String", "lc": 1143, "name": "Longest Common Subsequence", "progression": True},
    {"id": 15, "pattern": "2-D String", "lc": 139, "name": "Word Break", "progression": True},
    {"id": 16, "pattern": "2-D String", "lc": 97, "name": "Interleaving String", "progression": False},
    {"id": 19, "pattern": "2-D String", "lc": 115, "name": "Distinct Subsequences", "progression": False},
    {"id": 20, "pattern": "2-D String", "lc": 516, "name": "Longest Palindromic Subsequence", "progression": False},
    {"id": 21, "pattern": "2-D String", "lc": 1312, "name": "Min Insertions for Palindrome", "progression": False},
    {"id": 22, "pattern": "Knapsack", "lc": 322, "name": "Coin Change", "progression": True},
    {"id": 23, "pattern": "Knapsack", "lc": 518, "name": "Coin Change II", "progression": False},
    {"id": 24, "pattern": "Knapsack", "lc": 416, "name": "Partition Equal Subset Sum", "progression": True},
    {"id": 25, "pattern": "Knapsack", "lc": 494, "name": "Target Sum", "progression": True},
    {"id": 26, "pattern": "Knapsack", "lc": 1049, "name": "Last Stone Weight II", "progression": False},
    {"id": 27, "pattern": "Knapsack", "lc": 377, "name": "Combination Sum IV", "progression": False},
    {"id": 28, "pattern": "Subsequence", "lc": 300, "name": "Longest Increasing Subsequence", "progression": False},
    {"id": 29, "pattern": "Stock", "lc": 122, "name": "Best Time to Buy/Sell Stock II", "progression": False},
    {"id": 30, "pattern": "Stock", "lc": 123, "name": "Best Time to Buy/Sell Stock III", "progression": False},
    {"id": 31, "pattern": "Interval", "lc": 312, "name": "Burst Balloons", "progression": True},
    {"id": 32, "pattern": "Interval", "lc": 486, "name": "Predict the Winner", "progression": False},
    {"id": 33, "pattern": "Interval", "lc": 877, "name": "Stone Game", "progression": False},
    {"id": 34, "pattern": "Interval", "lc": 1140, "name": "Stone Game II", "progression": False},
    {"id": 36, "pattern": "Interval", "lc": 1547, "name": "Minimum Cost to Cut a Stick", "progression": False},
    {"id": 37, "pattern": "Interval", "lc": 1235, "name": "Job Scheduling", "progression": False},
    {"id": 38, "pattern": "Tree", "lc": 337, "name": "House Robber III", "progression": False},
]


if __name__ == "__main__":
    prog = DPProgression()
    assert prog.climb_stairs_recursion(10) == prog.climb_stairs_memo(10) == prog.climb_stairs_tabulation(10)
    assert prog.rob_recursion([1, 2, 3, 1]) == prog.rob_memo([1, 2, 3, 1]) == prog.rob_tabulation([1, 2, 3, 1])
    assert prog.coin_change_recursion([1, 5, 11], 15) == prog.coin_change_memo([1, 5, 11], 15) == prog.coin_change_tabulation([1, 5, 11], 15)

    linear = LinearDP()
    grid = GridDP()
    string_dp = StringDP()
    knapsack = KnapsackDP()
    subseq = SubsequenceDP()
    stock = StockDP()
    interval = IntervalDP()
    tree = TreeDP()

    # --- Linear ---
    assert linear.climbStairs(10) == 89
    assert linear.rob([1, 2, 3, 1]) == 4
    assert linear.robII([2, 3, 2]) == 3
    assert linear.numDecodings("226") == 3
    assert linear.minCostClimbingStairs([10, 15, 20]) == 15
    assert linear.deleteAndEarn([3, 4, 2]) == 6
    assert linear.maxProduct([2, 3, -2, 4]) == 6

    # --- Grid ---
    assert grid.uniquePaths(3, 7) == 28
    assert grid.uniquePathsWithObstacles([[0,0,0],[0,1,0],[0,0,0]]) == 2
    assert grid.minPathSum([[1,3,1],[1,5,1],[4,2,1]]) == 7
    assert grid.minimumTotal([[2],[3,4],[6,5,7],[4,1,8,3]]) == 11
    assert grid.maximalSquare([["1","0","1","0","0"],["1","0","1","1","1"],
                               ["1","1","1","1","1"],["1","0","0","1","0"]]) == 4
    assert grid.maximalRectangle([["1","0","1","0","0"],["1","0","1","1","1"],
                                  ["1","1","1","1","1"],["1","0","0","1","0"]]) == 6

    # --- String ---
    assert string_dp.minDistance("horse", "ros") == 3
    assert string_dp.longestCommonSubsequence("abcde", "ace") == 3
    assert string_dp.wordBreak("leetcode", ["leet", "code"]) == True
    assert string_dp.isInterleave("aabcc", "dbbca", "aadbbcbcac") == True
    assert string_dp.numDistinct("rabbbit", "rabbit") == 3
    assert string_dp.minInsertions("mbadm") == 2

    # --- Knapsack ---
    assert knapsack.coinChange([1, 5, 11], 15) == 3
    assert knapsack.change(5, [1, 2, 5]) == 4
    assert knapsack.canPartition([1, 5, 11, 5]) == True
    assert knapsack.findTargetSumWays([1,1,1,1,1], 3) == 5
    assert knapsack.lastStoneWeightII([2,7,4,1,8,1]) == 1

    # --- Subsequence ---
    assert subseq.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    # --- Stock ---
    assert stock.maxProfitII([7,1,5,3,6,4]) == 7
    assert stock.maxProfitIII([3,3,5,0,0,3,1,4]) == 6

    # --- Interval ---
    assert interval.maxCoins([3, 1, 5, 8]) == 167
    assert interval.predictTheWinner([1, 5, 233, 7]) == True
    assert interval.stoneGame([5, 3, 4, 5]) == True
    assert interval.stoneGameII([2, 7, 9, 4, 4]) == 10
    assert interval.minCost(7, [1,3,4,5]) == 16
    assert interval.jobScheduling([1,2,3,3], [3,4,5,6], [50,10,40,70]) == 120

    # --- Tree ---
    # robIII needs tree node — skip unless we have stub

    print("All dynamic programming tests passed.")
