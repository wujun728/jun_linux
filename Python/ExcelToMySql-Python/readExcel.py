import xlrd

def readExcel (tablename:str,filename:str):
    wb = xlrd.open_workbook(filename)  
    table = wb.sheet_by_name(tableName)   # 根据表的名字读取
    nrows = table.nrows
    row=[]
    dict_content = {
        "tableName":"",         # 表名
        "sourceTableName":"",   # 来源表名
        "fields":[],            # 字段
        "updateFields":[]       # key相同时，需要更新的字段
        }
    for i in range(2,nrows):
        row = table.row_values(i)
        if row[2]=="":
            break
        if row[9] != "PK":
            dict_content["updateFields"].append(row[2])
        dict_content["tableName"] = row[1]
        dict_content["sourceTableName"] = row [6]
        dict_content["fields"].append(row[2])
    
    result = "INSERT INTO {tableName}(".format(**dict_content)

    for s in dict_content["fields"]:
        if s =="Update_Date":
            result += s+") SELECT * FROM "+dict_content["sourceTableName"]
        else:
            result += s+","
    
    result += " ON DUPLICATE KEY UPDATE "
    for i in range(0,dict_content["updateFields"].__len__()):
        if i == dict_content["updateFields"].__len__()-1:
            result += dict_content["updateFields"][i]+" = "+dict_content["sourceTableName"]+"."+dict_content["updateFields"][i]
        else:
            result += dict_content["updateFields"][i]+" = "+dict_content["sourceTableName"]+"."+dict_content["updateFields"][i]+","
    return result

tableName = "Country"             # Excel中sheet的名字，注意大小写
filename  = "testExcel.xlsx"      # 读取的Excel文件,这里的文件是同级目录下的testExcel.xlsx

print(readExcel(tableName,filename))