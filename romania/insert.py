"""
    二分插入算法
"""

def insert(arr, value, mode="asc"):
    if mode == "desc":
        if len(arr) == 0:
            arr.append(value)

        elif len(arr) == 1:
            if value < arr[0]:
                arr.append(value)
            else:
                arr.insert(0, value)

        elif len(arr) > 1:
            max_i = len(arr) - 1
            min_i = 0

            mid_i = round((max_i + min_i) / 2)

            while max_i - min_i > 1:
                if arr[mid_i] > value:
                    min_i = mid_i
                    mid_i = round((max_i + min_i) / 2)
                elif arr[mid_i] < value:
                    max_i = mid_i
                    mid_i = round((max_i + min_i) / 2)
                elif arr[mid_i] == value:
                    index = mid_i
                    break
            else:
                index = max_i

            if value > arr[0]:
                arr.insert(min_i, value)
            elif value < arr[-1]:
                arr.append(value)
            else:
                arr.insert(index, value)
        return arr

    elif mode == "asc":
        if len(arr) == 0:
            arr.append(value)

        elif len(arr) == 1:
            if value > arr[0]:
                arr.append(value)
            else:
                arr.insert(0, value)

        elif len(arr) > 1:
            max_i = len(arr) - 1
            min_i = 0

            mid_i = round((max_i + min_i) / 2)

            while max_i - min_i > 1:
                if arr[mid_i] > value:
                    max_i = mid_i
                    mid_i = round((max_i + min_i) / 2)
                elif arr[mid_i] < value:
                    min_i = mid_i
                    mid_i = round((max_i + min_i) / 2)
                elif arr[mid_i] == value:
                    index = mid_i
                    break
            else:
                index = max_i

            if value > arr[-1]:
                arr.append(value)
            elif value < arr[0]:
                arr.insert(0, value)
            else:
                arr.insert(index, value)
        return arr

if __name__ == "__main__":
    from random import randint

    arr_asc = []
    arr_desc = []
    for i in range(30):
        arr_asc = insert(arr_asc, randint(1,100), mode="asc")
        arr_desc = insert(arr_desc, randint(1,100), mode="desc")
        
    print(arr_asc)
    print(arr_desc)
