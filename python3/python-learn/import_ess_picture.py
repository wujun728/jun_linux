#-*- coding=GBK -*-
import cx_Oracle
import logging
import sys


#global var
con = cx_Oracle.connect('user','passwd','127.0.0.1:1521/dbinstance')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

def modify_pic(con, order_id, id_iccid, pic_data):
    cur = con.cursor()
    photo_clob = cur.var(cx_Oracle.CLOB)
    photo_clob.setvalue(0, pic_data)
    SQL_JOB = ''' UPDATE SMZ_ESS_AUDIT_INFO
                     SET photo = :photo_clob
                   WHERE ECSORDERID = :order_id
                     AND CHECKCUSTID = :id_iccid'''
    try:
        cur.execute(SQL_JOB, {'photo_clob': photo_clob, 'order_id':order_id, 'id_iccid':id_iccid})
    except cx_Oracle.DatabaseError, exc:
        error, = exc.args
        logging.error("插入失败:[%s][%s]", order_id, id_iccid)
        logging.error("Oracle-Error-Code:[%d]", error.code)
        logging.error("Oracle-Error-Message:[%s]", error.message)
        return False
    return True


def parse_file(filename):
    f = open(filename)
    lines = f.readlines()
    count = 0
    for i in range(len(lines)):
        l = lines[i].split(",")
        if len(l) != 3:
            continue
        order_id = l[0]
        id_iccid = l[1]
        pic_data = l[2]

        logging.info(id_iccid)
        modify_pic(con, order_id, id_iccid, pic_data)
        count = count + 1
        
        if i % 100 == 0:
            con.commit()

    con.commit()
    con.close()
    logging.info("文件[%s]共计成功入库[%d]条记录.", filename, count)



def main():
    if len(sys.argv) != 2:
        logging.error("调用格式：python filename")
        sys.exit(-1)
    filename = sys.argv[1].strip()
    logging.info("处理文件:[%s]", filename)
    parse_file(filename)

if __name__ == '__main__':
    main()
