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

from pyecharts.charts import Graph
from pyecharts import options as opts
import json
from style import Style

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
        self.__dict__.update(**kwargs)

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
        # self.__dict__.update(**kwargs)

    def __repr__(self):
        string = "{} -> {}".format(self.source, self.target)

        if self.value:
            string += " : {}".format(self.value)
        else:
            string += " : None"

        return string

    def dict(self):
        edges_data = {
                    "source":self.source,
                    "target":self.target,
                    "value":self.value,
                    "symbol":['none', 'arrow'],
                    "linestyle_opts": {"width":1,"color":"#fff","curveness":0.2}
                    # "label_opts":opts.LabelOpts(is_show=True, color="#fff", position="middle", formatter="{c}")
                    }
        edges_data.update(self.attr)
        return edges_data

class GraphManager:
    def __init__(self, nodes:list=None, edges:list=None):
        """
            创建双向图结构
        : param nodes : 图的所有结点（列表）
        : param edges : 图的所有边（列表）
        """

        self.nodes = []
        self.edges = []

    def import_json_nodes(self, json_path):
        """
            从JSON中导入节点
        : param json_path : JSON文件的绝对或相对路径
        """
        with open("./city_nodes.json", 'r') as f:
            nodes_json = f.read()
        nodes_book = json.loads(nodes_json)

        for name, attr in nodes_book.items():
            self.nodes.append(Node(name, **attr))

    def import_json_edges(self, json_path):
        """
            从JSON中导入连接
        : param json_path : JSON文件的绝对或相对路径
        """
        with open("./city_edges.json", 'r') as f:
            edges_json = f.read()
        edges_book = json.loads(edges_json)

        for edge in edges_book:
            ### 插入所有正向的连接
            # 为正向连接插入样式
            edge.update(Style.forward_style)
            self.edges.append(Edge(**edge))

            ### 重新插入所有反向的连接
            # 为反向连接添加样式
            edge.update(Style.backward_style)

            edge["source"], edge["target"] = edge["target"], edge["source"]
            self.edges.append(Edge(**(edge)))
        

    def output_graph_html(self, init_options:dict, html_path:str = "./chart.html", **render_style):
        """
            将图导出为HTML形式
        : param init_options : PyEcharts全局配置，请在style库中修改。
        : param html_path : 输出的HTML地址，可使用绝对路径或者相对路径。
        : param **render_style : PyEcharts的渲染配置，请在style库中修改
        """
        nodes_printable = [opts.GraphNode(**n.dict()) for n in self.nodes]
        edges_printable = [opts.GraphLink(**e.dict()) for e in self.edges]

        graph = Graph(init_options)

        graph.add("",nodes_printable, edges_printable, **render_style)
        graph.render(html_path)

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
    # 使用数据，创建图表
    graph_manager = GraphManager()
    graph_manager.import_json_nodes("./city_nodes.json")
    graph_manager.import_json_edges("./city_edges.json")

    graph_manager.output_graph_html(Style.init_opts, html_path="./Romania.html" ,**Style.render_opts)

