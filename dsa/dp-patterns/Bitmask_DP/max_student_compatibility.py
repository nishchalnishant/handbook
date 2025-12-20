def max_compatibility_sum(students, mentors):
    """
    Problem: Assign M students to M mentors one-to-one to maximize compatibility score (sum of matching answers).
    
    Approach: Bitmask DP
    - dp[mask] = max score assigning first 'k' students to mentors in 'mask'.
    - 'k' = number of set bits in mask.
    - If mask has k bits set, it means we have assigned k mentors to the first k students (0...k-1).
    - Transition: Try adding m-th mentor (if bit m not set in mask) to (k+1)-th student?
    - Cleaner: dp[mask] = max score for assigning a set of mentors (mask) to the first count(mask) students.
    
    Time Complexity: O(2^M * M)
    Space Complexity: O(2^M)
    """
    m = len(students) # Number of students/mentors
    n = len(students[0]) # Number of questions
    
    # Precompute scores between student i and mentor j
    scores = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            score = 0
            for q in range(n):
                if students[i][q] == mentors[j][q]:
                    score += 1
            scores[i][j] = score
            
    dp = [-1] * (1 << m)
    dp[0] = 0
    
    for mask in range(1 << m):
        if dp[mask] == -1: continue
        
        # Number of set bits = index of next student to assign
        student_idx = bin(mask).count('1')
        if student_idx == m: continue
        
        # Try assigning any unassigned mentor j to student_idx
        for j in range(m):
            if not ((mask >> j) & 1):
                new_mask = mask | (1 << j)
                dp[new_mask] = max(dp[new_mask], dp[mask] + scores[student_idx][j])
                
    return dp[(1 << m) - 1]

# Example Usage
if __name__ == "__main__":
    students = [[1,1,0],[1,0,1],[0,0,1]]
    mentors = [[1,0,0],[0,0,1],[1,1,0]]
    print(f"Max compatibility: {max_compatibility_sum(students, mentors)}")
