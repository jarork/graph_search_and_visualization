"""
    树和图结构的Python实现
    作者:Jake Huang
    邮箱:jarork@qq.com
    博客:Jakehuang.com

    功能:
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

import pyecharts

class Node:
    """
        节点模型 -> 用于存储每个节点的数据
        数据包括节点名，以及其他kwargs参数
    """
    def __init__(self, name : str, **kwargs):
        """
            节点初始化
        : param name : 节点名
        : param kwargs->self.properties : 额外添加的节点属性，如x，y等。用于heuristic函数
        """
        self.name = name
        self.attr = kwargs

    def dict(self):
        nodes_data = {"name" : self.name}
        nodes_data.update(self.attr)
        return nodes_data

    def __repr__(self):
        return self.name

class Edge:
    """
        边模型 -> 用于存储节点之间的连接关系
        分为起点和终点
    """
    def __init__(self, source:str, target:str, value=None, **kwargs):
        """
            边的初始化
        : param source : 起点的节点名
        : param target : 终点的节点名
        """
        self.source = source
        self.target = target
        self.value = value
        self.attr = kwargs

    def __repr__(self):
        string = "{} -> {}".format(self.source, self.target)

        if self.value:
            string += " : {}".format(self.value)
        else:
            string += " : None"

        if self.attr:
            string += "  "
            string += str(self.attr)

        return string

    def dict(self):
        edges_data = {
                    "source":self.source,
                    "target":self.target,
                    "value":self.value,
                    }
        edges_data.update(self.attr)
        return edges_data

class Graph:
    def __init__(self, nodes:list, edges:list):
        """
            创建双向图结构
        : param nodes : 图的所有结点（列表）
        : param edges : 图的所有边（列表）
        """

        self.nodes = nodes
        self.edges = edges

    def get_json():
        pass

    def print_graph(self, **kwargs):
        nodes_printable = [n.dict() for n in self.nodes]
        edges_printable = [e.dict() for e in self.edges]

        graph = pyecharts.Graph("Romania")

        graph.add("",nodes_printable, edges_printable, **kwargs)
        graph.render("./Romania.html")

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
    
    def get_data_romania():
        nodes_book = {
            "Oradea" : {"value":30, "symbolSize":5, "population":450000},
            "Zerind" : {"value":30, "symbolSize":5, "population":450000},
            "Arad" : {"value":30, "symbolSize":5, "population":450000},
            "Timisoara" : {"value":30, "symbolSize":5, "population":450000},
            "Lugoj" : {"value":30, "symbolSize":5, "population":450000},
            "Mehadia" : {"value":30, "symbolSize":5, "population":450000},
            "Dobreta" : {"value":30, "symbolSize":5, "population":450000},
            "Craiova" : {"value":30, "symbolSize":5, "population":450000},
            "Pitesti" : {"value":30, "symbolSize":5, "population":450000},
            "Rimnicu Vilcea" : {"value":30, "symbolSize":5, "population":450000},
            "Sibiu" : {"value":30, "symbolSize":5, "population":450000},
            "Fagaras" : {"value":30, "symbolSize":5, "population":450000},
            "Bucharest" : {"value":30, "symbolSize":5, "population":450000},
            "Giurgiu" : {"value":30, "symbolSize":5, "population":450000},
            "Urziceni" : {"value":30, "symbolSize":5, "population":450000},
            "Vaslui" : {"value":30, "symbolSize":5, "population":450000},
            "Iasi" : {"value":30, "symbolSize":5, "population":450000},
            "Neamt" : {"value":30, "symbolSize":5, "population":450000},
            "Hirsova" : {"value":30, "symbolSize":5, "population":450000},
            "Eforie" : {"value":30, "symbolSize":5, "population":450000},
        }

        edges_book = [
            ("Oradea", "Zerind", 71),
            ("Oradea", "Sibiu", 151),
            ("Zerind", "Arad", 75),
            ("Arad", "Sibiu", 140),
            ("Arad", "Timisoara", 118),
            ("Timisoara", "Lugoj", 111),
            ("Lugoj", "Mehadia", 70),
            ("Mehadia", "Dobreta", 75),
            ("Dobreta", "Craiova", 120),
            ("Craiova", "Rimnicu Vilcea", 146),
            ("Craiova", "Pitesti", 138),
            ("Rimnicu Vilcea", "Sibiu", 80),
            ("Rimnicu Vilcea", "Pitesti", 97),
            ("Pitesti", "Bucharest", 101),
            ("Sibiu", "Fagaras", 99),
            ("Fagaras", "Bucharest", 211),
            ("Bucharest", "Giurgiu", 90),
            ("Bucharest", "Urziceni", 85),
            ("Urziceni", "Vaslui", 142),
            ("Urziceni", "Hirsova", 98),
            ("Hirsova", "Eforie", 86),
            ("Vaslui", "Iasi", 92),
            ("Iasi", "Neamt", 87)
        ]

        nodes = []
        edges = []
        for name, attr in nodes_book.items():
            nodes.append(Node(name, **attr))
        
        for edge in edges_book:
            source, target = edge[:2]
            if len(edge) > 2 and isinstance(edge[2], int):
                value = edge[2]
                edges.append(Edge(source, target, value))
                edges.append(Edge(target, source, value))

                if len(edge) > 3 and isinstance(edge[3], dict):
                    attr = edge[3]
                    edges.append(Edge(source, target, value, **attr))
                    edges.append(Edge(target, source, value, **attr))

            if len(edge) > 2 and isinstance(edge[2], dict):
                attr = edge[2]
                edges.append(Edge(source, target, **attr))
                edges.append(Edge(target, source, **attr))
        
        return nodes, edges
    
    nodes, edges = get_data_romania()
    graph = Graph(nodes, edges)

    print_kwargs = dict(categories=None, # 结点分类的类目，结点可以指定分类，也可以不指定。
                is_focusnode=True, # 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。默认为 True
                is_roam=True,
                # is_rotatelabel=True, # 是否旋转标签，默认为 False
                # graph_layout="circular", # 布局类型，默认force=力引导图，circular=环形布局
                # graph_edge_length=100, # 力布局下边的两个节点之间的距离，这个距离也会受 repulsion 影响。默认为 50，TODO 值越大则长度越长
                graph_gravity=0.2, # 点受到的向中心的引力因子。TODO 该值越大节点越往中心点靠拢。默认为 0.2
                graph_repulsion=1000, # 节点之间的斥力因子。默认为 50，TODO 值越大则斥力越大
                is_label_show=True,
                 line_curve=0.05) # 线的弯曲度
    graph.print_graph(**print_kwargs)
    pass
