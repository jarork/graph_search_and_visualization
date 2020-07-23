"""
    二分查找算法
"""


def binary_search(list: list, item: int) -> int or None:
    """
        根据某个值查找数组中元素的索引
    : param list : 数组
    : param item : 想要查找的值
    : return int or None : 如果数组中有该元素，返回它的索引；若没有则返回None
    """
    low = 0
    high = len(list)-1
    while low <= high:
        mid = round((low + high) / 2)
        guess = list[mid]
        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


my_list = [1, 3, 5, 7, 9, 11, 12, 15, 19, 30, 44, 46, 51, 55]
print(binary_search(my_list, 15))
print(binary_search(my_list, -1))

# 打印结果
'''
7
None
'''
