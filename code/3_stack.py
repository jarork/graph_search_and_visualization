"""
    栈数据结构的Python实现
    Python栈数据结构
    作者：Jake Huang
    邮箱：jarork@qq.com
    博客：Jakehuang.com

    功能：
    1. 实例化LinkedList时，可使用列表或元组进行栈的赋值，并可限制栈最大长度
    2. 支持使用len可返回栈长度
    3. 支持使用push在栈顶添加新的元素
    4. 支持使用poll在栈顶取出元素
    5. 支持栈对象的迭代
    6. 支持print打印
    7. 支持使用clear语句，清空栈中全部元素
"""
from copy import copy

class Stack():
    # 1. 实例化LinkedList时，可使用列表或元组进行栈的赋值，并可限制栈最大长度
    def __init__(self, arr = None, maxsize = None):
        self.stack = []
        self.maxsize = maxsize
        self.length = 0

        if arr != None:
            if maxsize != None and len(arr) > maxsize:
                raise Exception("The capacity of the new stack is not big enough to hold the input elements.")
            
            if isinstance(arr, list) or isinstance(arr, tuple):
                self.stack = list(copy(arr))
                self.length = len(arr)
            else:
                raise TypeError("Data type not supported for initializing stack.")
        

    # 2. 支持使用len可返回栈长度
    def __len__(self):
        return self.length

    # 3. 支持使用push在栈顶压入新的元素
    def push(self, value):
        if self.maxsize == None or self.length < self.maxsize:
            self.stack.append(value)
            self.length += 1
        else:
            raise Exception("The stack is full.")

    # 4. 支持使用poll在栈顶取出元素
    def poll(self):
        if len(self):
            self.length -= 1
            return self.stack.pop()
        else:
            raise Exception("The stack is empty.")

    # 5. 支持栈对象的迭代
    def __iter__(self):
        while len(self):
            self.length -= 1
            yield self.stack.pop()    

    # 6. 支持print打印
    def __repr__(self):
        stack_print = "stack("
        if not len(self):
            stack_print += ")"

        for i in range(len(self)-1,-1,-1):
            stack_print += str(self.stack[i])

            if i != 0:
                stack_print += ", "
            else:
                stack_print += ")"

        return stack_print

    # 7. 支持使用clear语句，清空栈中全部元素
    def clear(self):
        self.stack = []
        self.length = 0

if __name__ == "__main__":
    # 1. 测试实例化LinkedList时，可使用列表或元组进行栈的赋值，并可限制栈最大长度
    # 2. 测试支持使用len可返回栈长度
    def test_init():
        stack = Stack()
        assert len(stack) == 0
        stack = Stack([1,2,3,4,5])
        assert len(stack) == 5
        stack = Stack((1,2,3,4,5))
        assert len(stack) == 5

    # 3. 测试支持使用push在栈顶添加新的元素
    # 4. 测试支持使用poll在栈顶取出元素
    def test_push():
        stack = Stack()
        stack.push(15)
        assert stack.poll() == 15
        assert len(stack) == 0
        stack.push('h')
        stack.push("i")
        assert len(stack) == 2
        assert stack.poll() == "i"
        assert stack.poll() == "h"
        assert len(stack) == 0
    
    # 5. 支持栈对象的迭代
    # 6. 支持print打印
    def test_iter():
        list = ('a',2,9.9,'word')
        stack = Stack(list)
        print(stack)
        assertion = list[::-1]
        for i,j in zip(stack,assertion):
            assert i == j

    # 7. 支持使用clear语句，清空栈中全部元素
    def test_clear():
        stack = Stack([2,5,3,4,'hi'])
        assert len(stack) == 5
        stack.clear()
        assert len(stack) == 0

    test_init()
    test_push()
    test_iter()
    test_clear()
    
    print("end")