"""
    关系图的样式
"""
from pyecharts import options as opts

class Style:
    # 双向图中正向连接的样式
    forward_line_style = opts.LineStyleOpts(
                                        width=2,
                                        color="#faa",
                                        curve=0.05,
                                        opacity=0.3
                                        )
    forward_lable_style = opts.LabelOpts(
                                    is_show=True, 
                                    color="#fff", 
                                    position="middle", 
                                    formatter="{c}",
                                    font_size=10,
                                    margin=4
                                    )
    forward_style={
                "linestyle_opts":forward_line_style, 
                "label_opts":forward_lable_style,
                "symbol":['none', 'arrow']
                }
    
    # 双向图中逆向连接的样式
    backward_line_style = opts.LineStyleOpts(
                                        width=2,
                                        color="#aaf",
                                        curve=0.05,
                                        opacity=0.3
                                        )
    backward_lable_style = opts.LabelOpts(
                                        is_show=False, 
                                        color="#fff", 
                                        position="middle", 
                                        formatter="{c}",
                                        font_size=10,
                                        margin=4
                                        )
    backward_style={
                "linestyle_opts":backward_line_style, 
                "label_opts":backward_lable_style,
                "symbol":['none', 'arrow']
                }
    
    # 起点节点的样式

    # 起点连线的样式

    # 第n层

    # PyEcharts渲染选项
    render_opts = dict(
                    # 结点分类的类目，结点可以指定分类，也可以不指定。
                    categories=None, 
                    # 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。默认为 True
                    is_focusnode=True, 
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
                    symbol="circle",
                    symbol_size = 15,
                    # edge_symbol=['none', 'arrow'],
                    edge_symbol_size=10,

                    # linestyle_opts={"color":"#f00", "curveness":0.2}
                    
                    )

    # PyEcharts全局选项
    init_opts = opts.InitOpts(
                        #设置动画
                        animation_opts=opts.AnimationOpts(animation_delay=1000, animation_easing="elasticOut"),
                        #设置宽度、高度
                        width='400px',
                        height='400px', 
                        page_title="Romania",
                        theme="dark",
                        js_host="./assets/"
                        )