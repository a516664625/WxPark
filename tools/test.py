# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/3/3，15:34

# coding=UTF-8
import time
import datetime
import math

# 把字符串转成datetime
# def string_toDatetime(string):
#     return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
#
# def string_toTimestamp(strTime):
#     return time.mktime(string_toDatetime(strTime).timetuple())
#
#
# time_in = "2018-02-01 21:30:00"
# time_out = "2018-02-04 12:40:00"
# time1 =  string_toDatetime(time_in)
# time2 = string_toDatetime(time_out)
# times = time2 - time1
# days = times.days
# hours = days*24 + times.seconds/3600.00
# fee_hours = int(math.ceil(hours))
# fee_hours = fee_hours
# # print hours,fee_hours
# hour1 = time1.hour
# hour2 = time2.hour
# if fee_hours-hours > 0 :
#     hour2 = hour2 +1
# # print "停车时间 " , hour1,hour2 , hours
# if hours>=0.25 :
#     # 大于15分钟
#     fee = 0
#     d_fee = 0
#     n_fee = 0
#     n_fee_days = 0
#     day_i = 0
#     # 计算费用
#     hour_i = hour1
#     for i in range(fee_hours):
#         if  hour_i>=7 and hour_i<22 :
#             d_fee = d_fee + 4
#         if hour_i<7 :
#             n_fee = n_fee + 4
#         if hour_i>=22 :
#             n_fee = n_fee + 4
#         hour_i = hour_i+1
#         if hour_i == 24:
#             hour_i = 0
#         if hour_i == 7 :
#             # 判断过夜费优惠。处理多夜停车
#             if n_fee>0 :
#                 if n_fee >8:
#                     n_fee_days = n_fee_days+8
#                 else:
#                     n_fee_days = n_fee_days+n_fee
#                 n_fee = 0
#
#     # print n_fee_days,d_fee,n_fee
#     if n_fee >8 :
#         n_fee = 8
#     fee = d_fee + n_fee+n_fee_days
#
#     # print time1.hour , time2.hour
#     print "停车%s小时，收费%d小时，日间%d元， 夜间%d元，多夜间%d元，停车费：%d元" %(hours,fee_hours,d_fee, n_fee,n_fee_days,fee)
# else:
#     print "免费"
d1 = datetime.datetime.strptime('2012-03-05 17:25:19', '%Y-%m-%d %H:%M:%S')
print(type(d1))
d2 = datetime.datetime.strptime('2012-03-05 17:40:20', '%Y-%m-%d %H:%M:%S')
d3=datetime.datetime.now()
print(d3)
s = (d2 - d1).total_seconds()
print('*********')
print(s)
print(type(s))
h=('%.2f'%(s/3600))
print(h)
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# now=datetime.datetime.strptime(now,'%Y-%m-%d %H:%M:%S')
print(type(now))

# now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# nowd = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
# stay_time = (nowd - car[0].in_date)
# stay_time = ('%.2f' % (stay_time / 3600))
# money = charge(stay_time)