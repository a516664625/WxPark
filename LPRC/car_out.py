# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/2/24，15:11
# 车辆入库,出库
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
while True:
    cur = db.cursor()
    path = 'car_out_img/'
    list = os.listdir(path)
    length = len(list)
    time.sleep(2)
    if length >= 1:
        for i in list:
            filename = path + i
            print(filename)
            image = cv2.imread(filename)
            img, res = pp.SimpleRecognizePlate(image)
            print(res)
            os.remove(filename)
            plate = ''.join(res)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nowd=datetime.datetime.strptime(now,'%Y-%m-%d %H:%M:%S')

            sql = "select in_date from park_car_info where plate_number='%s' and out_date is null;" % plate
            cur.execute(sql)
            indate = cur.fetchone()
            print(indate)
            in_time=indate[0]
            print(in_time)
            print(type(in_time))
            stay_time=(nowd-in_time).total_seconds()
            stay_time=('%.2f'%(stay_time/3600))
            try:
                sql = "UPDATE park_car_info SET isout=1,stay_date='%s',exit_info='%s' where plate_number='%s' and isout=0" % (
                    stay_time,'2', plate)
                cur.execute(sql)
                print('正确')
                db.commit()
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

                sender_from = '516664625@qq.com'  # 发件人邮箱
                print(sender_from)
                sender_to = email
                title = '智慧停车场信息'
                contents = '尊敬的用户{},您车牌号为{}的车辆正在驶离停车场'.format(username, plate)
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
            except Exception as e:
                print('cuowu')
                print(e)
                db.rollback()
            cur.close()

    else:
        print('wait')
db.close()
