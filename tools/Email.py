# -*-coding:utf-8-*- 
# 作者：   51666
from django.core.mail import send_mail
# 当前系统日期时间：2020/5/19，0:30
def send_email(email):
    print(email)
    subject = '智慧停车场消息'
    message = '尊敬的用户您好,您有一笔智慧停车场的费用未支付,请尽快登陆客户端支付,以免影响您以后的停车'
    send_mail(subject=subject,message=message,from_email='516664625@qq.com',recipient_list=email)