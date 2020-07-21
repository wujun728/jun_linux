__author__ = "小柒"
__blog__ = "https://blog.52itstyle.vip/"
import requests
import time
# 导入文件操作库
import os
import re
import bs4
from bs4 import BeautifulSoup
import sys
from util.mysql_DBUtils import mysql


# 写入数据库
def write_db(param):
    try:
        sql = "insert into house (url,listed_price,transaction_cycle,modify_price," \
              "square_metre,unit_price,total_price,age_completion,community_name,completion_date) "
        sql = sql + "VALUES(%(url)s,%(listed_price)s, %(transaction_cycle)s,%(modify_price)s,"
        sql = sql + "%(square_metre)s,%(unit_price)s,%(total_price)s," \
                    "%(age_completion)s,%(community_name)s,%(completion_date)s)"
        mysql.insert(sql, param)
    except Exception as e:
        print(e)


# 主方法
def main():
    # 给请求指定一个请求头来模拟chrome浏览器
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    page_max = 24
    # 爬图地址
    for i in range(1, int(page_max) + 1):
        print("第几页：" + str(i))
        if i == 1:
            house = 'https://qd.lianjia.com/chengjiao/licang/'
        else:
            house = 'https://qd.lianjia.com/chengjiao/licang/pg'+str(i)
        res = requests.get(house, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        li_max = soup.find('ul', class_='listContent').find_all('li')
        for li in li_max:
            try:
                house_param = {}
                # 所在小区
                community = li.find('div', class_='title').text
                community_name = community.split(" ")[0]
                house_param['community_name'] = community_name
                # 成交地址
                title_src = li.find('a').attrs['href']
                house_param['url'] = title_src
                res = requests.get(title_src, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                # --------------------------------------------------------#
                # 成交日期
                completion_date = soup.find('div', class_='house-title').find('span').text
                completion_date = completion_date.split(" ")[0]
                completion_date = completion_date.replace(".", "-")
                house_param['completion_date'] = completion_date
                # 挂牌价格
                listed_price = soup.find('div', class_='msg').find_all('span')[0].find('label').text
                house_param['listed_price'] = listed_price
                # 成交周期
                transaction_cycle = soup.find('div', class_='msg').find_all('span')[1].find('label').text
                house_param['transaction_cycle'] = transaction_cycle
                # 调价次数
                modify_price = soup.find('div', class_='msg').find_all('span')[2].find('label').text
                house_param['modify_price'] = modify_price
                # 建筑面积
                square_metre = soup.find('div', class_='content').find("ul").find_all('li')[2].text
                square_metre = re.findall(r'-?\d+\.?\d*e?-?\d*?', square_metre)[0]
                house_param['square_metre'] = square_metre
                # 总价
                total_price = soup.find('span', class_='dealTotalPrice').find('i').text
                house_param['total_price'] = total_price
                # 单价
                unit_price = soup.find('b').text
                house_param['unit_price'] = unit_price
                # 建筑年代
                age_completion = soup.find('div', class_='content').find("ul").find_all('li')[7].text
                age_completion = re.findall(r'-?\d+\.?\d*e?-?\d*?', age_completion)[0]
                house_param['age_completion'] = age_completion
                write_db(house_param)
            except Exception as e:
                print(e)
        mysql.end("commit")
    mysql.dispose()


if __name__ == '__main__':
    main()




