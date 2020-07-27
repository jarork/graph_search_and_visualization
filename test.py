from pyecharts import Scatter
scatter = Scatter("散点图", "一年的降水量与蒸发量")
#xais_name是设置横坐标名称，这里由于显示问题，还需要将y轴名称与y轴的距离进行设置
scatter.add("降水量与蒸发量的散点分布", data1,data2,xaxis_name="降水量",yaxis_name="蒸发量",
            yaxis_name_gap=40)
scatter.render()