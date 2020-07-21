#!/usr/bin/python
# -*- coding: utf-8 -*-

import cx_Oracle
import os
import sys
import os.path
import smtplib
import email
import mimetypes
import time
import datetime
import base64
import logging

logging.basicConfig(
    filename="debug-mail.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')



os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

class DoEmail:
    cntSendTimes = 0

    def __init__(self):
        '''Initializes the person's data.'''
        self.htmlText = ""

    def __del__(self):
        '''off...'''

    def doMail(self):
        YYYYMMDD = time.strftime("%Y%m%d", time.gmtime())
        #print YYYYMMDD

        now = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        n_days = now - delta #昨天
        #解决跨月显示问题!
        YYYYLM= n_days.strftime('%Y%m')


        authInfo = {}
        authInfo['server'] = '0.0.0.0'
        authInfo['user'] = 'admin@si-tech.com.cn'
        authInfo['password'] = 'passwd'
        fromAdd = 'withfaker@gmail.com'
        toAdd = ["a@gmail.com", "b@gmail.com", "c@gmail.com"]
        subject = u'已出库情况统计[%s]' % YYYYMMDD
        plainText = 'abcd'


        logging.info("开始准备邮件内容")
        begin_time = time.time()
        self.htmlText = ''' <style type="text/css">
            *{
                font: normal 12px '微软雅黑','宋体',serif;
            }
            .table{
                width:100%;
                border: 1px solid #C1DAD7;
            }
            th {
                text-align:left;
            }
            
            td{
                border: 1px solid #C1DAD7;
                background: #fff;
                font-size:11px;
                padding: 6px 6px 6px 12px;
                color: #4f6b72;
            }
            .tr1{
                height: 21px;
                text-align: center;
                font: bold 12px '微软雅黑','宋体',serif;
            }
            .tr1 td{
                border-bottom: none;
                background: #C0D2DA;
                color: #008000;
                font: bold 14px '微软雅黑','宋体',serif;
            }
            .tr2{
               height: 23px;
            }
            .tr2 td{
                border: .5pt solid #C1DAD7;
                border-bottom:none;
            }
            .center{
                text-align: center;
            }
            .tr3{
                height: 22.50pt;
            }
            .tr3 td{
                border-right:.5pt solid #000000;
                border-bottom:.5pt solid #000000;
            }
            .tr4{
                height: 13.50pt;
            }
            .data{
                height:14.25pt;
            }
            .data td{
                height:14.25pt;
                text-align: right;
            }
        </style>
    </head>
    <body>
        <table cellpadding="0" cellspacing="0" style='border-collapse:collapse;'>
            <tr class="tr1">
                <td colspan="10">移动网已出库情况实时统计</td>
            </tr>
            <tr class="tr2">
                <td rowspan="3" class="center">序号</td>
                <td rowspan="3" class="center">分公司</td>
                <td colspan="7" class="center">用户出库情况</td>
                <td rowspan="3" class="center">电话实名制单停</td>
            </tr>
            <tr class="tr3">
                <td colspan="5" class="center">用户真实</td>
                <td colspan="2" class="center">用户不真实</td>
            </tr>
            <tr class="tr4">
                <td>电话核实</td>
                <td>短信核实</td>
                <td>业务办理核实</td>
                <td>行业应用用户</td>
                <td>预销/预拆/</td>
                <td>电话通知</td>
                <td>短信通知</td>
            </tr> '''
        orcl=cx_Oracle.connect('dbcustadm','newyork24','136.24.1.13:1521/crmdb')
        cursor=orcl.cursor()
        sql=''' select * from(SELECT A.REGION_NAME, DECODE(B.CNT, '', 0, B.CNT)  真实电话核实, 
                      DECODE(C.CNT, '', 0, C.CNT)  真实短信核实,
                      DECODE(D.CNT, '', 0, D.CNT)  真实业务办理核实,
                      DECODE(E.CNT, '', 0, E.CNT)  真实行业应用,
                      DECODE(F.CNT, '', 0, F.CNT)  真实预销预拆,
                      DECODE(G.CNT, '', 0, G.CNT)  不真实电话通知,
                      DECODE(H.CNT, '', 0, H.CNT)  不真实短信通知,
                      DECODE(I.CNT, '', 0, I.CNT)  电话实名制单停
  FROM SREGIONCODE A
  LEFT OUTER JOIN (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '电话核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) B
                    ON (A.REGION_CODE = B.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1'  --移动网
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '短信核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) C
                    ON (A.REGION_CODE = C.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '业务办理核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) D
                    ON (A.REGION_CODE = D.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '行业应用')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) E
                    ON (A.REGION_CODE = E.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '预销/预拆/销户')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) F
                    ON (A.REGION_CODE = F.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '不真实' and deal_type = '电话通知')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) G
                    ON (A.REGION_CODE = G.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '不真实' and deal_type = '短信通知')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) H
                    ON (A.REGION_CODE = H.REGION_CODE)
  LEFT OUTER JOIN (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网
                    and exists(select 1 from wrealuseropr x where x.id_no = msg.id_no)
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) I
                    ON (A.REGION_CODE = I.REGION_CODE)
 WHERE A.REGION_CODE <> '99'
 order by a.region_code asc) 
 union
select '总计', sum(x.a),  sum(x.b), sum(x.c), sum(x.d), sum(x.e), sum(x.f), sum(x.g),  sum(x.h) from (
SELECT A.REGION_NAME, DECODE(B.CNT, '', 0, B.CNT)  a, 
                      DECODE(C.CNT, '', 0, C.CNT)  b,
                      DECODE(D.CNT, '', 0, D.CNT)  c,
                      DECODE(E.CNT, '', 0, E.CNT)  d,
                      DECODE(F.CNT, '', 0, F.CNT)  e,
                      DECODE(G.CNT, '', 0, G.CNT)  f,
                      DECODE(H.CNT, '', 0, H.CNT)  g,
                      DECODE(I.CNT, '', 0, I.CNT)  h
  FROM SREGIONCODE A
  LEFT OUTER JOIN (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '电话核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) B
                    ON (A.REGION_CODE = B.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '短信核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) C
                    ON (A.REGION_CODE = C.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '业务办理核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) D
                    ON (A.REGION_CODE = D.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '行业应用')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) E
                    ON (A.REGION_CODE = E.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '预销/预拆/销户')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) F
                    ON (A.REGION_CODE = F.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '不真实' and deal_type = '电话通知')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) G
                    ON (A.REGION_CODE = G.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '不真实' and deal_type = '短信通知')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) H
                    ON (A.REGION_CODE = H.REGION_CODE)
  LEFT OUTER JOIN (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '1' --移动网
                    and exists(select 1 from wrealuseropr x where x.id_no = msg.id_no)
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) I
                    ON (A.REGION_CODE = I.REGION_CODE)
 WHERE A.REGION_CODE <> '99'
 order by a.region_code asc)x '''
        i=1
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
        	self.htmlText = self.htmlText+'''
                    <tr class="data">
                        <td>''' + str(i) + '''</td>
                        <td>''' + str(row[0]) + '''</td>
                        <td>''' + str(row[1]) + '''</td>
                        <td>''' + str(row[2]) + '''</td>
                        <td>''' + str(row[3]) + '''</td>
                        <td>''' + str(row[4]) + '''</td>
                        <td>''' + str(row[5]) + '''</td>
                        <td>''' + str(row[6]) + '''</td>
                        <td>''' + str(row[7]) + '''</td>
                        <td>''' + str(row[8]) + '''</td>
                    </tr>
                '''
                i = i + 1
        self.htmlText = self.htmlText+"</table><br><br>"


        #########################  无线上网卡 ########################
        self.htmlText= self.htmlText + ''' <table cellpadding="0" cellspacing="0" style='border-collapse:collapse;'>
            <tr class="tr1">
                <td colspan="10">无线上网卡已出库情况实时统计</td>
            </tr>
            <tr class="tr2">
                <td rowspan="3" class="center">序号</td>
                <td rowspan="3" class="center">分公司</td>
                <td colspan="7" class="center">用户出库情况</td>
                <td rowspan="3" class="center">电话实名制单停</td>
            </tr>
            <tr class="tr3">
                <td colspan="5" class="center">用户真实</td>
                <td colspan="2" class="center">用户不真实</td>
            </tr>
            <tr class="tr4">
                <td>电话核实</td>
                <td>短信核实</td>
                <td>业务办理核实</td>
                <td>行业应用用户</td>
                <td>预销/预拆/</td>
                <td>电话通知</td>
                <td>短信通知</td>
            </tr> '''
        sql=''' select * from(SELECT A.REGION_NAME, DECODE(B.CNT, '', 0, B.CNT)  真实电话核实, 
                      DECODE(C.CNT, '', 0, C.CNT)  真实短信核实,
                      DECODE(D.CNT, '', 0, D.CNT)  真实业务办理核实,
                      DECODE(E.CNT, '', 0, E.CNT)  真实行业应用,
                      DECODE(F.CNT, '', 0, F.CNT)  真实预销预拆,
                      DECODE(G.CNT, '', 0, G.CNT)  不真实电话通知,
                      DECODE(H.CNT, '', 0, H.CNT)  不真实短信通知,
                      DECODE(I.CNT, '', 0, I.CNT)  电话实名制单停
  FROM SREGIONCODE A
  LEFT OUTER JOIN (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '电话核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) B
                    ON (A.REGION_CODE = B.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2'  --无线上网卡
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '短信核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) C
                    ON (A.REGION_CODE = C.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '业务办理核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) D
                    ON (A.REGION_CODE = D.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '行业应用')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) E
                    ON (A.REGION_CODE = E.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '预销/预拆/销户')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) F
                    ON (A.REGION_CODE = F.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '不真实' and deal_type = '电话通知')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) G
                    ON (A.REGION_CODE = G.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '不真实' and deal_type = '短信通知')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) H
                    ON (A.REGION_CODE = H.REGION_CODE)
  LEFT OUTER JOIN (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡
                    and exists(select 1 from wrealuseropr x where x.id_no = msg.id_no)
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) I
                    ON (A.REGION_CODE = I.REGION_CODE)
 WHERE A.REGION_CODE <> '99'
 order by a.region_code asc) 
 union
select '总计', sum(x.a),  sum(x.b), sum(x.c), sum(x.d), sum(x.e), sum(x.f), sum(x.g),  sum(x.h) from (
SELECT A.REGION_NAME, DECODE(B.CNT, '', 0, B.CNT)  a, 
                      DECODE(C.CNT, '', 0, C.CNT)  b,
                      DECODE(D.CNT, '', 0, D.CNT)  c,
                      DECODE(E.CNT, '', 0, E.CNT)  d,
                      DECODE(F.CNT, '', 0, F.CNT)  e,
                      DECODE(G.CNT, '', 0, G.CNT)  f,
                      DECODE(H.CNT, '', 0, H.CNT)  g,
                      DECODE(I.CNT, '', 0, I.CNT)  h
  FROM SREGIONCODE A
  LEFT OUTER JOIN (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '电话核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) B
                    ON (A.REGION_CODE = B.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '短信核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) C
                    ON (A.REGION_CODE = C.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '业务办理核实')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) D
                    ON (A.REGION_CODE = D.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '行业应用')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) E
                    ON (A.REGION_CODE = E.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '真实' and deal_reason = '预销/预拆/销户')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) F
                    ON (A.REGION_CODE = F.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '不真实' and deal_type = '电话通知')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) G
                    ON (A.REGION_CODE = G.REGION_CODE)
  LEFT OUTER JOIN
                    (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡 
                    and exists(select 1 from drealcustinfo where msg.id_no = id_no and is_real = '不真实' and deal_type = '短信通知')
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) H
                    ON (A.REGION_CODE = H.REGION_CODE)
  LEFT OUTER JOIN (SELECT RE.REGION_CODE, RE.REGION_NAME, COUNT(1) CNT
                     FROM drealcustmsg MSG, SREGIONCODE RE
                    WHERE msg.region_code = re.region_code
                    and back1 = '2' --无线上网卡
                    and exists(select 1 from wrealuseropr x where x.id_no = msg.id_no)
                    GROUP BY RE.REGION_CODE, RE.REGION_NAME
                    ) I
                    ON (A.REGION_CODE = I.REGION_CODE)
 WHERE A.REGION_CODE <> '99'
 order by a.region_code asc)x '''
        i=1
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
        	self.htmlText=self.htmlText+'''
                        <tr class="data">
                        <td>''' + str(i) + '''</td>
                        <td>''' + str(row[0]) + '''</td>
                        <td>''' + str(row[1]) + '''</td>
                        <td>''' + str(row[2]) + '''</td>
                        <td>''' + str(row[3]) + '''</td>
                        <td>''' + str(row[4]) + '''</td>
                        <td>''' + str(row[5]) + '''</td>
                        <td>''' + str(row[6]) + '''</td>
                        <td>''' + str(row[7]) + '''</td>
                        <td>''' + str(row[8]) + '''</td>
                    </tr> '''
                i = i + 1
        self.htmlText=self.htmlText+"</table><br><br>"

        cursor.close()
        orcl.close()
        self.htmlText=self.htmlText+"</table>"

        end_time = time.time()
        logging.info("邮件内容准备完成, 用时%s秒完成", time.strftime("%S", time.gmtime(end_time - begin_time)))

        # 开始发邮件
        logging.info("开始发邮件")
        begin_time = time.time()

        for to in toAdd:
            self.sendEmail(authInfo, fromAdd, to, subject, plainText, self.htmlText)

        end_time = time.time()
        logging.info("邮件发送完成, 用时%s秒完成", time.strftime("%S", time.gmtime(end_time - begin_time)))


    #send email
    def sendEmail(self, authInfo, fromAdd, toAdd, subject, plainText, htmlText):
        server = authInfo.get('server')
        user = authInfo.get('user')
        passwd = authInfo.get('password')

        if not (server and user and passwd) :
                loogging.error("邮件认证信息不完整")
                return False
        # root
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = fromAdd 
        msgRoot['To'] = toAdd
        msgRoot.preamble = 'This is a multi-part message in MIME format.'
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        #HTML
        msgText = MIMEText(htmlText, 'html', 'utf-8')
        msgAlternative.attach(msgText)
        #send email
        try:
            smtp = smtplib.SMTP()
            smtp.set_debuglevel(0)
            smtp.connect(server)
            smtp.docmd('auth login')
            smtp.docmd(base64.b64encode(user))
            smtp.docmd(base64.b64encode(passwd))
            smtp.docmd('mail from:',authInfo['user'])
            smtp.docmd('rcpt to:', toAdd)
            smtp.docmd('data')
            smtp.docmd(msgRoot.as_string()+'\r\n.')
            smtp.quit()
        except Exception, e:
            error, = e.args
            logging.error("发送失败[%d][%s]", e.code, e.message)
            return False
        return True

def main():
    fd = DoEmail()
    fd.doMail()

if __name__ == '__main__':
    main()
