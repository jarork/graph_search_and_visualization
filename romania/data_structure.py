"""
    图表数据结构
"""


class Node:
    """
        节点模型 -> 用于存储每个节点的数据
        数据包括节点名，以及其他kwargs参数
    """

    def __init__(self, name: str, **kwargs):
        """
            节点初始化
        : param name : 节点名
        : param kwargs->self.properties : 额外添加的节点属性，如x，y等。用于heuristic函数
        """
        self.name = name
        self.attr = kwargs
        self.prop = {}
        # self.__dict__.update(**kwargs)

    def dict(self):
        nodes_data = {"name": self.name}
        nodes_data.update(self.attr)
        return nodes_data

    def __repr__(self):
        return "<NodeModel name = {}>".format(self.name)


class Edge:
    """
        边模型 -> 用于存储节点之间的连接关系
        分为起点和终点
    """

    def __init__(self, source: str, target: str, value=None, **kwargs):
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
        string = "{} > {}".format(self.source, self.target)

        if self.value:
            string += " : {}".format(self.value)
        else:
            string += " : None"

        return "<EdgeModel {}>".format(string)

    def dict(self):
        edges_data = {
            "source": self.source,
            "target": self.target,
            "value": self.value,
        }
        edges_data.update(self.attr)
        return edges_data
