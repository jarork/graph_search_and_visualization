"""
    树和图结构的Python实现
    作者：Jake Huang
    邮箱：jarork@qq.com
    博客：Jakehuang.com

    功能：
    1. 支持A星，贪婪，BFS查找
    2. 支持DFS，DLS，IDS查找
    3. 使用查找节点的方法时，可设置path的bool值，是否返回整条路径
    4. 使用A星和贪婪时，启发函数(heuristic function)h(n)可以从外部传入，也可以继承重写在你的子类里。


        A* > (UCS or GS) > BFS
        f(n) = g(n) + h(n)
        g(n)为到达该n点的实际路径，
        h(n)为该点到终点的估算路程，
        f(n)从起点到终点经过n点的总共估算路程。

        当g(n) = 0， 即f(n) = h(n)时，A*等价于GS；
        当h(n) = 0， 即f(n) = g(n)时，A*等价于UCS；
        当g(n) = 层数(n)时，UCS等价于BFS。
"""

class Node:
    """
        节点模型 -> 用于存储每个节点的数据
        数据包括节点名，父节点，子节点列表，以及其他kwargs参数
    """
    def __init__(
                self,
                name : str,                         # 节点名
                neighbors : dict{name: {cost:}} or None,           # 相邻节点名
                cost : int or float = None,         # 从各个父节点到本节点的路径长度
                g_cost : int or float = None,       # 从起点到本节点的最近路径长度
                h_cost : int or float = None,       # 从本节点到终点的估算长度
                **kwargs
                ):
        """
            节点初始化
        : param name : 节点名
        : param parent : 父节点名，根节点请传None
        : param children : 所有子节点名，末节点传None
        : param cost : 从父节点到本节点的路径长度
        : param g_cost : 从起点到本节点的路径长度
        : param h_cost : 从本节点到终点的估算长度
        : param kwargs->self.properties : 额外添加的节点属性，如x，y等。用于heuristic函数
        """
        self.name = name
        self.parent = parent
        self.children = children
        self.cost = cost
        self.g_cost = g_cost
        self.h_cost = h_cost

        self.properties = kwargs

class Graph:
    def __init__(self, nodes:list):
        """
            创建树结构
            {节点名：{}}
        : param nodes : 图的所有结点（列表）
        """
        pass
        # 判断tree_dict是否是一个树，还是图表

    def __iter__(self, path = True, method = "bfs"):
        """
            图的遍历，无视终点，必须遍历所有元素
        : param path : 是否返回每一结点的路径 bool
        : param method : 使用的查找方法，默认BFS
        : yield node or path : 返回树内所有结点
        """
        pass

    def insert(self, nodes:list):
        """
            在图中插入新的节点
        : param nodes : 新添的节点（列表）
        """
        pass

    def a_star(self, start, func_g = None, func_h = None, path = True):
        """
            A*查找
        : param path : 是否返回每一结点的路径 bool
        : param start : 查找的起点
        : param func_g function(g) return fg : 计算从起点到达该点所需的路程的函数
        : param func_h function(h) return fh : 估算从该点到达终点大概要走路程的函数
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """

    def ucs(self, path = True):
        """
            统一成本查找 (Uniform Cost Search)
            优先展开从起点能到达的最近的点。当起点到所有未展开点的路程都一致的情况，就等价于BFS
        : param path : 是否返回目的地的整条路径
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass

    def gs(self, path = True):
        """
            贪婪查找 (Greedy Search)
            优先展开到终点估计路程最近的节点。
        """
        pass

    def bfs(self, path = True):
        """
            广度优先查找 (Breadth First Search)
        : param path : 是否返回目的地的整条路径
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass
    
    def dfs(self, path = True, depth_limit = None):
        """
            深度优先查找 (Depth First Search)
            如果限制搜索层数，则变为DLS (Depth Limited Search)
        : param path : 是否返回目的地的整条路径
        : param depth_limit : 查找深度的限制（层数）
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass

    def ids(self, path = True, depth_limit = None):
        """
            迭代深化搜索 (Iterative Deepening Search)
        : param path : 是否返回目的地的整条路径
        : param depth_limit : 查找深度的限制（层数）
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass

if __name__ == "__main__":
    nodes = []
    nodes.append(Node())