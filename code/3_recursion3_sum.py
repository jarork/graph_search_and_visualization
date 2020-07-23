"""
    使用递归把一个列表中的所有数字相加
"""

def sum_all(arr: list) -> int:
    """
        把一个列表中所有数字相加
    """
    if arr:
        new_elem = list.pop(0)
        return new_elem + sum_all(list)
    else:
        return 0

list = [1,4,5,3,7,11]
print(sum_all(list))