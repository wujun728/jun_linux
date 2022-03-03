import sys

# 日志告警这里有三个参数 %{type} %{path} %{message}
if len(sys.argv) == 4:
    print(sys.argv[0])  # 自身
    print("项目名：{type}, 日志路径 {path}，详细信息 {message}".format(type=sys.argv[1], path=sys.argv[2], message=sys.argv[3]))

