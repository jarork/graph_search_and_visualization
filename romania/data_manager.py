"""
    数据读写层
"""

from pyecharts.charts import Graph
from pyecharts import options as opts
from data_structure import Node, Edge
from style_sheet import Style
import json

class DataManager:
    """
        数据读写层
        提供数据的导入导出方法
        包括读写JSON节点和边，写入HTML
    """
    @classmethod
    def init_data(cls, nodes, edges):
        """
            数据控制者的初始化，读入节点和边的信息
        : param nodes : 包含所有节点对象的列表
        : param edges : 包含所有边对象的列表
        """
        cls.nodes = nodes
        cls.edges = edges

    @classmethod
    def import_json_nodes(cls, json_path) -> list:
        """
            从JSON中导入节点
        : param json_path : JSON文件的绝对或相对路径
        : return nodes_table : 存储所有导入节点的数据表
        """

        nodes = []
        with open(json_path, 'r') as f:
            nodes_json = f.read()
        nodes_book = json.loads(nodes_json)

        for name, attr in nodes_book.items():
            nodes.append(Node(name, **attr))

        return nodes

    @classmethod
    def import_json_edges(cls, json_path, mirror_edges=False):
        """
            从JSON中导入连接
        : param json_path : JSON文件的绝对或相对路径
        : param mirror_edges : 如果JSON中的边是单向的，可以把此项设为True变为双向边
        : return edges_table : 存储所有导入边的数据表
        """

        edges_table = []
        with open(json_path, 'r') as f:
            edges_json = f.read()
        edges_book = json.loads(edges_json)

        for edge in edges_book:
            # 插入所有正向的连接
            # 为正向连接插入样式
            edge.update(Style.FORWARD_STYLE)
            edges_table.append(Edge(**edge))

            if mirror_edges == True:
                # 重新插入所有反向的连接
                # 为反向连接添加样式
                edge.update(Style.BACKWARD_STYLE)

                edge["source"], edge["target"] = edge["target"], edge["source"]
                edges_table.append(Edge(**(edge)))

        return edges_table

    @classmethod
    def create_nodes_dict(cls, nodes_table) -> dict:
        """
            根据节点名/ID创建节点的索引，这样就可以在众多节点中快速定位到一个节点了
        : param nodes_table : 节点表
        : return nodes_hash_table : 以节点名为索引的哈希表
        """
        # 为nodes表建立节点名name的索引，以便使节点的查找效率为O(1)。
        nodes_hash_table = {}
        for node_model in nodes_table:
            node_name = node_model.name

            nodes_hash_table.update({node_name: node_model})
        return nodes_hash_table

    @classmethod
    def create_edges_dict(cls, edges_table) -> tuple:
        """
            根据起始节点名/ID，以及目标节点名/ID创建索引
            这样，就可以查找一个点的所有连接，能到达的所有节点
            以及能到达一个节点的所有节点和临边了
        : param edges_table : 没有索引的临边列表
        : return (source_hash_table, target_hash_table) : 以临边起终节点名为索引的2个哈希表
        """
        # 为edges表建立source和target项的索引，以便使边的查找效率为O(1)。
        # 把所有边进行分类，每个节点可作为起点和终点，每个起点和终点分为一类。
        targets_table = {}
        sources_table = {}
        for edge_model in edges_table:
            source = edge_model.source
            target = edge_model.target
            value = edge_model.value
            attr = edge_model.attr

            if source not in targets_table:
                targets_table.update({source: {}})

            targets_table[source].update(
                {target: edge_model})

            if target not in sources_table:
                sources_table.update({target: {}})

            sources_table[target].update(
                {source: edge_model})

        return (targets_table, sources_table)

    @classmethod
    def export_json_nodes(cls):
        nodes_table = {key: node_model.dict()
                       for key, node_model in cls.get_node.items()}
        json_nodes = json.dumps(
            nodes_table, sort_keys=True, indent=4, separators=(',', ': '))
        with open("./output_json_nodes.json", 'w') as f:
            f.write(json_nodes)

    @classmethod
    def export_json_edges(cls):
        source_edges = {source: {target_name: str(target_attr)
                                 for target_name, target_attr in target.items()}
                        for source, target in cls.targets.items()}
        target_edges = {target: {source_name: str(source_attr)
                                 for source_name, source_attr in source.items()}
                        for target, source in cls.sources.items()}
        json_source_edges = json.dumps(
            source_edges, sort_keys=True, indent=4, separators=(',', ': '))
        json_target_edges = json.dumps(
            target_edges, sort_keys=True, indent=4, separators=(',', ': '))
        with open("./output_json_source_edges.json", 'w') as f:
            f.write(json_source_edges)
        with open("./output_json_target_edges.json", 'w') as f:
            f.write(json_target_edges)

    @classmethod
    def print_html(cls,
                   html_path: str = Style.DEFAULT_HTML_PATH,
                   init_options: dict = Style.DEFAULT_INIT_OPTS,
                   render_style: dict = Style.DEFAULT_RENDER_OPTS
                   ):
        """
            将图导出为HTML形式
        : param init_options : PyEcharts全局配置，请在style库中修改。
        : param html_path : 输出的HTML地址，可使用绝对路径或者相对路径。
        : param **render_style : PyEcharts的渲染配置，请在style库中修改
        """
        nodes_printable = [opts.GraphNode(
            **n.styles_dict()) for n in cls.nodes]
        edges_printable = [opts.GraphLink(
            **e.styles_dict()) for e in cls.edges]

        graph = Graph(init_options)

        graph.add("", nodes_printable, edges_printable, **render_style)
        graph.render(html_path)
