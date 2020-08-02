"""
    业务逻辑层
    提供图的查找和遍历方法
"""

from style_controller import StyleCtrl
from data_logic import DataAlgos
from data_manager import DataManager
from time import sleep
from copy import deepcopy


class GraphManager:
    def __init__(self,
                 json_path_nodes,
                 json_path_edges,
                 mirror_edges=False,
                 animation=True,
                 frames_per_minute=60
                 ):
        """
            创建双向图结构
        """
        # 建立存放节点和边的数据表
        self.nodes = DataManager.import_json_nodes(json_path_nodes)
        self.edges = DataManager.import_json_edges(json_path_edges, mirror_edges)

        # 建立工作区的备份，以便每次搜索完可以重新加载工作区
        self.nodes_backup = deepcopy(self.nodes)
        self.edges_backup = deepcopy(self.edges)

        # 建立存放节点和边的索引，节点的索引为name，边的索引为source和target
        self.get_node = DataManager.create_nodes_dict(self.nodes)
        self.targets, self.sources = DataManager.create_edges_dict(
            self.edges)

        # 建立查找队列
        self.queue = []

        # 建立数据控制器
        DataManager.init_data(self.nodes, self.edges)
        DataAlgos.init_data(self.get_node, self.targets, self.sources)

        # 是否开启动画，以及动画帧率
        self.animation = animation
        self.frames_per_minute = frames_per_minute

    def reload_workspace(self):
        # 清空工作区，包括所有节点和边以及引用它们的容器
        del self.queue, self.get_node, self.targets, self.sources, self.nodes, self.edges

        self.nodes = deepcopy(self.nodes_backup)
        self.edges = deepcopy(self.edges_backup)

        # 重新生成节点和边的索引
        self.get_node = DataManager.create_nodes_dict(self.nodes)
        self.targets, self.sources = DataManager.create_edges_dict(
            self.edges)
        
        # 重新建立查找队列
        self.queue = []

        # 重新建立数据控制器
        DataManager.init_data(self.nodes, self.edges)
        DataAlgos.init_data(self.get_node, self.targets, self.sources)

    def add_frame(self, last_frame=False):
        """
            给动画添加一帧
        : param last_frame : 是否最后一帧
        """
        if self.animation == True:
            DataManager.print_html()
            sleep(60 / self.frames_per_minute)
        if last_frame == True:
            DataManager.print_html()

    def a_star(self,
               root: str,          # 查找起始点
               end: str,           # 查找终止点
               func_g=DataAlgos.get_g_cost,               # 实际成本计算公式：g(n)
               func_h=DataAlgos.get_euclid_distance,      # 预期成本计算公式：h(n)函数
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
                target_node = self.get_node[target_name]    # 获取子节点对象
                target_path = cur_path.copy()               # 获取子节点路径
                target_path.append(target_name)             # 更新子节点路径

                tgt_g, tgt_h, tgt_f = g_cost, h_cost, f_cost    # 获取子节点当前成本，预期成本，总共成本
                # 获取子节点坐标
                cur_x, cur_y = target_node.attr["x"], target_node.attr["y"]

                # 如果这个节点的路径有环，则略过这个节点
                if DataAlgos.is_circular_path(target_path):
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
                        target_node.prop.update({"expanded": 0})

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

                        # 如果在队列中已经存在更高成本的这个节点，就把它删除掉
                        if target_node.prop["expanded"] != 0:
                            self.queue = DataAlgos.drop_node_from_queue(self.queue, target_name)

                # 把临边标记成已展开
                StyleCtrl.be_searched_edge(edge)
                target_node.prop["expanded"] += 1

                target_node_data = [target_node, tgt_g,
                                    tgt_h, tgt_f, target_path]

                # 如果是终点，打印，重置工作区，并返回
                if target_name == end:
                    final_edge = DataAlgos.get_edge(
                        target_path[-2], target_path[-1])

                    StyleCtrl.be_current_edge(final_edge)
                    self.add_frame(last_frame=True)

                    self.reload_workspace()
                    return target_path, DataAlgos.get_path_distance(target_path)

                # 使用二分插入法将本节点插入查找队列
                self.queue = DataAlgos.insert(
                    self.queue, target_node_data, mode=insert_mode)

            # 在所有子节点渲染完毕后，刷新页面
            self.add_frame()

            # 把当前节点的样式调整成已查找的样式
            StyleCtrl.be_searched_path(cur_path)

            if cur_node.name != root:
                StyleCtrl.be_searched_node(cur_node)

        else:
            self.reload_workspace()
            return None, None

    def ucs(self,
            root,           # 查找的起始点
            end,            # 查找的终止点
            func_g=DataAlgos.get_g_cost,     # 实际成本计算公式 g(n)
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
            func_h=DataAlgos.get_euclid_distance,     # 实际成本计算公式 g(n)，默认为欧几里得
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

    def ids(self,
            root,           # 查找的起始点
            end,            # 查找的终止点
            depth_limit=5,          # 是否限制搜索层数
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

        if not depth_limit:
            raise Exception("你必须限制IDS的搜索层数")

        l = 1
        while l <= depth_limit:
            result = self.dfs(root, end, depth_limit=l, is_dijkstra=is_dijkstra)
            
            if result[0] == None:
                l += 1
            else:
                return result
        return None, None