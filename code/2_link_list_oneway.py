"""
    Python链表数据结构
    作者：Jake Huang
    邮箱：jarork@qq.com
    博客：Jakehuang.com

    链表数据结构支持的方法有：
    1. 实例化LinkedList时，可使用列表或元组进行链表的赋值，并可限制链表最大长度 O(n)
    2. 支持使用len可返回链表长度 O(1)
    3. 支持使用append可在链表末尾添加新的结点 O(1)
    4. 支持使用索引获取或修改第i个结点的值 O(n)
    5. 支持使用切片获取一个子链表
    6. 支持使用pop，remove和del删除链表中的结点 定位O(n) 删除O(1)
    7. 支持链表对象的迭代   O(n)
    8. 支持print打印    O(n)
    9. 支持in语句，判断链表中是否包含某一元素   O(n)
    10. 支持使用insert，在链表某一位置插入结点   定位O(n) 插入O(1)
    11. 支持使用clear语句，清空链表中全部结点   O(n)
    12. 支持使用 + 运算符拼接链表和链表     O(1)
    13. 支持使用reverse反转链表中的所有结点 O(n)
"""

import copy
from time import sleep


class Node():
    # 限制添加其他属性
    __slots__ = ('value', 'next')

    def __init__(self, value=None, next=None):
        # 数据域和指针域
        self.value, self.next = value, next

    def __repr__(self):
        return "<Node: value={}, next={}>".format(self.value, self.next)

    def next_node(self):
        return self.next

    def __iter__(self):
        while self.next:
            yield self.next
            self.next = self.next.next

