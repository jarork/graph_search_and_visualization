"""
    关系图的样式表
"""
from pyecharts import options as opts

class Style:
    @classmethod
    def make_root(cls, node):
        node.attr.update(cls.ROOT_NODE_STYLE)

    @classmethod
    def make_terminal(cls, node):
        node.attr.update(cls.TERMINAL_NODE_STYLE)

    @classmethod
    def node_searched(cls, node):
        node.attr.update(cls.SEARCHED_NODE_STYLE)

    @classmethod
    def node_current(cls, node):
        node.attr.update(cls.CURRENT_NODE_STYLE)

    @classmethod
    def edge_searched(cls, edge):
        edge.attr.update(cls.SEARCHED_EDGE_STYLE)

    @classmethod
    def edge_current(cls, edge):
        edge.attr.update(cls.CURRENT_EDGE_STYLE)

    # 默认的HTML输出地址
    DEFAULT_HTML_PATH = "./Romania.html"

    # 默认的JS服务器
    DEFAULT_JS_SERVER = "./assets/"

    # PyEcharts渲染选项
    DEFAULT_RENDER_OPTS = dict(
                    # 结点分类的类目，结点可以指定分类，也可以不指定。
                    categories=None, 
                    # 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。默认为 True
                    is_focusnode=False, 
                    # 是否开启鼠标缩放和平移漫游。
                    is_roam=True,
                    # 是否旋转标签，默认为 False
                    is_rotate_label=True, 
                    # 布局类型，默认force=力引导图，circular=环形布局
                    layout="force", 
                    # graph_edge_length=100, # 力布局下边的两个节点之间的距离，这个距离也会受 repulsion 影响。默认为 50，TODO 值越大则长度越长
                    # 点受到的向中心的引力因子。TODO 该值越大节点越往中心点靠拢。默认为 0.2
                    gravity=0.8,
                    # 节点之间的斥力因子。默认为 50，TODO 值越大则斥力越大
                    repulsion=1000, 
                    # edge_label=opts.LabelOpts(
                    #     is_show=True, color="#fff", position="middle", formatter="{c}"
                    # ),
                    symbol="rect",
                    symbol_size = 8,
                    # edge_symbol=['none', 'arrow'],
                    edge_symbol_size=10,

                    # linestyle_opts={"color":"#f00", "curveness":0.2}
                    
                    )

    # PyEcharts全局选项
    DEFAULT_INIT_OPTS = opts.InitOpts(
                        #设置动画
                        animation_opts=opts.AnimationOpts(animation_delay=1000, animation_easing="elasticOut"),
                        #设置宽度、高度
                        width='600px',
                        height='500px', 
                        page_title="Romania",
                        theme="dark",
                        js_host=DEFAULT_JS_SERVER
                        )

    # 双向图中正向连接的样式
    FORWARD_LINE_STYLE = opts.LineStyleOpts(
                                        width=1,
                                        color="#f55",
                                        curve=0,
                                        opacity=0.4
                                        )
    FORWARD_LABLE_STYLE = opts.LabelOpts(
                                    is_show=False, 
                                    color="#55f", 
                                    position="middle", 
                                    formatter="{c}",
                                    font_size=10,
                                    margin=4
                                    )
    FORWARD_STYLE={
                "linestyle_opts":FORWARD_LINE_STYLE, 
                "label_opts":FORWARD_LABLE_STYLE,
                "symbol":['none', 'none']
                }
    
    # 双向图中逆向连接的样式
    BACKWARD_LINE_STYLE = opts.LineStyleOpts(
                                        width=1,
                                        color="#77f",
                                        curve=0,
                                        opacity=0.4
                                        )
    BACKWARD_LABLE_STYLE = opts.LabelOpts(
                                        is_show=False, 
                                        color="#fff", 
                                        position="middle", 
                                        formatter="{c}",
                                        font_size=10,
                                        margin=4
                                        )
    BACKWARD_STYLE={
                "linestyle_opts":BACKWARD_LINE_STYLE, 
                "label_opts":BACKWARD_LABLE_STYLE,
                "symbol":['none', 'none']
                }
    
    # 起点节点的样式
    ROOT_NODE_STYLE = {
        "symbol_size" : 30,
        "symbol" : "triangle"  
    }

    # 目的地节点的样式
    TERMINAL_NODE_STYLE = {
        "symbol_size" : 40,
        "symbol" : "circle"
    }

    # 正在查找的节点的样式
    CURRENT_NODE_STYLE = {
        "symbol_size" : 20,
        "symbol" : "circle"
    }

    # 以查找过的节点的样式
    SEARCHED_NODE_STYLE = {
        "symbol_size" : 15,
        "symbol" : "triangle"
    }

    # 已遍历的边的样式
    SEARCHED_LINE_STYLE = opts.LineStyleOpts(
                                        width=1,
                                        color="#fff",
                                        curve=0,
                                        opacity=0.5
                                        )
    SEARCHED_LABLE_STYLE = opts.LabelOpts(
                                        is_show=True, 
                                        color="#ccc", 
                                        position="middle", 
                                        formatter="{c}",
                                        font_size=10,
                                        margin=4
                                        )
    SEARCHED_EDGE_STYLE = {
                "linestyle_opts":SEARCHED_LINE_STYLE, 
                "label_opts":SEARCHED_LABLE_STYLE,
                "symbol":['none', 'arrow'],
                "symbol_size":5
                }

    # 正在查找的边的样式
    CURRENT_LINE_STYLE = opts.LineStyleOpts(
                                        width=4,
                                        color="#0f0",
                                        curve=0,
                                        opacity=1
                                        )
    CURRENT_LABLE_STYLE = opts.LabelOpts(
                                        is_show=True, 
                                        color="#ccc", 
                                        position="middle", 
                                        formatter="{c}",
                                        font_size=10,
                                        margin=4
                                        )
    CURRENT_EDGE_STYLE = {
                "linestyle_opts":CURRENT_LINE_STYLE, 
                "label_opts":CURRENT_LABLE_STYLE,
                "symbol":['none', 'arrow'],
                "symbol_size":15
                }
