# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2020/1/7，20:49
from django.conf.urls import url

from dtoken import views

urlpatterns = [
    # url(r'login', views.login),
    url(r'tokens', views.tokens)
]