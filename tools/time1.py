# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/2/20，20:45
import datetime
import arrow

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
utc = arrow.utcnow()
local1=arrow.now()
print(local1)
print(utc)
local=utc.to('local')
print(local)
local_zero=local.replace(hour=0,minute=0,second=0)
print(local_zero)
today = local_zero.format("YYYY-MM-DD HH:mm:ss")
print(today)