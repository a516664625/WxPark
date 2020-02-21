# -*-coding:utf-8-*- 
# 作者：   51666 
# 当前系统日期时间：2019/12/30，19:56
from django.conf.urls import url

from user import views
app_name = 'user'
urlpatterns = [
    url(r'^login$', views.login,name='login'),
    url(r'^index$', views.adminIndex,name='index'),
    url(r'^editpassword$', views.editpassword,name='edpassword'),
    url(r'^logout$', views.logout,name='logout'),
    url(r'^carday$',views.CarDay,name='carday'),
    url(r'^carhistory$',views.CarHistory,name='carhistory'),
    url(r'^carreal',views.CarReal,name='carreal'),

]
