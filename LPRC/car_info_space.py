# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/2/24，15:11
#车辆入库,出库
import os
from hyperlpr import pipline as pp
import smtplib
from email.mime.text import  MIMEText
from email.mime.image import  MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.header import Header

import pymysql
import cv2
import time
import datetime

# 原生数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='123456',
                     database='wxpark',
                     charset='utf8')
# 生成游标对象(操作数据库,执行sql语句)
cur = db.cursor()
userId=1
sql = "select nickname,username from user_profile where id='%d';" % userId
cur.execute(sql)
print(cur.fetchone())