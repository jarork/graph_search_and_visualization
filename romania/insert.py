"""
    二分插入算法
"""

arr = [1,3,5,9,13,14,17,19,20,24,26,27]

def insert(arr, value):
    max_i = len(arr) - 1
    min_i = 0

    mid_i = round((max_i + min_i) / 2)

    while max_i - min_i > 1:
        if arr[mid_i] > value:
            max_i = mid_i
            mid_i = round((max_i + min_i) / 2)
        else:
            min_i = mid_i
            mid_i = round((max_i + min_i) / 2)
    
    print(max_i, min_i, mid_i)
    arr.insert(max_i, value)
    return arr

print(insert(arr, 0))