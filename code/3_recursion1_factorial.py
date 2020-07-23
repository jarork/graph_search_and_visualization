"""
    递归 = 基线条件 + 递归条件
"""


def factorial(x):
    # 基线条件
    if x == 1:
        return 1
    # 递归条件
    else:
        return x * factorial(x-1)

print(factorial(10))
