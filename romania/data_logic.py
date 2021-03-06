"""
    数据业务层
    提供帮助获取及修改数据的方法
"""

class DataAlgos:
    """
        数据业务层
        提供帮助获取及修改数据的方法
    """

    @classmethod
    def init_data(cls, nodes, target_edges, source_edges):
        """
            数据控制者的初始化，读入节点和边的信息
        : param nodes : 包含所有节点对象的列表
        : param target_edges : 包含建立出发点索引的边字典
        : param source_edges : 包含建立到达点索引的边字典
        """
        cls.nodes = nodes
        cls.target_edges = target_edges
        cls.source_edges = source_edges

    @classmethod
    def get_edge(cls, source_name, target_name):
        """
            已知两点返回临边，如果两个点没有临边则返回None
        : param source_name : 起点名
        : param target_name : 终点名
        : return edge or None : 临边对象
        """
        return cls.target_edges[source_name][target_name]

    @classmethod
    def insert(cls, queue, node, mode = "DESC"):
        """
            正逆序排列的二分插入
            
        : param queue : 查找队列，按照队列的f_cost参数从大到小的顺序存放的节点
                        节点包node的数据结构：
                        list[节点对象, g_cost, h_cost, f_cost, 节点路径(包含路径上全部节点对象)]
        : param mode : 插入模式
                        DESC -> 降序插入
                        ASC  -> 升序插入
                        FIFO -> 队列插入，先进先出
                        FILO -> 栈插入，先进后出
        : param node : 要在查找队列中插入的新节点
        : return queue : 插入之后的队列
        """

        if mode == "desc" or mode == "DESC":
            node_f_cost = node[3]

            if len(queue) == 0:
                queue.append(node)

            elif len(queue) == 1:
                if node_f_cost < queue[0][3]:
                    queue.append(node)
                else:
                    queue.insert(0, node)

            elif len(queue) > 1:
                max_i = len(queue) - 1
                min_i = 0

                mid_i = round((max_i + min_i) / 2)

                while max_i - min_i > 1:

                    if queue[mid_i][3] > node_f_cost:
                        min_i = mid_i
                        mid_i = round((max_i + min_i) / 2)
                    elif queue[mid_i][3] < node_f_cost:
                        max_i = mid_i
                        mid_i = round((max_i + min_i) / 2)
                    elif queue[mid_i][3] == node_f_cost:
                        index = mid_i
                        break
                else:
                    index = max_i

                if node_f_cost > queue[0][3]:
                    queue.insert(min_i, node)
                elif node_f_cost < queue[-1][3]:
                    queue.append(node)
                else:
                    queue.insert(index, node)
            return queue

        elif mode == "asc" or mode == "ASC":
            node_f_cost = node[3]

            if len(queue) == 0:
                queue.append(node)

            elif len(queue) == 1:
                if node_f_cost > queue[0][3]:
                    queue.append(node)
                else:
                    queue.insert(0, node)

            elif len(queue) > 1:
                max_i = len(queue) - 1
                min_i = 0

                mid_i = round((max_i + min_i) / 2)

                while max_i - min_i > 1:
                    if queue[mid_i][3] > node_f_cost:
                        max_i = mid_i
                        mid_i = round((max_i + min_i) / 2)
                    elif queue[mid_i][3] < node_f_cost:
                        min_i = mid_i
                        mid_i = round((max_i + min_i) / 2)
                    elif queue[mid_i][3] == node_f_cost:
                        index = mid_i
                        break
                else:
                    index = max_i

                if node_f_cost > queue[-1][3]:
                    queue.append(node)
                elif node_f_cost < queue[0][3]:
                    queue.insert(0, node)
                else:
                    queue.insert(index, node)
            return queue

        elif mode == "fifo" or mode == "FIFO":
            queue.insert(0, node)
            return queue

        elif mode == "filo" or mode == "FILO":
            queue.append(node)
            return queue

    @classmethod
    def drop_node_from_queue(cls, queue, node):
        """
        在查找队列中找到节点名，并删除它和它的全部信息
        : param queue : 查找队列，按照队列的f_cost参数从大到小的顺序存放的节点
                        节点包node的数据结构：
                        list[节点对象, g_cost, h_cost, f_cost, 节点路径(包含路径上全部节点对象)]
        : param node : 要在查找队列中插入的新节点
        : return queue : 插入之后的队列
        """
        
        if len(queue) != 0:
            for i in range(len(queue)):
                # 如果找到这个节点，跳出并依照找到的索引删除它
                node_found = 0
                if queue[i][0].name == node:
                    node_found = 1
                    break
            
            if node_found:
                del queue[i]
            return queue
        else:
            return queue

    @classmethod
    def is_circular_path(cls, path_of_nodename) -> bool:
        """
            识别这个节点的路径是否有环，如果有环则略过这个节点
        : param path_of_nodename : 含有路径上所有节点名的列表
        : return bool : True -> 路径有环；False -> 路径无环
        """
        # 利用集合的不可重复性：如果路径中有重复的节点，则集合的长度必定缩短
        path_length = len(path_of_nodename)
        set_length = len(set(path_of_nodename))

        if path_length != set_length:
            return True
        else:
            return False

    @classmethod
    def get_path_distance(cls, path_of_nodename) -> int or float:
        """
            根据一条路径中的节点名，求得这条路径的总长度
        : param path_of_nodename : 含有路径上所有节点名的列表
        : return distance : 路径的总长度
        """

        distance = 0
        for i in range(len(path_of_nodename)-1):
            edge = cls.get_edge(path_of_nodename[i],path_of_nodename[i+1])
            distance += edge.value
        return distance

    @classmethod
    def get_euclid_distance(self, node_x, node_y, terminal_x, terminal_y):
        """
            Heuristic为当前节点与目标节点的欧几里得距离
        : param node_x : 当前节点的x坐标
        : param node_y : 当前节点的y坐标
        : param terminal_x : 目标节点的x坐标
        : param terminal_y : 目标节点的y坐标
        : param weight : Heuristic的权重，权重逼近正无穷等价于GS搜索，权重为0等价于UFS
        : return euclid_distance : 两节点间的欧几里得距离
        """
        return ((terminal_x-node_x)**2+(terminal_y-node_y)**2)**0.5

    @classmethod
    def get_g_cost(self, prev_cost, new_cost, cost_eq_depth=False):
        if cost_eq_depth == True:
            return prev_cost + 1
        elif cost_eq_depth == False:
            return prev_cost + new_cost