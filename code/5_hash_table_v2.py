"""
    哈希表（散列表）的Python实现

    作者：Jake Huang
    邮箱：jarork@qq.com
    博客：Jakehuang.com

    v2.0版本调整：
    1. 取消了对哈希表各个位置上列表的存储支持，一律使用链表进行存储
    2. 将存储结构改为双链，不再在各个位置上存储子链表，而是把子链表串联成长链，在哈希表每个位置上保存长链上的各个地址。
    3. 增加了哈希表元素遍历和键值对遍历的功能（__iter__() 和 items()方法）

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

    def __init__(self, len_arr):
        # 根据数组长度建立空数组
        if len_arr > 1:
            self.len_arr = len_arr
            self.arr = [None for i in range(len_arr)]
            self.arr[0] = LinkedListOneway()
            self.root = self.arr[0]
        else:
            raise IndexError(
                "The array length of the hash table must be greater than 1.")

        self.length = 0

    def __len__(self):
        return self.length

    def __iter__(self):
        for i in self.root:
            yield i

    def __repr__(self):
        """
            提供哈希表的打印方式
        """
        string = "HashTable{"
        for key, value in self.items():
            if isinstance(key, str):
                string += "'%s': " % key
            else:
                string += "{}: ".format(key)

            if isinstance(value, str):
                string += "'%s', " % value
            else:
                string += "{}, ".format(value)

        string = string[:-2]
        string += "}"

        return string

    def items(self):
        """
            遍历哈希表中所有的键和值
        : yield key, value : 数据的键和值
        """
        for i in self.root:
            if isinstance(i, dict):
                for key, value in i.items():
                    yield (key, value)
            elif isinstance(i, list) or isinstance(i, tuple):
                key = i[0]

                value = i[1:]
                if len(value) == 1:
                    value = value[0]
                yield (key, value)

    def print_hash_table(self):
        """
            打印哈希表所有的位置
        """
        for i in range(len(self.arr)):
            if i == 0:
                print("位置[{}] （链表头） : \n{}".format(i, self.arr[i]))

            else:
                print("位置[{}] : {}".format(i, self.arr[i]))

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
            id = int(abs(sin(id)) * 10 ** 20)

            # print(id)
            # id = int(str(id)[-10:])

            # 根据数组的长度把这个字符串分到一组，数组在索引0位置留空
            group_id = id % (self.len_arr-1) + 1
            # print(group_id)
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
            raise TypeError(
                "The hash table only receives list, tuple or dict.")

        if not isinstance(key, str):
            raise TypeError("The key can only be str.")

        # 获取散列索引
        data_gip = self.get_group_id(str(key))

        # 如果数组该位置为空，则建立一个空链表，然后插入该元素
        if not self.arr[data_gip]:
            # print("\n\n插入前的哈希表")
            # self.print_hash_table()

            cur_list = LinkedListOneway()
            cur_list.append(data)

            self.arr[data_gip] = cur_list

            # print("插入后的哈希表")
            # self.print_hash_table()

            # 把当前链表加入到总链中
            for i in range(data_gip-1, -1, -1):     # 查找左面最近的链表
                # 当在左边发现了链表，把它的尾结点连接到这个新链表的头结点后面
                prev_list = self.arr[i]
                if prev_list != None:
                    # print("左侧链表的索引是", i)

                    # 如果左侧链表是总链表
                    if prev_list == self.root:
                        prev_list.root.next = cur_list.root.next

                    # 如果左侧链表非空，直接连接尾结点
                    else:
                        prev_list.tailnode.next = cur_list.root.next

                    self.root.length += 1
                    break

            for j in range(data_gip+1, self.len_arr):
                # 当在右侧发现了链表，把当前链表的尾结点连接到右侧链表头结点之后
                next_list = self.arr[j]
                if next_list != None:
                    # print("右侧链表的索引是", j)
                    cur_list.tailnode.next = next_list.root.next
                    break

                if j == self.len_arr - 1:
                    # print("没有找到右侧的链表")
                    break

            # print("连接后的哈希表：")
            # self.print_hash_table()

        # 如果数组该位置已有数据，在该位置的链表中插入该元素
        else:
            self.arr[data_gip].append(data)
            self.root.length += 1
            # print("本位置已有链表")
            # self.print_hash_table()

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


if __name__ == "__main__":

    ####################  以下为哈希表测试用函数  #######################

    def get_random_data(type="list"):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # 随机长度
        length = randint(1, 20)

        # 获取随机字符
        letters = [alphabet[randint(0, len(alphabet)-1)]
                   for i in range(length)]
        random_str = "".join(letters)
        if type == "list":
            return [random_str, random_str[::-1]]
        elif type == "tuple":
            return (random_str, random_str[::-1])
        elif type == "dict":
            return {random_str: random_str[::-1]}
        elif type == "random":
            rand = randint(0, 2)
            if rand == 0:
                return [random_str, random_str[::-1]]
            elif rand == 1:
                return (random_str, random_str[::-1])
            elif rand == 2:
                return {random_str: random_str[::-1]}

        else:
            raise TypeError("Only list, tuple, dict or random is acceptable")

    def get_data(number, type="random"):
        return [get_random_data(type) for i in range(number)]

    def test_hash_insert(data, arr_size=10000):
        """
        检测算法的插入是否均匀
        """
        # 创建空的哈希表
        hash_table = HashTable(arr_size)

        @timer
        def hash_insert(data):
            for i in data:
                hash_table.push(i)

        hash_insert(data, name=">> 插入了%d个元素，哈希表有%d个位置。本函数" %
                    (len(data), arr_size))

        for j in range(len(hash_table.arr)):
            if hash_table.arr[j]:
                length = len(hash_table.arr[j])
            else:
                length = 0

            print("  哈希表位置%d，链表长度：%d" % (j, length))
        print("\n  哈希表总长度%d" % len(hash_table))

    def test_hash_efficiency(data, arr_size=50):
        # 建立哈希表
        hash_table = HashTable(arr_size)

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
                hash_table.push({key: value})
            print("  存储测试：已在自定义哈希表中存储了%d条数据。" % len(data))

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
            print("  查找测试：已在自定义哈希表中查找了%d条数据。" % len(data))

        @timer
        def test_iter():
            count = 0
            for key, value in hash_table.items():
                count += 1

            print("  遍历测试：已在自定义哈希表中遍历了%d条数据。" % count)

        test_insert(data, name="  >> 本函数")
        test_search(data, name="  >> 本函数")
        test_iter(name="  >> 本函数")

    def test_python_dict_efficiency(data):
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
                python_dict.update({key: value})
            print("  存储测试：已在Python字典中存储了%d条数据。" % len(data))

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
            print("  查找测试：已在Python字典中查找了%d条数据。" % len(data))

        @timer
        def test_python_dict_iter():
            count = 0
            for key, value in python_dict.items():
                count += 1
            print("  遍历测试：已在Python字典中遍历了%d条数据。" % count)

        test_python_dict_insert(data, name="  >> 本函数")
        test_python_dict_search(data, name="  >> 本函数")
        test_python_dict_iter(name="  >> 本函数")

    def test_python_list_efficiency(data):
        l = []

        @timer
        def list_insert(data):
            for pair_insert in data:
                l.append(pair_insert)
            print("  存储测试：已在Python列表中存储了%d条数据。" % len(data))

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

            print("  查找测试：已在Python列表中查找了%d条数据。" % len(data))

        @timer
        def list_iter():
            count = 0
            for i in l:
                count += 1
            print("  遍历测试：已在Python列表中遍历了%d条数据。" % count)

        list_insert(data, name="  >> 本函数")
        list_search(data, name="  >> 本函数")
        list_iter(name="  >> 本函数")

    def test_hash_iter():
        """
            测试哈希表的遍历
        """
        hash = HashTable(10)
        hash.push(['a1', 1])
        hash.push(['a2', '2'])
        hash.push(['a3', '3'])
        hash.push(['a4', '4'])
        hash.push(['a5', '5'])
        hash.push(['a6', '6'])
        hash.push(['a7', '7'])

        print(hash)

        print("\n>> 哈希表中各个位置的存储情况：")
        hash.print_hash_table()

        print("\n>> 哈希表的遍历情况")
        count = 0
        for i in hash:
            print(i)
            count += 1

        assert count == len(hash)

    def test_hash_items():
        """
            测试哈希表的键值对遍历
        """
        hash = HashTable(10)
        hash.push(['a1', '1'])
        hash.push(['a2', '2'])
        hash.push(['a3', '3'])
        hash.push(['a4', '4'])
        hash.push(['a5', '5'])
        hash.push(['a6', '6'])
        hash.push(['a7', '7'])

        print("\n>> 哈希表中各个位置的存储情况：")
        hash.print_hash_table()

        print("\n>> 哈希表键值对的遍历情况")
        count = 0
        for key, value in hash.items():
            print("键：{}\t值:{}".format(key, value))
            count += 1

        assert count == len(hash)

    def test_hash_push_and_poll():
        """
            测试哈希表的插入和取出是否准确
        """
        hash = HashTable(10)
        hash.push(['a1', '1'])
        hash.push(['a2', '2'])
        hash.push(['a3', '3'])
        hash.push(['a4', '4'])
        hash.push(['a5', '5'])
        hash.push(['a6', '6'])
        hash.push(['a7', '7'])

        assert hash.poll('a1') == ['a1', '1']
        assert hash.poll('a3') == ['a3', '3']
        assert hash.poll('a7') == ['a7', '7']
        print(">> 测试成功。")

    def main():
        print("\n########### 哈希表功能测试 ###########")
        print("\n1. 正在进行自定义哈希表插入的均匀度测试：")
        test_hash_insert(get_data(10000), arr_size=20)

        print("\n2. 测试哈希表的遍历")
        test_hash_iter()

        print("\n3. 测试哈希表键值对的遍历")
        test_hash_items()

        print("\n4. 测试哈希表的插入和取出是否准确")
        test_hash_push_and_poll()

        ##########  本哈希表与Python字典/列表的插入查询速度比较  ##########

        print("\n########### 哈希表性能测试 ###########")

        data_size = 1000

        print("\n5. 在自定义哈希表中(使用链表)的插入查找测试：")
        test_hash_efficiency(get_data(data_size), arr_size=int(data_size*1.5))

        print("\n6. 在Python字典中的插入查找测试：")
        test_python_dict_efficiency(get_data(data_size))

        print("\n7. 在Python列表中的插入查找测试：")
        test_python_list_efficiency(get_data(data_size))

    ####################  哈希表测试开始  #######################

    main()
    # print("\n1. 正在进行自定义哈希表插入的均匀度测试：")
    # test_hash_insert(get_data(100000), arr_size=100000)