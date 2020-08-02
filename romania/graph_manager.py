"""
    业务逻辑层
    提供图的查找和遍历方法
"""
from pyecharts.charts import Graph
from pyecharts import options as opts
from data_structure import Node, Edge
from style_controller import StyleCtrl
from style_sheet import Style
from data_controller import DataCtrl
from time import sleep
import json


class GraphManager:
    frames_per_minute = 60

    def __init__(self, json_path_nodes, json_path_edges, mirror_edges=False, animation=True):
        """
            创建双向图结构
        """
        # 建立存放节点和边的数据表
        self.nodes = self.import_json_nodes(json_path_nodes)
        self.edges = self.import_json_edges(json_path_edges, mirror_edges)

        # 建立存放节点和边的哈希表，节点哈希表的索引为name，边的哈希表的索引为source和target
        self.get_node = self.create_nodes_hash_table(self.nodes)
        self.targets, self.sources = self.create_edges_hash_tables(
            self.edges)

        # 建立查找队列
        self.queue = []

        # 建立数据控制器
        DataCtrl.init_data(self.get_node, self.targets, self.sources)

        # 是否使用动画
        self.animation = animation

    def __iter__(self, path=True, method="bfs"):
        """
            图的遍历，无视终点，必须遍历所有元素
        : param path : 是否返回每一结点的路径 bool
        : param method : 使用的查找方法，默认BFS
        : yield node or path : 返回树内所有结点
        """
        pass

    def add_frame(self, end=False):
        if self.animation == True:
            self.print_html()
            sleep(60 / self.frames_per_minute)
        if end == True:
            self.print_html()

    def a_star(self,
               root: str,          # 查找起始点
               end: str,           # 查找终止点
               func_g=DataCtrl.get_g_cost,               # 实际成本计算公式：g(n)
               func_h=DataCtrl.get_euclid_distance,      # 预期成本计算公式：h(n)函数
               h_weight: int or float = 1,                               # Heuristic的权重
               mode="a_star",             # 查找模式
               depth_limit=None,          # 是否限制搜索层数
               is_dijkstra: bool = True    # 是否使用迪克斯特拉更新重复点的成本
               ):
        """
            A* 查找
        : param root : 查找的起始点
        : param end : 查找的终止点
        : param func_g function(g): 实际成本计算公式；计算从起点到达该点所需的路程的函数
        : param func_h function(h): Heuristic计算公式；估算从该点到达终点大概要走路程的函数，默认为使用欧几里得距离做Heuristic
        : param dijkstra : 是否使用迪克斯特拉算法，迪克斯特拉更新到达每个节点的最小成本，高于此成本的路径将被剔除不进行继续展开
        : param mode : 搜索模式。
                        "a_star" -> A*搜索；
                        "ucs" -> 统一成本搜索；
                        "gs" -> 贪婪搜索；
                        "bfs" -> 广度优先搜索；
        : param depth_limit : 最深搜索的层数，默认没有层数限制。
        : return path, g_cost : 返回到达目的地的整条路径，以及这条路径的长度
        """

        # 处理不正确的输入值
        if root == end:
            raise Exception("起点和终点是相同的，这毫无意义。")
        if root not in self.get_node:
            raise Exception("不存在这个起始点。")
        if end not in self.get_node:
            raise Exception("不存在这个终止点")

        root_node = self.get_node[root]
        end_node = self.get_node[end]
        end_x, end_y = end_node.attr["x"], end_node.attr["y"]

        # 把根节点、当前成本、预期成本、总共成本以及根路径放入查找队列
        self.queue.append([root_node, 0, 0, 0, [root_node.name]])

        # 增加根节点和目标节点的样式
        StyleCtrl.be_root_node(root_node)
        StyleCtrl.be_terminal_node(end_node)
        self.add_frame()

        # 每次从查找队列取出一个节点，直到队列为空（没有找到），或者找到目标节点跳出
        while len(self.queue) > 0:
            cur_node, g_cost, h_cost, f_cost, cur_path = self.queue.pop()

            # 渲染当前节点，如果这是根节点，则不渲染它
            if cur_node.name != root:
                StyleCtrl.be_current_node(cur_node)

            # 渲染当前节点的整条路径
            StyleCtrl.be_current_path(cur_path)
            self.add_frame()

            # 获取当前节点的所有临边
            fringes = self.targets[cur_node.name]

            for target_name, edge in fringes.items():
                # 获取子节点的数据
                tgt_g, tgt_h, tgt_f = g_cost, h_cost, f_cost    # 获取子节点当前成本，预期成本，总共成本
                cur_x, cur_y = target_node.attr["x"], target_node.attr["y"]     # 获取子节点坐标
                target_node = self.get_node[target_name]    # 获取子节点对象
                target_path = cur_path.copy()               # 获取子节点路径               
                target_path.append(target_name)             # 更新子节点路径

                # 如果这个节点的路径有环，则略过这个节点
                if DataCtrl.is_circular_path(target_path):
                    continue

                if mode == "a_star":
                    # A* mode: 成本计算公式 f(n) = g(n) + h(n)
                    tgt_g = func_g(tgt_g, edge.value, cost_eq_depth=False)
                    tgt_h = func_h(cur_x, cur_y, end_x, end_y)
                    tgt_f = tgt_g + tgt_h * h_weight
                    insert_mode = "DESC"

                elif mode == "ucs":
                    # Uniform Cost Search Mode： 成本计算公式 f(n) = g(n)
                    tgt_g = func_g(tgt_g, edge.value, cost_eq_depth=False)
                    tgt_h = 0
                    tgt_f = tgt_g
                    insert_mode = "DESC"

                elif mode == "gs":
                    # Greedy Search Mode: 成本计算公式 f(n) = h(n)
                    tgt_g = func_g(tgt_g, edge.value, cost_eq_depth=False)
                    tgt_h = func_h(cur_x, cur_y, end_x, end_y)
                    tgt_f = tgt_h
                    insert_mode = "DESC"

                elif mode == "bfs":
                    # Breadth First Search Mode: 成本计算公式 f(n) = g(n)
                    # g(n) = n
                    tgt_g = func_g(tgt_g, edge.value, cost_eq_depth=True)
                    tgt_h = 0
                    tgt_f = tgt_g
                    insert_mode = "FIFO"

                elif mode == "dfs":
                    # Depth First Search Mode: 成本计算公式 f(n) = g(n)
                    # g(n) = n
                    tgt_g = func_g(tgt_g, edge.value, cost_eq_depth=True)
                    tgt_h = 0
                    tgt_f = tgt_g
                    insert_mode = "FILO"

                elif mode == "ids":
                    # Depth First Search Mode: 成本计算公式 f(n) = g(n)
                    # g(n) = n
                    tgt_g = func_g(tgt_g, edge.value, cost_eq_depth=True)
                    tgt_h = 0
                    tgt_f = tgt_g
                    insert_mode = "FILO"

                else:
                    raise Exception("没有名为{}的算法。".format(mode))

                # 如果该节点的层数超过了层数限制，则略过所有兄弟节点，继续取下一节点
                if depth_limit and len(target_path)-1 > depth_limit:
                    break

                # 如果应用迪克斯特拉算法，搜索时则更新节点的实际成本
                if is_dijkstra == True:
                    if target_node.attr["value"] == "null":
                        # A*, UCS, GS优先展开最小成本节点，BFS优先展开最小深度节点
                        if mode not in ("dfs", "ids"):
                            target_node.attr["value"] = 99999999
                        # DFS和IDS优先展开的是深度最高的节点，所以节点的初始成本设为0
                        else:
                            target_node.attr["value"] = tgt_g

                        # 增加节点遍历次数    
                        target_node.prop.update({"expanded":0})

                    # 如果这条路径到达这个节点的实际成本高于之前路径的实际成本，那么就放弃这条路径
                    if tgt_g >= target_node.attr["value"]:
                        if mode in ("dfs", "ids") and tgt_g == target_node.attr["value"]:
                            if target_node.prop["expanded"]:
                                continue                            
                        else:
                            continue
                    else:
                        # 如果发现到达这个节点的更短的路径，那么就更新这个点的实际成本
                        target_node.attr["value"] = tgt_g

                # 把临边标记成已展开
                StyleCtrl.be_searched_edge(edge)
                target_node.prop["expanded"] += 1

                target_node_data = [target_node, tgt_g,
                               tgt_h, tgt_f, target_path]

                # 如果是终点，打印并跳出
                if target_name == end:
                    final_edge = DataCtrl.get_edge(
                        target_path[-2], target_path[-1])

                    StyleCtrl.be_current_edge(final_edge)
                    self.add_frame(end=True)

                    return target_path, tgt_g

                # 使用二分插入法将本节点插入查找队列
                self.queue = DataCtrl.insert(
                    self.queue, target_node_data, mode=insert_mode)

            # 在所有子节点渲染完毕后，刷新页面
            self.add_frame()

            # 把当前节点的样式调整成已查找的样式
            StyleCtrl.be_searched_path(cur_path)

            if cur_node.name != root:
                StyleCtrl.be_searched_node(cur_node)

        else:
            return None, None

    def ucs(self,
            root,           # 查找的起始点
            end,            # 查找的终止点
            func_g=DataCtrl.get_g_cost,     # 实际成本计算公式 g(n)
            depth_limit=None,          # 是否限制搜索层数
            is_dijkstra=True    # 是否使用迪克斯特拉更新重复点的成本
            ):
        """
            统一成本查找 (Uniform Cost Search)
            优先展开从起点能到达的最近的点。当起点到所有未展开点的路程都一致的情况，就等价于BFS
        : param root : 查找的起始点
        : param end : 查找的终止点
        : param func_g function(g): 实际成本计算公式；计算从起点到达该点所需的路程的函数
        : param depth_limit : 最深搜索的层数，默认没有层数限制。
        : param dijkstra : 是否使用迪克斯特拉算法，迪克斯特拉更新到达每个节点的最小成本，高于此成本的路径将被剔除不进行继续展开
        : return path, g_cost : 返回到达目的地的整条路径，以及这条路径的长度
        """

        return self.a_star(root, end, func_g=func_g, depth_limit=depth_limit, is_dijkstra=is_dijkstra, mode="ucs")

    def gs(self,
            root,           # 查找的起始点
            end,            # 查找的终止点
            func_h=DataCtrl.get_euclid_distance,     # 实际成本计算公式 g(n)，默认为欧几里得
            depth_limit=None,          # 是否限制搜索层数
            is_dijkstra=True    # 是否使用迪克斯特拉更新重复点的成本
           ):
        """
            贪婪查找 (Greedy Search)
            优先展开到终点估计路程最近的节点。
        : param root : 查找的起始点
        : param end : 查找的终止点
        : param func_h : Heuristic计算公式；估算从该点到达终点大概要走路程的函数，默认为使用欧几里得距离做Heuristic
        : param depth_limit : 最深搜索的层数，默认没有层数限制。
        : param dijkstra : 是否使用迪克斯特拉算法，迪克斯特拉更新到达每个节点的最小成本，高于此成本的路径将被剔除不进行继续展开
        : return path, g_cost : 返回到达目的地的整条路径，以及这条路径的长度
        """

        return self.a_star(root, end, func_h=func_h, depth_limit=depth_limit, is_dijkstra=is_dijkstra, mode="gs")

    def bfs(self,
            root,           # 查找的起始点
            end,            # 查找的终止点
            depth_limit=None,          # 是否限制搜索层数
            is_dijkstra=True    # 是否使用迪克斯特拉更新重复点的成本
            ):
        """
            广度优先查找 (Breadth First Search)
            优先展开最小深度的节点
        : param root : 查找的起始点
        : param end : 查找的终止点
        : param depth_limit : 最深搜索的层数，默认没有层数限制。
        : param dijkstra : 是否使用迪克斯特拉算法，迪克斯特拉更新到达每个节点的最小成本，高于此成本的路径将被剔除不进行继续展开
        : return path, g_cost : 返回到达目的地的整条路径，以及这条路径的长度
        """

        return self.a_star(root, end, depth_limit=depth_limit, is_dijkstra=is_dijkstra, mode="bfs")

    def dfs(self,
            root,           # 查找的起始点
            end,            # 查找的终止点
            depth_limit=None,          # 是否限制搜索层数
            is_dijkstra=True    # 是否使用迪克斯特拉更新重复点的成本
            ):
        """
            深度优先查找 (Depth First Search)
            优先展开最大深度的节点
        : param root : 查找的起始点
        : param end : 查找的终止点
        : param depth_limit : 最深搜索的层数，默认没有层数限制。
        : param dijkstra : 是否使用迪克斯特拉算法，迪克斯特拉更新到达每个节点的最小成本，高于此成本的路径将被剔除不进行继续展开
        : return path, g_cost : 返回到达目的地的整条路径，以及这条路径的长度
        """

        return self.a_star(root, end, is_dijkstra=is_dijkstra, depth_limit=depth_limit, mode="dfs")

    def ids(self, path=True, depth_limit=None):
        """
            迭代深化搜索 (Iterative Deepening Search)
        : param path : 是否返回目的地的整条路径
        : param depth_limit : 查找深度的限制（层数）
        : return node or path : 返回目的地元素或者到达目的地的整条路径
        """
        pass

    def import_json_nodes(self, json_path) -> list:
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

    def import_json_edges(self, json_path, mirror_edges=False):
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

    def create_nodes_hash_table(self, nodes_table) -> dict:
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

    def create_edges_hash_tables(self, edges_table) -> tuple:
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

    def export_json_nodes(self):
        nodes_table = {key: node_model.dict()
                       for key, node_model in self.get_node.items()}
        json_nodes = json.dumps(
            nodes_table, sort_keys=True, indent=4, separators=(',', ': '))
        with open("./output_json_nodes.json", 'w') as f:
            f.write(json_nodes)

    def export_json_edges(self):
        source_edges = {source: {target_name: str(target_attr)
                                 for target_name, target_attr in target.items()}
                        for source, target in self.targets.items()}
        target_edges = {target: {source_name: str(source_attr)
                                 for source_name, source_attr in source.items()}
                        for target, source in self.sources.items()}
        json_source_edges = json.dumps(
            source_edges, sort_keys=True, indent=4, separators=(',', ': '))
        json_target_edges = json.dumps(
            target_edges, sort_keys=True, indent=4, separators=(',', ': '))
        with open("./output_json_source_edges.json", 'w') as f:
            f.write(json_source_edges)
        with open("./output_json_target_edges.json", 'w') as f:
            f.write(json_target_edges)

    def print_html(
        self, html_path: str = Style.DEFAULT_HTML_PATH,
        init_options: dict = Style.DEFAULT_INIT_OPTS,
        render_style: dict = Style.DEFAULT_RENDER_OPTS
    ):
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
