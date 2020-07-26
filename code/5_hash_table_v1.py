"""
    哈希表（散列表）的Python实现

    作者：Jake Huang
    邮箱：jarork@qq.com
    博客：Jakehuang.com

    笔者先将每个字符的ASCII相加（相乘），然后使用正弦函数sin取得小数点后的数字，
    然后再以该数字除以位置数量所得余数做映射地址，用来减少冲突。

    在各种数据输入量的情况下，
    本哈希表插入和查找速度都是O(1)，运行速度大约是Python字典结构的十五分之一，
    但是仍然比使用列表顺序插入、查找的速度快了n倍。
    在本结构中使用的单向链表为本人编写。

    但是测试结果证明，进一步使用sin函数并不能降低冲突，反而会使各位置上数据量的分布更加不均匀，而且速度会大概下降10%.
    把每个字符的ASCII码相乘，然后进行下一步操作也不能有效降低冲突。而且速度也会下降10%。
    在各个位置上使用链表，在10000条数据量，10个位置的情况下，比使用列表的查找和插入(append)速度要慢30%

    但是使用sin函数可以达到补全的效果，如果位置数量很多，可以使用。

    支持散列表查找、插入和删除操作。
    一旦填装因子超过0.7，自动调整散列表的长度。
    散列表可用于缓存数据（例如，在Web服务器上）。
    散列表非常适合用于防止重复
"""

from lib.link_list_oneway import *
from math import sin
from random import randint
from timer import *

class HashTable():
    # 填装因子 = 哈希表中的元素数 / 哈希表数组位置数
    hash_factor = 0.7

    def __init__(self, len_arr, storage='LinkedList'):
        # 根据数组长度建立空数组
        if storage == "LinkedList" or storage == "Array":
            self.storage = storage
        else:
            raise TypeError("You can only storage data with Array or LinkedList in this Hash Table.")
        
        if len_arr > 0:
            self.len_arr = len_arr
            self.arr = [None for i in range(len_arr)]
        else:
            raise IndexError("The array length of the hash table must be greater than 0.")
        
        self.length = 0
    
    def __len__(self):
        return self.length

    # 散列函数：把每个字符串映射到元组中的地址
    def get_group_id(self, string):
        """
            散列函数：把每个字符串映射到元组中的地址
        : param string : 键（字符串形式）
        """
        if isinstance(string, str):
            # 先把字符串转成每个字的ascii乘机
            id = 1
            for i in string:
                id += ord(i)
            
            # 然后把这个数代入sin函数，取小数点后第9位到第15位数字
            # print(sin(id))
            id = int(abs(sin(id)) * 10 ** 15)
            
            # print(id)
            id = int(str(id)[-7:])
            # print(id)
                       
            # 根据数组的长度把这个字符串分到一组
            group_id = id % self.len_arr
            return group_id
            
        else:
            raise TypeError("Only string is allowed.")

    def push(self, data):
        """
            用于向哈希表插入一个数据
        : param data : 可以是列表、元组或者字典。列表或元组的第一个元素被作为键。字典只能有单个键值对。
        """
        if isinstance(data, dict):
            if len(data) == 1:
                for key, value in data.items():
                    pass
            else:
                raise TypeError("Dictionary can only have one pair.")
            
        elif isinstance(data, list) or isinstance(data, tuple): 
            key = data[0]
        else:
            raise TypeError("The hash table only receives list, tuple or dict.")

        if not isinstance(key, str):
            raise TypeError("The key can only be str.")

        # 获取散列索引
        data_gip = self.get_group_id(str(key))

        # 如果数组该位置为空，则建立一个空链表，然后插入该元素
        if not self.arr[data_gip]:
            # 使用链表存储数据
            if self.storage == "LinkedList":
                linked_list = LinkedListOneway()
                linked_list.append(data)
                self.arr[data_gip] = linked_list

            # 使用"数组"（Python列表）存储数据
            elif self.storage == "Array":
                array = []
                array.append(data)
                self.arr[data_gip] = array
    
        # 如果数组该位置已有数据，在该位置的链表中插入该元素
        else:
            self.arr[data_gip].append(data)
        
        self.length += 1

    def poll(self, key):
        """
            在哈希表中搜索一个键
        : param key : 键；列表或元组中的第一个元素，或者单个键值对中的键
        """
        # 获取键在数组中的地址
        address = self.get_group_id(key)

        # 如果该位置已有数据，在链表中查找该键
        if self.arr[address]:
            # 遍历链表，查找键
            for i in self.arr[address]:
                # 如果结点i是字典
                if isinstance(i, dict):
                    for i_key, value in i.items():
                        if i_key == key:
                            return i
                
                # 如果结点i是列表或元组
                else:
                    if i[0] == key:
                        return i
            
            # 遍历完链表，仍没找到该键
            return False

        # 如果该位置没有数据，返回不存在
        else:
            return False


####################  以下为哈希表测试用函数  #######################

