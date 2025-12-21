"""
Medium Recursion Problems
-------------------------
This file contains solutions to 10 common medium difficulty recursion problems.
"""

# 1. Subsets (Power Set)
# Generate all possible subsets of a set
def subsets(nums):
    res = []
    def backtrack(start, curr):
        res.append(list(curr))
        for i in range(start, len(nums)):
            curr.append(nums[i])
            backtrack(i + 1, curr)
            curr.pop()
    backtrack(0, [])
    return res

# 2. Permutations
# Generate all permutations of an array
def permutations(nums):
    res = []
    def backtrack(curr):
        if len(curr) == len(nums):
            res.append(list(curr))
            return
        for n in nums:
            if n not in curr:
                curr.append(n)
                backtrack(curr)
                curr.pop()
    backtrack([])
    return res

# 3. Tower of Hanoi
# Solve the classic Tower of Hanoi puzzle
def tower_of_hanoi(n, source, target, auxiliary):
    if n == 1:
        # print(f"Move disk 1 from {source} to {target}")
        return 1
    moves = tower_of_hanoi(n - 1, source, auxiliary, target)
    # print(f"Move disk {n} from {source} to {target}")
    moves += 1
    moves += tower_of_hanoi(n - 1, auxiliary, target, source)
    return moves

# 4. Combination Sum
# Find all combinations that sum to a target value
def combination_sum(candidates, target):
    res = []
    def backtrack(remain, start, curr):
        if remain == 0:
            res.append(list(curr))
            return
        if remain < 0:
            return
        for i in range(start, len(candidates)):
            curr.append(candidates[i])
            backtrack(remain - candidates[i], i, curr)
            curr.pop()
    backtrack(target, 0, [])
    return res

# 5. Letter Combinations of a Phone Number
# Map digits to letters
def letter_combinations(digits):
    if not digits: return []
    mapping = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
    }
    res = []
    def backtrack(index, curr):
        if index == len(digits):
            res.append(curr)
            return
        for char in mapping[digits[index]]:
            backtrack(index + 1, curr + char)
    backtrack(0, "")
    return res

# 6. Generate Parentheses
# Generate all valid combinations of n pairs of parentheses
def generate_parentheses(n):
    res = []
    def backtrack(curr, open_count, close_count):
        if len(curr) == 2 * n:
            res.append(curr)
            return
        if open_count < n:
            backtrack(curr + "(", open_count + 1, close_count)
        if close_count < open_count:
            backtrack(curr + ")", open_count, close_count + 1)
    backtrack("", 0, 0)
    return res

# 7. Subset Sum
# Check if a subset exists with a given sum
def is_subset_sum(arr, n, sum_val):
    if sum_val == 0:
        return True
    if n == 0:
        return False
    if arr[n - 1] > sum_val:
        return is_subset_sum(arr, n - 1, sum_val)
    return is_subset_sum(arr, n - 1, sum_val) or is_subset_sum(arr, n - 1, sum_val - arr[n - 1])

# 8. Josephus Problem
# Find the survivor in a circle of people
def josephus(n, k):
    if n == 1:
        return 0
    return (josephus(n - 1, k) + k) % n

# 9. String to Integer (atoi)
# Implement atoi recursively (simplified)
def atoi(s):
    s = s.strip()
    if not s: return 0
    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]
    
    def helper(s, current_val):
        if not s or not s[0].isdigit():
            return current_val
        return helper(s[1:], current_val * 10 + int(s[0]))
    
    return sign * helper(s, 0)

# 10. Binary Tree Traversal
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder(root, res):
    if root:
        res.append(root.val)
        preorder(root.left, res)
        preorder(root.right, res)

def inorder(root, res):
    if root:
        inorder(root.left, res)
        res.append(root.val)
        inorder(root.right, res)

def postorder(root, res):
    if root:
        postorder(root.left, res)
        postorder(root.right, res)
        res.append(root.val)

if __name__ == "__main__":
    # Sample Test Cases
    print(f"Subsets of [1,2,3]: {subsets([1,2,3])}")
    print(f"Permutations of [1,2,3]: {len(permutations([1,2,3]))} permutations found.")
    print(f"Tower of Hanoi moves for 3 disks: {tower_of_hanoi(3, 'A', 'C', 'B')}")
    print(f"Combination Sum for 7 in [2,3,6,7]: {combination_sum([2,3,6,7], 7)}")
    print(f"Letter combinations of '23': {letter_combinations('23')}")
    print(f"Generate Parentheses for n=3: {generate_parentheses(3)}")
    print(f"Subset Sum (11) in [2,3,7,8,10]: {is_subset_sum([2,3,7,8,10], 5, 11)}")
    print(f"Josephus problem (n=5, k=3): {josephus(5, 3)}") # Expect 3 (0-indexed)
    print(f"Atoi '-1234': {atoi('-1234')}")
    
    root = Node(1, Node(2), Node(3))
    res_in = []
    inorder(root, res_in)
    print(f"Inorder Traversal: {res_in}")
