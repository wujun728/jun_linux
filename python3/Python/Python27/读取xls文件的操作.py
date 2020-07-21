#!/usr/bin/evn python
# -*- encoding: utf-8 -*-

import xlrd
import xlwt
import xlutils.copy


class Excels:
    def createExcel(self):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(u"sheet页名称", cell_overwrite_ok=True)

        sheet.write(0, 0, u"Name")  # 写入(行,列,内容)
        sheet.write(0, 1, u"age")

        sheet.write(1, 0, u"DanBrown")
        sheet.write(1, 1, u"18")

        workbook.save(u"../导出demo.xls")  # 保存 ./为当前目录 ../上级目录 /所在磁盘根目录

    def readExcel(self):
        paths = u"../导出demo.xls"
        book = xlrd.open_workbook(paths)  # 打开文件
        table = book.sheets()[0]  # 得到第一个sheet页

        row_value = table.row_values(0)  # 获取第一行数据
        col_value = table.col_values(0)  # 获取第一列数据
        value = table.cell(0, 1).value  # 获取指定格子内容

        print row_value
        print col_value
        print value

        def updataExcel(self):
            paths = u"../导出demo.xls"

        book = xlrd.open_workbook(paths)  # 打开文件

        updataBook = xlutils.copy.copy(book)  # 复制
        sheet = updataBook.get_sheet(0)  # 得到第一个sheet页

        sheet.write(1, 1, u"28")  # 将18跟新为28

        sheet.write(2, 0, u"王xx")
        sheet.write(2, 1, u"30")

        updataBook.save(u"../导出demo.xls")

    def mergeCell(self):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(u"sheet页名称", cell_overwrite_ok=True)
        sheet.write_merge(0, 2, 0, 1, '一年一班')
        workbook.save(u"../导出demo.xls")  # 保存 ./为当前目录 ../上级目录 /所在磁盘根目录

        book = xlwt.Workbook()  # 添加一个sheet
        sheet=book.add_sheet('sheet1') #向sheet中添加数据，行、列、value值 #合并单元格，跨行跨列
        sheet.write_merge(0,2,0,1,'一年一班')
        sheet.write(0,2,'小明')
        sheet.write(1,2,'小李')
        sheet.write(2,2,'小二哈')
        book.save('peitest.xls')
    def main(self):
        # 创建一个Excel
        self.createExcel()

        # 读取Excel内容
        self.readExcel()

        # 修改Excel内容
        self.updataExcel()
        #合并单元格
        self.mergeCell()



if __name__ == '__main__':
    excels = Excels()
    excels.main()
