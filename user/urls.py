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
    #收费管理设定 http://127.0.0.1:8000/user/chargeStandard
    url(r'^chargeStandard',views.ChargeStandard,name='chargeStandard'),
    #设定是否启用http://127.0.0.1:8000/user/toEnable
    url(r'^toEnable',views.toEnable,name='toEnable'),
    #删除设定http://127.0.0.1:8000/user/delcs
    url(r'^delcs',views.del_chargestandard,name='delcs'),
    #增加收费标准http://127.0.0.1:8000/user/addcs
    url(r'^addcs',views.add_chargestandard,name='addcs'),
    #用户管理http://127.0.0.1:8000/user/userManage
    url(r'^userManage',views.userManage,name='userManage'),
    #删除用户http://127.0.0.1:8000/user/deluser
    url(r'^deluser',views.DeleteUser,name='deluser'),



]
