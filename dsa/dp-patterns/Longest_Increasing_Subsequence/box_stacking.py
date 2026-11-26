def box_stacking(dims):
    """
    Problem: Given boxes (l, w, h), stack them such that box on top has strictly smaller l and w. Maximize height.
    Allowed to rotate boxes.
    
    Approach: LIS
    - Generate all 3 rotations for each box.
    - Sort boxes by base area (l*w) or just l (if consistent).
    - Apply LIS on max height.
    - Condition: box i can be on box j if l_i < l_j and w_i < w_j.
    
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    """
    boxes = []
    for l, w, h in dims:
        # Generate permutations where we fix height
        boxes.append((max(l, w), min(l, w), h))
        boxes.append((max(w, h), min(w, h), l))
        boxes.append((max(l, h), min(l, h), w))
        
    # Sort by base area descending
    boxes.sort(key=lambda x: x[0] * x[1], reverse=True)
    
    n = len(boxes)
    heights = [box[2] for box in boxes]
    
    for i in range(1, n):
        for j in range(i):
            # Check if i can go on top of j
            if boxes[i][0] < boxes[j][0] and boxes[i][1] < boxes[j][1]:
                heights[i] = max(heights[i], heights[j] + boxes[i][2])
                
    return max(heights) if heights else 0

# Example Usage
if __name__ == "__main__":
    # (l, w, h)
    dims = [(4, 6, 7), (1, 2, 3), (4, 5, 6), (10, 12, 32)]
    print(f"Max height: {box_stacking(dims)}")
