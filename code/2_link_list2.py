class Node():
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return "<Node: value = {}, next = {}>".format(self.value, self.next)

class LinkedList():
    def __init__(self, maxsize = None):
        self.__maxsize = maxsize
        self.__root = Node()
        self.__tailnode = None
        self.__length = 0

    def __len__(self):
        return self.__length

    def __getitem__(self, index: int):
        """
            获取链表中索引为index的元素的值
        : param index : 链表的索引
        """
        if index <= self.__length:
            current_node = self.__root.next 
            for i in range(index):
                current_node = current_node.next
            return current_node.value
        else:
            return None
    
    def __setitem__(self, index: int, value):
        """
            改变链表中索引为index的元素的值为value
        : param index : 链表的索引
        : param value : 修改后元素的值
        """
        if index < self.__length:
            # 定位到目标元素
            current_node = self.__root.next
            for i in range(index):
                current_node = current_node.next
            current_node.value = value
        else:
            raise IndexError("Linked list index out of range.")

    def __iter__(self):
        current_node = self.__root.next
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

        current_node = self.__root.next
        # 如果链表只有一个结点
        if len(self) == 1:
            return linked_list_print + str(current_node.value) + ")"
        linked_list_print += str(current_node.value) + ", "

        for i in range(len(self)-1):
            current_node = current_node.next
            if isinstance(current_node.value, int) or isinstance(current_node.value, float):
                linked_list_print += str(current_node.value)
            else:
                linked_list_print += '"%s"' % str(current_node.value)                    
            
            if i < len(self) - 2:
                linked_list_print += ", "
            else:
                linked_list_print += ")"
        
        return linked_list_print  

    def append(self, value):    # O(1)
        """
            在链表结尾插入值为value的新结点
        : param value : 链表中新结点的值
        """
        if self.__maxsize is not None and len(self) >= self.__maxsize:
            raise Exception('LinkedList is Full')
        node = Node(value)    # 构造节点
        tailnode = self.__tailnode
        if tailnode is None:    # 还没有 append 过，length = 0， 追加到 root 后
            self.__root.next = node
        else:     # 否则追加到最后一个节点的后边，并更新最后一个节点是 append 的节点
            tailnode.next = node
        self.__tailnode = node
        self.__length += 1

    def pop(self, index: int):
        """
            删除并弹出链表中索引为index的结点
        : param index : 链表的索引
        """
        if index < self.__length:
            # 定位到目标元素
            current_node = self.__root.next
            for i in range(index):
                prev_node = current_node
                current_node = current_node.next
            
            next_node = current_node.next

            if index == 0:
                self.__root.next = next_node
            else:
                # 把目标前面的结点连接到目标后面的结点
                prev_node.next = next_node
            
            # 删除当前结点
            value = current_node.value
            del current_node
            self.__length -= 1

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
        current_node = self.__root.next

        if current_node.value == value:
            self.__root.next = current_node.next
            del current_node
            self.__length -= 1
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
        self.__length -= 1
      
    def insert(self, index: int, value):
        """
            在链表索引index位置插入值为value的结点
        : param index : 链表的索引位置
        : param value : 新结点的值
        """
        if self.__maxsize is not None and len(self) >= self.__maxsize:
            raise Exception("The LinkedList is Full")
        if index < self.__length:
            # 定位到目标元素
            current_node = self.__root.next
            for i in range(index):
                prev_node = current_node
                current_node = current_node.next
            
            # 新建结点
            node = Node(value=value, next=current_node)
            prev_node.next = node
            self.__length += 1

        else:
            raise IndexError("Linked list index out of range.")

    def clear(self):
        """
            清空链表中的所有结点
        """
        current_node = self.__root.next
        for i in range(len(self)):
            prev_node = current_node
            current_node = current_node.next
            del prev_node
        del current_node
        del self.__tailnode
        self.__length = 0

a = LinkedList(15)
# for i in range(10):
#     a.append(i)


# a.remove(0)


print(a)
