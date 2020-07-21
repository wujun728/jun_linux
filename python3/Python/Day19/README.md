## 介绍 

找一个好用的画图工具真心不容易，Activiti 工作流自带的 Web 版画图工具，外表挺华丽，其实使用起来各种拧巴；Eclipse 的 Activiti 画图插件，对于相对复杂的流程也是很不友好。

## 环境搭建

| 软件 | 版本  | 功能|   地址|
| ---- | ----- |----- |----- |
|   Python   |  3.7.1 |  脚本语言   | https://www.python.org/  |
|   Django   | 2.1.3 |   Web框架|  https://www.djangoproject.com/ |
|   PyCharm| 2018.2.4 |  可视化开发工具| http://www.jetbrains.com/pycharm/  |
|   BPMN-JS| 3.2.2 |  BPMN前端插件| https://github.com/bpmn-io/bpmn-js |

## 项目截图

![输入图片说明](https://images.gitee.com/uploads/images/2019/0323/121259_41f19adb_87650.png "1.png")

![输入图片说明](https://images.gitee.com/uploads/images/2019/0323/121304_7e6a4833_87650.png "2.png")

![输入图片说明](https://images.gitee.com/uploads/images/2019/0323/121313_37b67c95_87650.jpeg "3.jpg")

![输入图片说明](https://images.gitee.com/uploads/images/2019/0323/121320_203435ab_87650.png "4.png")


## 功能模块

这是一个Python版本，Java版本功能已经基本开发完毕，需要进行功能迁移。

- 用户登录
- 流程列表(CURD)
- 用户注册(待实现)
- 游客访问在线作图，可实现在线导入导出，本地缓存

## 演示

以下是基于 bpmn-js 开发的一个 Activiti 工作流作图管理系统，可以增删查改流程图，系统还在优化中。

游客访问：https://bpmn.52itstyle.vip/