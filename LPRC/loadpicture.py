# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/2/23，17:35
import os
from hyperlpr import pipline as pp
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
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

smtp = "smtp.qq.com"
pwd = 'nkkiujrruixrcaah'
# 车牌识别
while True:
    cur = db.cursor()
    path = 'car/'
    list = os.listdir(path)
    length = len(list)
    time.sleep(2)
    if length >= 1:
        for i in list:
            filename = path + i
            print(filename)
            image = cv2.imread(filename)
            img, res = pp.SimpleRecognizePlate(image)
            os.remove(filename)
            plate = ''.join(res)
            plate_length=len(plate)
            car_type='燃油'
            if plate_length==7:
                car_type='燃油'
            if plate_length==8:
                car_type='新能源'
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into park_car_info (plate_number,in_date,car_type,enter_info,isout) values(%s,%s,%s,%s,%s) "
            try:
                cur.execute(sql, [plate, now, car_type, '1','0'])
                db.commit()
            except Exception as e:
                print(e)
                # db.rollback()
            sql = "select user_id from license_info where license='%s';" % plate
            cur.execute(sql)
            user = cur.fetchone()
            userId = user[0]
            sql = "select email,nickname from user_profile where id='%d';" % userId
            cur.execute(sql)
            data = cur.fetchone()
            email = data[0]
            username = data[1]
            print(email)
            print(type(email))
            # sql = "select nickname from user_profile where id='%d';" % userId
            # cur.execute(sql)
            # username=cur.fetchone()[0]
            print(username)
            print(type(username))
            cur.close()
            sender_from = '516664625@qq.com'  # 发件人邮箱
            print(sender_from)
            sender_to = email
            title = '智慧停车场信息'
            contents = '尊敬的用户{},您车牌号为{}的车辆已经进入停车场'.format(username, plate)
            try:
                msg = MIMEText(contents, 'plain', 'utf-8')  # 邮件内容
                msg['From'] = Header(sender_from, 'utf-8')
                msg['To'] = Header(sender_to, 'utf-8')
                msg['Subject'] = Header(title, 'utf-8')
                s = smtplib.SMTP_SSL(smtp, 465)
                s.login(sender_from, pwd)
                s.sendmail(sender_from, sender_to, msg.as_string())
                s.quit()
                print('发送成功')
            except Exception as e:
                print(e)
                print('发送失败')

    else:
        print('wait')
