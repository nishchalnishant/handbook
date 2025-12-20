import bisect

def max_bridges(pairs):
    """
    Problem: Building Bridges. Connect North bank cities to South bank cities.
    Pairs (N_i, S_i). No crossing bridges.
    
    Approach: LIS
    - Sort pairs by North bank coordinate.
    - Find LIS of South bank coordinates.
    - Similar to Russian Doll Envelopes but one dimension can be equal.
    
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    # Sort by north increasing, then south increasing
    pairs.sort()
    
    south_coords = [p[1] for p in pairs]
    
    # Simple LIS using bisect (patience sorting)
    tails = []
    for x in south_coords:
        idx = bisect.bisect_left(tails, x)
        if idx < len(tails):
            tails[idx] = x
        else:
            tails.append(x)
            
    return len(tails)

# Example Usage
if __name__ == "__main__":
    # (North, South)
    pairs = [(6, 2), (4, 3), (2, 6), (1, 5)]
    print(f"Max non-crossing bridges: {max_bridges(pairs)}")
