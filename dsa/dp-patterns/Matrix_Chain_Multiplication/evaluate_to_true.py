# This is functionally the same as boolean_parenthesization.py.
# In many contexts "Evaluate to True" IS Boolean Parenthesization.
# Creating a wrapper or explanation file.

from boolean_parenthesization import count_eval

if __name__ == "__main__":
    expression = "T^F&T"
    print(f"Expression: {expression}")
    print(f"Ways to True: {count_eval(expression)}")
