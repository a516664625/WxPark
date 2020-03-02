# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/2/25，18:55
from django.conf.urls import url

from LPRC import views

urlpatterns = [
    # 空余停车位 http://127.0.0.1:8000/LPRC/emptyNum
    url('^emptyNum$', views.empty_car_num, name='emptyNum'),
    # 停车状态 http://127.0.0.1:8000/LPRC/status
    url('^status$', views.statusStop, name='status'),
    # 停车订单 http://127.0.0.1:8000/LPRC/orders
    # url('^orders$', views.orders, name='orders'),
    # 支付 http://127.0.0.1:8000/LPRC/payorders
    url('^payorders$', views.payOrders, name='payorders')

]
