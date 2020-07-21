#coding:utf-8
import  pymysql

class MysqlHelper(object):
    config={
        "host":"localhost",
        "user":"root",
        "password":"123456",
        "db":"demo",
        "charset":"utf8"
    }
    def __init__(self):
        self.connection=None
        self.cursor=None

    # 从数据库表中查询一行数据 select count(*) from emp
    def getOne(self,sql,*args):
        try:
            self.connection = pymysql.connect(**MysqlHelper.config)
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql,args)
            return self.cursor.fetchone()
        except Exception as ex:
            print(ex,ex)
        finally:
            self.close()

    # 从数据库表中查询多行数据
    def getList(self,sql,*args):
        try:
            self.connection = pymysql.connect(**MysqlHelper.config)
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql,args)
            return self.cursor.fetchall()
        except Exception as ex:
            print(ex,ex)
        finally:
            self.close()

    # 对数据库进行增，删，改
    def executeDML(self,sql,*args):
        try:
            self.connection = pymysql.connect(**MysqlHelper.config)
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql,args)#  返回 sql语句执行之后影响的行数
            new_id = self.connection.insert_id() # 返回系统刚刚自动生成的id
            self.connection.commit();
            return new_id
        except Exception as ex:
            self.connection.rollback()
            print(ex,ex)
        finally:
            self.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    helper = MysqlHelper()
    print(helper.executeDML("delete from dept where deptno=%s",80))
#     print(helper.executeDML("insert into dept values(%s,%s,%s)","80","admin","beijing"))