"""
    选择排序算法：按从小到大顺序排序
"""


def findSmallest(arr: list) -> int:
    """
        寻找数组中最小元素
    : param arr : 数组
    : return smallest_index : 数组中最小元素的索引
    """
    smallest = arr[0]
    smallest_index = 0
    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_index = i
    return smallest_index

# 现在可以使用这个findSmallest()函数来编写选择排序算法了。


def selectionSort(arr: list) -> list:
    """
        选择排序：依次在数组中查找最小元素
    : param arr : 需要进行选择排序的数组
    : return newArr : 从小到大排序后的新列表
    """
    newArr = []
    for i in range(len(arr)):
        smallest = findSmallest(arr)
        newArr.append(arr.pop(smallest))
    return newArr


array = [14, 5, 1, 8, 23, 5, 12, 7, 4, 11]
print(selectionSort(array))

# 打印结果
'''
    [1, 4, 5, 5, 7, 8, 11, 12, 14, 23]
'''
