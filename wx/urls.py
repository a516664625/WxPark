# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2019/12/30，21:12
from django.conf.urls import url

from wx import views

urlpatterns = [
    url(r'Wxlogin', views.Wxlogin),
    url(r'wxre', views.wxre),
    url(r'getid', views.getid),
    url(r'reid', views.reid),
    url(r'register', views.register),
    url(r'addcar', views.addcar),
    url(r'showcar', views.showcar),

]
