from pyecharts import Bar

bar = Bar("我的第一个图表", "我是副标题")

# add()为主要方法，用于添加图表的数据和设置各种配置项
# is_more_utils: 是提供更多的实用小功能
bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90], is_more_utils=True)

# 这个方法只为了打印配置项，方便调试时候使用
# bar.print_echarts_options()

# use_theme是使用主题，dark：黑暗
bar.use_theme('dark')

# 默认将会在根目录下生成一个 render.html 的文件，支持 path 参数，
# 设置文件保存位置，如 render(r"e:\my_first_chart.html")，文件用浏览器打开。
bar.render()


""" 总结步骤
1、实例化一个具体类型的图表对象  chart = FootChart()
2、为图表添加 通用的配置，如主题   cahrt.use_theme()
3、为图表添加特定的配置  chart.gadd_coordinate()
4、添加数据及配置项   chart.add()
5、生成本地文件（html/svg/jpeg/png/pdf/gif）   chart.render()
"""

