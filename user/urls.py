# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2019/12/30，19:56
from django.conf.urls import url

from user import views

urlpatterns=[
    url(r'/',views.login),
]