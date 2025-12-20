import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Solution:
    """
    Problem: Closest Pair of Points
    Difficulty: Hard
    Time Complexity: O(n log n)
    """
    def dist(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def bruteForce(self, P, n):
        min_dist = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                if self.dist(P[i], P[j]) < min_dist:
                    min_dist = self.dist(P[i], P[j])
        return min_dist

    def stripClosest(self, strip, size, d):
        min_dist = d
        strip.sort(key=lambda point: point.y)
        
        for i in range(size):
            for j in range(i + 1, size):
                if (strip[j].y - strip[i].y) >= min_dist:
                    break
                if self.dist(strip[i], strip[j]) < min_dist:
                    min_dist = self.dist(strip[i], strip[j])
        return min_dist

    def closestUtil(self, P, n):
        if n <= 3:
            return self.bruteForce(P, n)

        mid = n // 2
        midPoint = P[mid]

        dl = self.closestUtil(P[:mid], mid)
        dr = self.closestUtil(P[mid:], n - mid)

        d = min(dl, dr)

        strip = []
        for i in range(n):
            if abs(P[i].x - midPoint.x) < d:
                strip.append(P[i])

        return min(d, self.stripClosest(strip, len(strip), d))

    def closest(self, P, n):
        P.sort(key=lambda point: point.x)
        return self.closestUtil(P, n)