class LinkedListOneway():
    def __init__(self, arr=None, maxsize=None):
        """
            链表初始化
            可以限制链表的长度，也可以用元组或列表给链表初始化
        : param maxsize : 链表的最大长度
        : param arr : 用以创建链表的数据，可以使列表或者元组
        """

        self.maxsize = maxsize
        self.tailnode = None

        # 创建空链表
        self.root = Node()
        self.length = 0

        # 依据现有列表和元组建立链表
        if arr:
            if isinstance(arr, list) or isinstance(arr, tuple):
                if self.maxsize == None or len(arr) < self.maxsize:
                    # 把列表或元组中的数据全部复制到新链表中
                    prev_node = self.root

                    for i in arr:
                        current_node = Node(value=i)
                        prev_node.next = current_node
                        prev_node = current_node
                    self.length += len(arr)
                    self.tailnode = current_node

                else:
                    raise Exception(
                        "The capacity of the new Linked List is not big enough to hold the input elements.")

            else:
                raise TypeError(
                    "The Linked List Type can only be initialized with a list or tuple, not %s" % str(type(arr)))

    def __len__(self) -> int:
        """
            支持使用 len 方法取得链表的长度
        """
        return self.length

    def __getitem__(self, index):
        """
            获取链表中索引为index的元素的值
        : param index : 链表的索引，可以是一个索引值，也可以是切片。不支持步长
        """

        if isinstance(index, slice):
            start = index.start
            stop = index.stop
            step = index.step

            if step != None:
                raise Exception(
                    "Slicing with a step is not supported for linked list.")

            if start == None and stop == None:
                return self

            if start == None:
                start = 0

            if stop == None:
                stop = len(self)

            if start > len(self) or stop > len(self):
                raise IndexError("Linked list index out of range.")

            if len(self) == 0:
                return None

            if (not isinstance(start, int)) or (not isinstance(stop, int)):
                raise IndexError("The slicing indice should all be integers.")

            if stop <= start:
                raise IndexError(
                    "the slice stop should always be larger than the start.")

            # 创建用于存放切片的空链表
            new_linked_list = LinkedListOneway()

            # 定位到起始索引的位置
            current_node = self.root.next
            for i in range(start):
                current_node = current_node.next

            # 开始往新链表中复制
            copy_times = stop - start
            for i in range(copy_times):
                node = copy.deepcopy(current_node)
                new_linked_list.append(node.value)
                current_node = current_node.next
            return new_linked_list

        elif isinstance(index, int):
            if index < self.length:
                current_node = self.root.next
                for i in range(index):
                    current_node = current_node.next
                return current_node.value

            else:
                raise IndexError("Linked list index out of range.")

        else:
            raise IndexError("Linked list index should be int.")

    def __setitem__(self, index: int, value):
        """
            改变链表中索引为index的元素的值为value
        : param index : 链表的索引
        : param value : 修改后元素的值
        """
        if index < self.length:
            # 定位到目标元素
            current_node = self.root.next
            for i in range(index):
                current_node = current_node.next
            current_node.value = value
        else:
            raise IndexError("Linked list index out of range.")

    def __delitem__(self, index: int) -> None:
        """
            使用 del 语句删除链表中的元素
        : param index : 删除结点的索引值
        """
        self.pop(index)

    def __iter__(self):
        current_node = self.root.next
        for i in range(len(self)):
            yield current_node.value
            current_node = current_node.next

    def __repr__(self):
        """
            提供打印链表中的全部元素的方法
        """
        linked_list_print = "LinkedList("
        # 如果是空链表
        if len(self) == 0:
            return linked_list_print + ")"

        current_node = self.root.next
        # 如果链表只有一个结点
        if len(self) == 1:
            return linked_list_print + str(current_node.value) + ")"
        linked_list_print += str(current_node.value) + ", "

        for i in range(len(self)-1):
            current_node = current_node.next
            if isinstance(current_node.value, int) or isinstance(current_node.value, float):
                linked_list_print += str(current_node.value)
            else:
                linked_list_print += '%s' % str(current_node.value)

            if i < len(self) - 2:
                linked_list_print += ", "
            else:
                linked_list_print += ")"

        return linked_list_print

    def __contains__(self, value) -> bool:
        """
            支持 in 语句，判断元素是否存在于链表中
        : param value : 要查找的元素
        """
        # 遍历链表，查找value
        current_node = self.root.next

        if current_node.value == value:
            self.root.next = current_node.next
            return True

        for i in range(len(self)-1):
            current_node = current_node.next

            # 如果定位到该元素，删除，跳出
            if current_node.value == value:
                return True

        # 没有找到该元素
        return False

    def __add__(self, linked_list):
        """
            链表拼接，原链表 + 新链表
        : param linked_list : 新链表(在+右侧)
        : return concat_linked_list : 合成之后的链表
        """
        # 深拷贝链表A和链表B
        linked_list_a = copy.deepcopy(self)
        linked_list_b = copy.deepcopy(linked_list)

        # 创建一个新链表存储连接之后的链表
        linked_list_a.tailnode.next = linked_list_b.root.next
        linked_list_a.tailnode = linked_list_b.tailnode
        linked_list_a.length += linked_list_b.length
        return linked_list_a

    def __radd__(self, linked_list):
        """
            链表拼接，新链表 + 原链表
        : param linked_list : 新链表(在+左侧)
        : return concat_linked_list : 合成之后的链表
        """
        # 深拷贝链表A和链表B
        linked_list_a = copy.deepcopy(linked_list)
        linked_list_b = copy.deepcopy(self)

        # 创建一个新链表存储连接之后的链表
        linked_list_a.tailnode.next = linked_list_b.root.next
        linked_list_a.tailnode = linked_list_b.tailnode
        linked_list_a.length += linked_list_b.length
        return linked_list_a

    def node(self, index):
        """
            获取链表某索引位置的结点
        """
        if isinstance(index, int):
            if index == 0:
                return self.root.next

            if index >= self.length:
                raise IndexError("Index out of range.")

            current_node = self.root.next
            for i in range(index):
                current_node = current_node.next
            return current_node

        else:
            raise TypeError("The input index should be int.")

    def append(self, value):
        """
            在链表结尾插入值为value的新结点
        : param value : 链表中新结点的值
        """
        if self.maxsize is not None and len(self) >= self.maxsize:
            raise Exception('The LinkedList is Full')
        node = Node(value)    # 构造节点
        tailnode = self.tailnode
        if tailnode is None:    # 还没有 append 过，length = 0， 追加到 root 后
            self.root.next = node
            self.tailnode = node
            self.length += 1
        else:     # 否则追加到最后一个节点的后边，并更新最后一个节点是 append 的节点
            tailnode_next = tailnode.next   # 保存原来尾结点的值
            tailnode.next = node            # 把新结点连接到原来尾结点的后面
            self.tailnode = node            # 更新尾结点
            self.tailnode.next = tailnode_next  # 把原来尾结点的连接对象作为新尾结点的连接对象
            self.length += 1

    def pop(self, index: int):
        """
            删除并弹出链表中索引为index的结点
        : param index : 链表的索引
        """
        if index < self.length:
            # 定位到目标元素
            current_node = self.root.next
            for i in range(index):
                prev_node = current_node
                current_node = current_node.next

            next_node = current_node.next

            if index == 0:
                self.root.next = next_node
            else:
                # 把目标前面的结点连接到目标后面的结点
                prev_node.next = next_node

            # 删除当前结点
            value = current_node.value
            del current_node
            self.length -= 1

            # 弹出删除元素的值
            return value

        else:
            raise IndexError("Linked list index out of range.")

    def remove(self, value):
        """
            删除链表中值为value的第一个元素
        : param value : 要删除的元素的值
        """
        # 遍历链表，查找value
        current_node = self.root.next

        if current_node.value == value:
            self.root.next = current_node.next
            del current_node
            self.length -= 1
            return

        for i in range(len(self)):
            prev_node = current_node
            current_node = current_node.next

            # 如果定位到该元素，删除，跳出
            if current_node.value == value:
                break
        next_node = current_node.next

        prev_node.next = next_node
        del current_node
        self.length -= 1

    def insert(self, index: int, value):
        """
            在链表索引index位置插入值为value的结点
        : param index : 链表的索引位置
        : param value : 新结点的值
        """
        if self.maxsize is not None and len(self) >= self.maxsize:
            raise Exception("The LinkedList is Full")

        if index == 0:
            node = Node(value=value, next=self.root.next)
            self.root.next = node
            self.length += 1
            return

        if index < self.length:
            # 定位到目标元素
            current_node = self.root.next
            for i in range(index):
                prev_node = current_node
                current_node = current_node.next

            # 新建结点
            node = Node(value=value, next=current_node)

            prev_node.next = node
            self.length += 1

        else:
            raise IndexError("Linked list index out of range.")

    def clear(self):
        """
            清空链表中的所有结点
        """
        current_node = self.root.next
        for i in range(len(self)):
            prev_node = current_node
            current_node = current_node.next
            del prev_node
        del current_node
        del self.tailnode
        self.length = 0

    def reverse(self):
        """
            对链表进行反转
        """
        current_node = self.root.next
        self.tailnode = current_node
        prev_node = None

        while current_node:
            next_node = current_node.next
            current_node.next = prev_node

            if next_node is None:
                self.root.next = current_node

            prev_node = current_node
            current_node = next_node
        return self


if __name__ == "__main__":
    a = LinkedListOneway(list(range(10)))
    print(a[3])
    print(a[:])
    print(len(a))
    b = a.node(4)
    print(b)
    print(b.next_node())