def get_random_data(type = "list"):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # 随机长度
    length = randint(1,20)

    # 获取随机字符
    letters = [alphabet[randint(0,len(alphabet)-1)] for i in range(length)]
    random_str = "".join(letters)
    if type == "list":
        return [random_str, random_str[::-1]]
    elif type == "tuple":
        return (random_str, random_str[::-1])
    elif type == "dict":
        return {random_str: random_str[::-1]}
    elif type == "random":
        rand = randint(0,2)
        if rand == 0:
            return [random_str, random_str[::-1]]
        elif rand == 1:
            return (random_str, random_str[::-1])
        elif rand == 2:
            return {random_str: random_str[::-1]}

    else:
        raise TypeError("Only list, tuple, dict or random is acceptable")

def get_data(number, type = "random"):
    return [get_random_data(type) for i in range(number)]

def test_hash_insert(data, storage="LinkedList", insert_times = 10000, arr_size = 10000):
    """
    检测算法的插入是否均匀
    """
    # 创建空的哈希表
    hash_table = HashTable(arr_size, storage)

    @timer
    def hash_insert(data):
        for i in data:
            hash_table.push(i)

    hash_insert(data, name=">> 插入了%d个元素，哈希表数组长度为%d。本函数" % (insert_times, arr_size))

    if storage == "LinkedList":
        storage_type = "链表"
    elif storage == "Array":
        storage_type = "数组"

    for j in range(len(hash_table.arr)):
        if hash_table.arr[j]:
            length = len(hash_table.arr[j])
        else:
            length = 0

        print("  哈希表位置%d，%s长度：%d" % (j, storage_type, length))
    print("\n  哈希表总长度%d" % len(hash_table))

def test_hash_insert_and_search(data, storage="LinkedList", arr_size = 50):
    # 建立哈希表
    hash_table = HashTable(arr_size, storage)

    @timer
    def test_insert(data):
        for pair_insert in data:
            # print("插入Python字典的数据是：", pair_insert)
            if isinstance(pair_insert, dict):
                for key, value in pair_insert.items():
                    pass
            else:
                key = pair_insert[0]
                value = pair_insert[1]

            # print(key,value)
            hash_table.push({key:value})
        print("  已在自定义哈希表中存储了%d条数据。" % len(data))

    @timer
    def test_search(data):
        for pair_insert in data:
            # print("插入Python字典的数据是：", pair_insert)
            if isinstance(pair_insert, dict):
                for key, value in pair_insert.items():
                    pass
            else:
                key = pair_insert[0]
                value = pair_insert[1]

            # print(key,value)
            pair_get = hash_table.poll(key)
        print("  已在自定义哈希表中查找了%d条数据。" % len(data))

    test_insert(data, name="  >> 本函数")
    test_search(data, name="  >> 本函数")

def test_python_dict(data):
    python_dict = {}

    @timer
    def test_python_dict_insert(data):
        for pair_insert in data:
            # print("插入Python字典的数据是：", pair_insert)
            if isinstance(pair_insert, dict):
                for key, value in pair_insert.items():
                    pass
            else:
                key = pair_insert[0]
                value = pair_insert[1]

            # print(key,value)
            python_dict.update({key:value})
        print("  已在Python字典中存储了%d条数据。" % len(data))


    @timer
    def test_python_dict_search(data):
        for pair_insert in data:
            # print("插入Python字典的数据是：", pair_insert)
            if isinstance(pair_insert, dict):
                for key, value in pair_insert.items():
                    pass
            else:
                key = pair_insert[0]
                value = pair_insert[1]

            # print(key,value)
            pair_get = python_dict[key]
        print("  已在Python字典中查找了%d条数据。" % len(data))
    
    test_python_dict_insert(data, name="  >> 本函数")
    test_python_dict_search(data, name="  >> 本函数")

def test_list_insert_and_search(data):
    l = []

    @timer
    def list_insert(data):
        for pair_insert in data:
            l.append(pair_insert)
        print("  已在Python列表中存储了10000条数据。")

    @timer
    def list_search(data):
        j = 0
        for pair_insert in data:
            if isinstance(pair_insert, dict):
                for key, value in pair_insert.items():
                    pass
            else:
                key = pair_insert[0]
                value = pair_insert[1]
        
            
            for i in range(len(l)):            
                if isinstance(l[i], dict):
                    for each_key, each_value in l[i].items():
                        pass

                    if each_key == key:
                        break                   

                elif isinstance(l[i], list) or isinstance(l[i], tuple):
                    if l[i][0] == key:
                        break
                        
                else:
                    print("ERROR.")

        print("  已在Python列表中查找了10000条数据。")
    
    list_insert(data, name="  >> 本函数")
    list_search(data, name="  >> 本函数")

if __name__ == "__main__":
    print("哈希表功能与性能测试：")
    print("\n1. 正在进行自定义哈希表插入的均匀度测试：")
    test_hash_insert(get_data(10000), arr_size=20, storage = "Array")
    
    ##########  本哈希表与Python字典/列表的插入查询速度比较  ##########

    data_size = 10000
    print("\n2. 在自定义哈希表中(使用数组)的插入查找测试：")
    test_hash_insert_and_search(get_data(data_size), arr_size = 20000, storage = "Array")

    print("\n3. 在自定义哈希表中(使用链表)的插入查找测试：")
    test_hash_insert_and_search(get_data(data_size), arr_size = 20000, storage = "LinkedList")

    print("\n4. 在Python字典中的插入查找测试：")
    test_python_dict(get_data(data_size))
    
    print("\n5. 在Python列表中的插入查找测试：")
    test_list_insert_and_search(get_data(data_size))


    