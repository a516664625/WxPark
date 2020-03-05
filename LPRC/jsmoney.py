# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/3/3，21:42
import pymysql


def charge(saty_time):
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         password='123456',
                         database='wxpark',
                         charset='utf8')
    cur = db.cursor()
    sql = "select hour_money,six_money,after_money from charge_standard where able=1"
    cur.execute(sql)
    price = cur.fetchone()
    hour_money = float(price[0])
    six_money = float(price[1])
    after_money = float(price[2])
    if saty_time<0.25:
        money=0
        return money
    elif 0.25<saty_time<=1:
        money=1*hour_money
        return money
    elif 1<saty_time<=6:
        money=saty_time*six_money
        return money
    else:
        money=(6*six_money)+((saty_time-6)*after_money)
        return money
if __name__ == '__main__':
    res=charge(4.23)
    print(type(res))

