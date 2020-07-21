#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/25 15:49
# @Author  : 王志鹏
# @Site    : 820398513@qq.com
# @File    : d3.py
# @Software: PyCharm
import os
import re
import sys
import json
import xlrd
import xlwt
import MySQLdb
import datetime
import requests
import tempfile
import traceback
import xlutils.copy


class Util:
    def openDBConnect(self, host='', username='', password='', charset=''):
        self.dbconn = MySQLdb.connect(host, username, password, charset=charset)

    def getDBCursor(self, host='', username='', password='', charset=''):

        if not self.dbconn:
            self.openDBConnect(host, username, password, charset)

        self.cursor = self.dbconn.cursor()

    def commit(self):
        self.dbconn and self.dbconn.commit()

    def closeDBConnect(self):
        if self.dbconn:
            self.dbconn.close()
            self.dbconn = None

    # @功能创建文件夹
    # @path:文件夹路径
    def mkdir(self, path):
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)

    # @功能：封装post方式 并支持上传文件
    # @url:请求地址 ,@param_dict:参数 , @param_header:请求头 ,@文件地址
    # @paramType:指传入参数类型，可以是form-data、x-www-form-urlencode、json
    #
    def post(self, url, param_dict, param_header, filePath='', param_type='x-www-form-urlencode'):

        if param_type == "x-www-form-urlencode":
            params = param_dict
        elif param_type == 'json':
            params = json.dumps(param_dict)

        if filePath == "":
            ret = requests.post(url, data=params, headers=param_header)
        else:

            fileName = os.path.basename(filePath)
            extensionName = os.path.splitext(fileName)[1]

            files = {'strutsUploads': (extensionName, open(filePath, 'rb'), {"name": "strutsUploads"})}

            ret = requests.post(url, data=params, headers=param_header, files=files)

        return ret

    # @功能：上传文件
    # @filePath:文件路径，@url:请求地址 ,@param_dict:附加参数
    def uploudFile(self, filePath, url="", param_dict={}):

        if url == "":
            return

        if filePath == None and filePath == "":
            return

        param_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}

        res = self.post(url, param_dict, param_header, filePath)

        path = res.json()
        path = path["resUrl"]

        return path

    # @功能：下载文件
    # @url:请求地址 ,@path:文件路径(文件服务器中的路径 例:group1/M00/16/24/xxxxxxx.xls)
    # @return filePath: 下载后的文件路径
    def downLoadFile(self, url, path):
        # Example:
        # url  ip + xxx.xls
        # path xxx.xls 获取文件名使用
        if path == None and path == "":
            return

        html = requests.get(url)

        fileName = os.path.basename(path)

        tempPath = tempfile.gettempdir()
        filePath = tempPath + "/" + fileName

        with open(filePath, 'wb') as f:
            f.write(html.content)

        return filePath

    # @功能：删除文件
    # @path:文件路径
    def delFile(self, path):
        if os.path.isfile(path):
            os.remove(path)

    # @功能：删除文件
    # @pthost:请求地址, @pid: plan表主键, @param: 更新参数
    def updataSchedule(self, pthost, pid, param):

        modernFilePath = os.path.realpath(__file__)
        configPath = "%s/%s" % (os.path.dirname(modernFilePath), "config.json")

        config = json.load(open(configPath))
        authenticationValue = config.get("authentication")

        param[u"plan.pid"] = pid
        param[u"authentication"] = authenticationValue
        url = u"%s/updatePlanForAdvance.do" % pthost
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}

        self.post(url, param, header)

    # @功能：创建表格文件
    # @sheetName:sheet名称
    # @return workbook, sheet : 表格文件,sheet页
    # 注:未保存时不会生成本地文件!
    def createWorkbook(self, sheetName):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(sheetName, cell_overwrite_ok=True)

        return workbook, sheet

    # @功能：保存表格
    # @filePaths:文件路径, @workbook:表格文件
    def saveWorkbook(self, filePaths, workbook):

        filePath = os.path.dirname(filePaths)
        self.mkdir(filePath)

        workbook.save(filePaths)

    # @功能：表格写入数据
    # @sheet:sheet页, @row:行坐标, @col:列坐标,@value:写入内容 ,@css(int)(可以为空):颜色
    def writeWorkbook(self, sheet, row, col, value, css=None):
        if css != None:

            patterns = xlwt.Pattern()
            patterns.pattern = xlwt.Pattern.SOLID_PATTERN
            patterns.pattern_fore_colour = css
            styles = xlwt.XFStyle()
            styles.pattern = patterns

            sheet.write(row, col, value, styles)
        else:
            sheet.write(row, col, value)

    # @功能：打开表格(读取)
    # @ filePath:表格文件路径, @sheetsNum:sheet页
    # @ return book, sheet : 表格文件, sheet页
    def openWorkbook(self, filePath, sheetsNum=0):
        book = xlrd.open_workbook(filePath, formatting_info=True)
        sheet = book.sheets()[sheetsNum]

        return book, sheet

    # @功能：功能创建表头
    # @sheet:sheet页, @tableHeadList: 表头列表,例 tableHeadList=["a","b"] @:num:行数
    # 支持按行写入数据
    def createTableHead(self, sheet, tableHeadList, num=0):

        count = 0
        for v in tableHeadList:
            tableName = u"%s" % v
            self.writeWorkbook(sheet, num, count, tableName)
            count += 1

    # @功能：查询count
    # @sql:要查询的sql
    # return data[0][0] : 个数
    def count(self, sql):

        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        return data[0][0]

    # @功能：分页
    # @sql: 查询的sql, @nowPage:当前页, @size:容量,默认每次拿200条
    # return data : 返回查询结果
    # 注:传入sql 中不能出现 ";" 号
    def page(self, sql, nowPage, size=200):

        nowPage = (nowPage - 1) * size

        limtStr = """limit %s,%s; """ % (nowPage, size)
        pageSql = sql + limtStr

        self.cursor.execute(pageSql)
        data = self.cursor.fetchall()

        return data

    # @功能：文件创建并追加写入
    # @path: 文件路径 @srts:写入内容
    def writeFile(self, path, srts):

        with open(path, 'ab+') as f:
            srts = u"%s " % srts
            f.write(srts.encode("utf-8"))
            f.write("\n")

    # @功能: 去除字符串中换行空格等
    # return strs: 返回处理后的字符串
    def delspace(self, strs):
        strs = strs.replace(u" ", u"")
        strs = strs.replace(u"\n", u"")
        strs = strs.replace(u"\t", u"")
        strs = strs.replace(u"\r", u"")
        return strs

    # @功能,返回当前时间, 格式为 %Y-%m-%d %H:%M:%S
    def nowTime(self):
        nowTime = datetime.datetime.now()
        strNowTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
        return strNowTime

    # @功能: 错误回调,并更新状态
    # @pid: plan表主键, @host:请求地址,@media:媒体服务地址 ,@err:错误信息, @flag=True: 控制是否跟新为失败,默认是
    def errCall(self, pid, host, media, err=None, flag=True):

        reload(sys)
        sys.setdefaultencoding('utf8')

        tempPath = tempfile.gettempdir()
        errPath = tempPath + "/err.log"

        if err != None:
            errs = u"%s" % err
            self.writeFile(errPath, self.nowTime() + errs)
            self.writeFile(errPath, self.nowTime() + u"\n" + traceback.format_exc())

        if flag:
            url = media + u"uploadOther.do"
            infofilepath = self.uploudFile(errPath, url)

            paln = {u"plan.status": 3}
            paln[u"plan.info"] = u"执行出现严重错误,详情请查看错误日志!"
            paln[u"plan.infoFilepath"] = infofilepath
            self.updataSchedule(host, pid, paln)

    # @功能 按行读取表格文件数据
    # @filePath: 文件地址, @sheetsNum:sheet页 类型:int
    # @return rowsList : 文件数据集 rowsList=[(行数据),(行数据)]
    def readFilesByline(self, filePath, sheetsNum):
        param = self.openWorkbook(filePath, sheetsNum)
        sheet = param[1]
        num_rows = sheet.nrows

        rowsList = []

        for i in range(0, num_rows):
            row = sheet.row_values(i)
            rowsList.append(row)

        return rowsList

    # @功能: 批量提交
    # @res : 整理后的数据集 res=["(a,b,c)","(d,f,g)"], @sql:提交sql, @cmt:默认每500条提交一次
    def importCommit(self, res, sql, cmt=50):

        for i in xrange(0, len(res), cmt):
            lists = res[i:i + cmt]

            sqls = ",".join(lists)

            exsql = sql % sqls

            self.cursor.execute(exsql)
            self.commit()

    # @功能:执行查询sql并返回数据
    # @sql: 查询sql
    # @return data
    def executeQuerySQL(self, sql):

        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        return data

    # @功能: 程序结束回调,当log文件存在时,上传错误文件后,更新数据库错infofilepath字段,并删除临时文件,关闭数据库连接
    # @pid: plan表主键, @pthost:请求地址, @media:媒体服务器请求地址 @flag :boolean False 代表出程序出现过错误
    def modelEnd(self, pid, pthost, media, flag=True):

        tempPath = tempfile.gettempdir()
        errPath = tempPath + "/err.log"

        url = media + u"uploadOther.do"
        paln = {}

        if flag:
            paln[u"plan.schedule"] = 100
            paln[u"plan.status"] = 2

        if os.path.isfile(errPath):
            if flag:
                paln[u"plan.info"] = u"部分数据出现异常,详情请查看错误日志!"

            infofilepath = self.uploudFile(errPath, url)
            paln[u"plan.infoFilepath"] = infofilepath

        self.updataSchedule(pthost, pid, paln)

        self.delFile(errPath)

        self.closeDBConnect()

    #@功能字符串正则验证
    #@rule: 正则表达式, @content:内容
    #return boolean
    def paramCheck(self, rule, content):

        pattern = re.compile(rule)
        contents = u"%s" % content
        result = pattern.search(contents)
        if result:
            return True
        else:
            return False

    # @功能时间差判断
    # 是否在num值范围内num默认值:31, 支持传入字符串/时间类型,支持配合任务计划时间段参数中"/"替换为"-"
    # 返回值 boolean:True 在范围内, False 不在
    def controlTime(self, startTime, endTime, num=31):

        if type(startTime) != datetime.datetime:

            if startTime.find(u"/") != -1:
                startTime = startTime.replace("/", "-")
                endTime = endTime.replace("/", "-")

            if len(startTime)==10:
                startTime = "%s 00:00:00" % startTime
                endTime = "%s 23:59:59" % endTime

            startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
            endTime = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

        if endTime - startTime <= datetime.timedelta(days=num):
            return True
        else:
            return False

