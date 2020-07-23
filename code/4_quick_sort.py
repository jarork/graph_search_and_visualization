"""
    使用快速排序对数组中元素进行排序
    使用了DC以及递归思想
"""

def quicksort(array: list) -> list:
    """
        使用快速排序对数组中元素进行排序
    : param array : 传入的无序数组
    : return array : 传出的有序数组，从小到大
    """
    if len(array) < 2:
        return array  
    else:     
        pivot = array[0]
        less = [i for i in array[1:] if i <= pivot]
        greater = [i for i in array[1:] if i > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)

list = [10, 5, 2, 3]
print(quicksort(list))