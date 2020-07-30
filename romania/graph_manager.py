"""
    业务逻辑层
    提供图的查找和遍历方法
"""
from pyecharts.charts import Graph
from pyecharts import options as opts
from data_structure import Node, Edge
from style_sheet import Style
import json


class GraphManager:
    def __init__(self, json_path_nodes, json_path_edges, mirror_edges=False):
        """
            创建双向图结构
        """
        # 建立存放节点和边的数据表
        self.nodes = self.import_json_nodes(json_path_nodes)
        self.edges = self.import_json_edges(json_path_edges, mirror_edges)

        # 建立存放节点和边的哈希表，节点哈希表的索引为name，边的哈希表的索引为source和target
        """根据节点名/ID创建节点的索引，这样就可以在众多节点中快速定位到一个节点了"""
        self.nodes_hash = self.create_nodes_hash_table(self.nodes)

        """根据起始节点名/ID，以及目标节点名/ID创建索引
        这样，就可以查找一个点的所有连接，能到达的所有节点
        以及能到达一个节点的所有节点和临边了"""
        self.source_edges_hash, self.target_edges_hash = self.create_edges_hash_tables(
            self.edges)

        print(self.source_edges_hash)

    def import_json_nodes(self, json_path) -> list:
        """
            从JSON中导入节点
        : param json_path : JSON文件的绝对或相对路径
        : return nodes_table : 存储所有导入节点的数据表
        """

        nodes = []
        with open("./city_nodes.json", 'r') as f:
            nodes_json = f.read()
        nodes_book = json.loads(nodes_json)

        for name, attr in nodes_book.items():
            nodes.append(Node(name, **attr))

        return nodes

    def import_json_edges(self, json_path, mirror_edges=False):
        """
            从JSON中导入连接
        : param json_path : JSON文件的绝对或相对路径
        : param mirror_edges : 如果JSON中的边是单向的，可以把此项设为True变为双向边
        : return edges_table : 存储所有导入边的数据表
        """

        edges_table = []
        with open("./city_edges.json", 'r') as f:
            edges_json = f.read()
        edges_book = json.loads(edges_json)

        for edge in edges_book:
            # 插入所有正向的连接
            # 为正向连接插入样式
            edge.update(Style.forward_style)
            edges_table.append(Edge(**edge))

            if mirror_edges == True:
                # 重新插入所有反向的连接
                # 为反向连接添加样式
                edge.update(Style.backward_style)

                edge["source"], edge["target"] = edge["target"], edge["source"]
                edges_table.append(Edge(**(edge)))

        return edges_table

    def create_nodes_hash_table(self, nodes_table) -> dict:
        # 为nodes表建立节点名name的索引，以便使节点的查找效率为O(1)。
        nodes_hash_table = {}
        for node_model in nodes_table:
            node_name = node_model.name

            nodes_hash_table.update({node_name: node_model})
        return nodes_hash_table

    def create_edges_hash_tables(self, edges_table) -> tuple:
        # 为edges表建立source和target项的索引，以便使边的查找效率为O(1)。
        # 把所有边进行分类，每个节点可作为起点和终点，每个起点和终点分为一类。
        source_edges_hash_table = {}
        target_edges_hash_table = {}
        for edge_model in edges_table:
            source = edge_model.source
            target = edge_model.target
            value = edge_model.value
            attr = edge_model.attr

            if source not in source_edges_hash_table:
                source_edges_hash_table.update({source: {}})

            source_edges_hash_table[source].update(
                {target: edge_model})

            if target not in target_edges_hash_table:
                target_edges_hash_table.update({target: {}})

            target_edges_hash_table[target].update(
                {source: edge_model})

        return (source_edges_hash_table, target_edges_hash_table)

    def export_json_nodes(self):
        nodes_table = {key: node_model.dict()
                       for key, node_model in self.nodes_hash.items()}
        json_nodes = json.dumps(
            nodes_table, sort_keys=True, indent=4, separators=(',', ': '))
        with open("./output_json_nodes.json", 'w') as f:
            f.write(json_nodes)

    def export_json_edges(self):
        source_edges = {source: {target_name: str(target_attr)
                                 for target_name, target_attr in target.items()}
                        for source, target in self.source_edges_hash.items()}
        target_edges = {target: {source_name: str(source_attr)
                                 for source_name, source_attr in source.items()}
                        for target, source in self.target_edges_hash.items()}
        json_source_edges = json.dumps(
            source_edges, sort_keys=True, indent=4, separators=(',', ': '))
        json_target_edges = json.dumps(
            target_edges, sort_keys=True, indent=4, separators=(',', ': '))
        with open("./output_json_source_edges.json", 'w') as f:
            f.write(json_source_edges)
        with open("./output_json_target_edges.json", 'w') as f:
            f.write(json_target_edges)

    def output_graph_html(self, init_options: dict, html_path: str = "./chart.html", **render_style):
        """
            将图导出为HTML形式
        : param init_options : PyEcharts全局配置，请在style库中修改。
        : param html_path : 输出的HTML地址，可使用绝对路径或者相对路径。
        : param **render_style : PyEcharts的渲染配置，请在style库中修改
        """
        nodes_printable = [opts.GraphNode(**n.dict()) for n in self.nodes]
        edges_printable = [opts.GraphLink(**e.dict()) for e in self.edges]

        graph = Graph(init_options)

        graph.add("", nodes_printable, edges_printable, **render_style)
        graph.render(html_path)

    def __iter__(self, path=True, method="bfs"):
        """
            图的遍历，无视终点，必须遍历所有元素
        : param path : 是否返回每一结点的路径 bool
        : param method : 使用的查找方法，默认BFS
        : yield node or path : 返回树内所有结点
        """
        pass

    def insert(self, nodes: list):
        """
            在图中插入新的节点
        : param nodes : 新添的节点（列表）
        """
        pass

    def a_star(self, start, func_g=None, func_h=None, path=True):
        """
            A*查找
        : param path : 是否返回每一结点的路径 bool
        : param start : 查找的起点
        : param func_g function(g) return fg : 计算从起点到达该点所需的路程的函数
        : param func_h function(h) return fh : 估算从该点到达终点大概要走路程的函数
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """

    def ucs(self, path=True):
        """
            统一成本查找 (Uniform Cost Search)
            优先展开从起点能到达的最近的点。当起点到所有未展开点的路程都一致的情况，就等价于BFS
        : param path : 是否返回目的地的整条路径
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass

    def gs(self, path=True):
        """
            贪婪查找 (Greedy Search)
            优先展开到终点估计路程最近的节点。
        """
        pass

    def bfs(self, path=True):
        """
            广度优先查找 (Breadth First Search)
        : param path : 是否返回目的地的整条路径
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass

    def dfs(self, path=True, depth_limit=None):
        """
            深度优先查找 (Depth First Search)
            如果限制搜索层数，则变为DLS (Depth Limited Search)
        : param path : 是否返回目的地的整条路径
        : param depth_limit : 查找深度的限制（层数）
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass

    def ids(self, path=True, depth_limit=None):
        """
            迭代深化搜索 (Iterative Deepening Search)
        : param path : 是否返回目的地的整条路径
        : param depth_limit : 查找深度的限制（层数）
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass
