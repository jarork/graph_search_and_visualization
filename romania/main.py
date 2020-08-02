"""
    树和图结构的Python实现
    作者:Jake Huang
    邮箱:jarork@qq.com
    博客:Jakehuang.com

    如何导入数据：
    1. 把节点和边的数据分别存储到JSON文件中
    2. 节点的JSON数据格式为：
        {
            "Arad": {
                "is_fixed": true,
                "value": 30,
                "x": 20,
                "y": 100
            },
            ...
        }
    3. 边的JSON数据格式为：
        [
            {
                "source": "Oradea",
                "target": "Zerind",
                "value": 71
            },
            ...
        ]
        如果您只写了单向的连接，希望把连接做成双向的，
        那么可以在载入时传递 mirror_edges=True ，将自动生成反向的连接。
    
    4. 关于数据转换：在您导入了所有节点和边之后，将自动对节点名和边的起点终点创建哈希索引。

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

from graph_manager import GraphManager
from style_sheet import Style

if __name__ == "__main__":
    # 使用数据，创建图表
    graph = GraphManager(
                        json_path_nodes="./city_nodes.json",    # 导入节点
                        json_path_edges="./city_edges.json",    # 导入边
                        mirror_edges=True,      # 源数据单向边变为双向
                        animation=True          # 开启动画
                        )

    start, end = "Craiova", "Neamt"

    # result_path, result_cost = graph.a_star(start, end, h_weight=1)
    # result_path, result_cost = graph.ucs(start, end)
    # result_path, result_cost = graph.gs(start, end)
    # result_path, result_cost = graph.bfs(start, end)
    result_path, result_cost = graph.dfs(start, end)

    if result_path == None and result_cost == None:
        print("没有找到到达该节点的路。")
    else:
        print("已从{}到达终点{}！总共路程：{}".format(start, end, result_cost))
        print("所经路径是：{}".format(" -> ".join(result_path)))
    