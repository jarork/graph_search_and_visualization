"""
    队列Queue的Python实现
    Python队列数据结构
    作者：Jake Huang
    邮箱：jarork@qq.com
    博客：Jakehuang.com

    功能：
    1. 实例化LinkedList时，可使用列表或元组进行队列的赋值，并可限制队列最大长度
    2. 支持使用len可返回队列长度
    3. 支持使用push在队列顶添加新的元素
    4. 支持使用poll在队列顶取出元素
    5. 支持队列对象的迭代
    6. 支持print打印
    7. 支持使用clear语句，清空队列中全部元素
"""
from copy import copy

class Queue():
    # 1. 实例化队列时，可使用列表或元组进行队列的赋值，并可限制队列最大长度
    def __init__(self, arr = None, maxsize = None):
        self.queue = []
        self.maxsize = maxsize
        self.length = 0

        if arr != None:
            if maxsize != None and len(arr) > maxsize:
                raise Exception("The capacity of the new queue is not big enough to hold the input elements.")
            
            if isinstance(arr, list) or isinstance(arr, tuple):
                self.queue = list(copy(arr))
                self.length = len(arr)
            else:
                raise TypeError("Data type not supported for initializing queue.")
        
    # 2. 支持使用len可返回队列长度
    def __len__(self) -> int:
        return self.length

    # 3. 支持使用push在队列尾部压入新的元素
    def push(self, value) -> None:
        """
            在队尾添加新的元素
        : param value : 新元素的值
        """
        if self.maxsize == None or self.length < self.maxsize:
            self.queue.append(value)
            self.length += 1
        else:
            raise Exception("The queue is full.")

    # 4. 支持使用poll在队列头部取出元素
    def poll(self):
        """
            在队列头部取出元素
        : return value : 在队列头部取出的元素
        """
        if len(self):
            self.length -= 1
            return self.queue.pop(0)
        else:
            raise Exception("The queue is empty.")

    # 5. 支持队列对象的迭代
    def __iter__(self):
        """
            允许对队列数据结构的迭代，迭代之后队列中的元素会清空
        : yield value : 队列中从头到尾的各个元素
        """
        while len(self):
            self.length -= 1
            yield self.queue.pop(0)    

    # 6. 支持print打印
    def __repr__(self):
        """
            使队列数据结构支持打印查询
        : return str : 打印出来的内容
        """
        queue_print = "queue("
        if not len(self):
            queue_print += ")"

        for i in range(len(self)-1,-1,-1):
            queue_print += str(self.queue[i])

            if i != 0:
                queue_print += ", "
            else:
                queue_print += ")"

        return queue_print

    # 7. 支持使用clear语句，清空队列中全部元素
    def clear(self):
        """
            清空队列
        """
        self.queue = []
        self.length = 0

if __name__ == "__main__":
    # 1. 测试实例化LinkedList时，可使用列表或元组进行队列的赋值，并可限制队列最大长度
    # 2. 测试支持使用len可返回队列长度
    def test_init():
        queue = Queue()
        assert len(queue) == 0
        queue = Queue([1,2,3,4,5])
        assert len(queue) == 5
        queue = Queue((1,2,3,4,5))
        assert len(queue) == 5

    # 3. 测试支持使用push在队列顶添加新的元素
    # 4. 测试支持使用poll在队列顶取出元素
    def test_push():
        queue = Queue()
        queue.push(15)
        assert queue.poll() == 15
        assert len(queue) == 0
        queue.push('h')
        queue.push("i")
        assert len(queue) == 2
        assert queue.poll() == "h"
        assert queue.poll() == "i"
        assert len(queue) == 0
    
    # 5. 支持队列对象的迭代
    # 6. 支持print打印
    def test_iter():
        assertion = ('a',2,9.9,'word')
        queue = Queue(assertion)
        
        print(queue)
        for i,j in zip(queue,assertion):
            assert i == j
        

    # 7. 支持使用clear语句，清空队列中全部元素
    def test_clear():
        queue = Queue([2,5,3,4,'hi'])
        assert len(queue) == 5
        queue.clear()
        assert len(queue) == 0

    test_init()
    test_push()
    test_iter()
    test_clear()
    
    print("end")