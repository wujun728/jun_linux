import xlrd
import mysql.connector

#读取EXCEL中内容到数据库中
def readExcel (tablename:str,filename:str):
    wb = xlrd.open_workbook(filename)  
    table = wb.sheet_by_name(tableName)   # 根据表的名字读取
    nrows = table.nrows
    fo=[]
    ddl = "create table"+"`"+tableName+"` ("
    keys = []
    # 表格是第3行开始有数据的
    for i in range(2,nrows):
        fo = table.row_values(i)
        # 根据每一行添加字段
        # 如果没有数据，则终止循环
        if fo[2]=="":
            break
        # 添加字段名和类型
        if "DATE" in fo[4]:
            ddl += "`"+fo[2]+"` DATE"
        else:
            ddl += "`"+fo[2]+"` "+fo[4]

        if fo[10] == "NOT NULL":
            ddl +=" "+fo[10]
        if fo[10] =="":
            ddl +=" DEFAULT NULL"

        ddl +=" COMMENT '"+fo[5]+"',"

        if fo[9]=="PK":
            keys.append(fo[2])

    ddl += "PRIMARY KEY ("
    for key in keys:
        if key == "Update_Date":
            ddl+="`"+key+"`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        else:
            ddl+="`"+key+"`,"
    return ddl

def connectFunction(config:dict):
    try:
        cnn = mysql.connector.connect(**config)
        return cnn
    except mysql.connector.Error as e:
        print("数据库连接失败!",str(e))
    else:
        print("数据库已连接")

def creatTable(ddl:str):
    cnn = connectFunction(config)
    cursor = cnn.cursor(buffered = True)
    
    try:
        cursor.execute(ddl)
    except mysql.connector.Error as e:
        print('创建表失败！',str(e))
    finally:
        cursor.close()#关闭标记位
        cnn.close()#关闭数据库链接



tableName = "Country"             # Excel中sheet的名字，注意大小写
filename  = "testExcel.xlsx"      # 读取的Excel文件,这里的文件是同级目录下的testExcel.xlsx
ddl = readExcel(tableName,filename)
print("ddl:",ddl)

config = {
    "host":"127.0.0.1",
    "user":"root",
    "password":"123456",
    "port":"3306",
    "database":"test",  #数据库
    "charset":"utf8"
}

creatTable(ddl)
