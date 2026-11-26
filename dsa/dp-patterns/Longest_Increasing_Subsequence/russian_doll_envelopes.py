import bisect

def max_envelopes(envelopes):
    """
    Problem: Max number of envelopes you can Russian doll (fit inside one another).
    One envelope (w1, h1) fits in (w2, h2) if w1 < w2 AND h1 < h2.
    
    Approach: LIS Pattern (2D Geometry variation)
    - Sort by width (asc). If widths are same, sort by height (desc).
    - Explanation for sorting: solving LIS on heights.
        - If widths same [3, 3] and [3, 4], we can't put [3,3] in [3,4].
        - Sorting heights desc ensures we don't pick [3,3] then [3,4] as a sequence, since 4 comes before 3.
    - Find LIS of heights.
    
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    # Sort width asc, then height desc
    envelopes.sort(key=lambda x: (x[0], -x[1]))
    
    # LIS on heights
    heights = [h for _, h in envelopes]
    lis = []
    
    for h in heights:
        idx = bisect.bisect_left(lis, h)
        if idx == len(lis):
            lis.append(h)
        else:
            lis[idx] = h
            
    return len(lis)

# Example Usage
if __name__ == "__main__":
    envelopes = [[5,4],[6,4],[6,7],[2,3]]
    print(f"Max envelopes: {max_envelopes(envelopes)}")
