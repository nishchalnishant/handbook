class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

class Solution:
    def fractionalKnapsack(self, w: int, arr: list) -> float:
        """
        Problem: Fractional Knapsack
        Difficulty: Medium
        Time Complexity: O(n log n)
        Space Complexity: O(1)
        """
        # Sort by value/weight ratio descending
        arr.sort(key=lambda x: x.value / x.weight, reverse=True)
        
        curWeight = 0
        finalValue = 0.0
        
        for item in arr:
            if curWeight + item.weight <= w:
                curWeight += item.weight
                finalValue += item.value
            else:
                remain = w - curWeight
                finalValue += item.value * (remain / item.weight)
                break
        return finalValue
