"""
    样式控制层
    提供了控制节点和边样式的诸多方法
"""

from style_sheet import Style
from data_controller import DataCtrl


class StyleCtrl:
    """
        样式控制层
        提供了控制节点和边样式的诸多方法
    """
    @classmethod
    def be_root_node(cls, node):
        """
            设置本节点为根节点样式
        : param node : 节点对象
        """
        node.attr.update(Style.ROOT_NODE_STYLE)

    @classmethod
    def be_terminal_node(cls, node):
        """
            设置本节点为终节点样式
        : param node : 节点对象
        """
        node.attr.update(Style.TERMINAL_NODE_STYLE)

    @classmethod
    def be_searched_node(cls, node):
        """
            设置本节点为已搜节点样式
        : param node : 节点对象
        """
        node.attr.update(Style.SEARCHED_NODE_STYLE)

    @classmethod
    def be_current_node(cls, node):
        """
            设置本节点为当前节点样式
        : param node : 节点对象
        """
        node.attr.update(Style.CURRENT_NODE_STYLE)

    @classmethod
    def be_searched_edge(cls, edge):
        """
            设置本条边为已搜边的样式
        : param edge : 边对象
        """
        edge.attr.update(Style.SEARCHED_EDGE_STYLE)

    @classmethod
    def be_current_edge(cls, edge):
        """
            设置本条边为当前边的样式
        : param edge : 边对象
        """
        edge.attr.update(Style.CURRENT_EDGE_STYLE)

    @classmethod
    def be_current_path(cls, path_of_nodes):
        """
            设置本条路径中所有边为当前边的样式
        : param path_of_nodes : 含有节点名的路径列表
        """
        for i in range(len(path_of_nodes) - 1):
            edge = DataCtrl.get_edge(path_of_nodes[i], path_of_nodes[i+1])
            cls.be_current_edge(edge)

    @classmethod
    def be_searched_path(cls, path_of_nodes):
        """
            设置本条路径中所有边为已搜边的样式
        : param path_of_nodes : 含有节点名的路径列表
        """
        for i in range(len(path_of_nodes) - 1):
            edge = DataCtrl.get_edge(path_of_nodes[i], path_of_nodes[i+1])
            cls.be_searched_edge(edge)
