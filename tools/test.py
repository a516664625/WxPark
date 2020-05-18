# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/3/3，15:34
# coding=UTF-8
import datetime
import math

now = datetime.datetime.now().strftime('%Y-%m-%d')
print(now)

import hashlib
m=hashlib.md5()
a='123'
m.update(a.encode())
print(m.hexdigest())
b='456'
m=hashlib.md5()
m.update(b.encode())
print(m.hexdigest())



