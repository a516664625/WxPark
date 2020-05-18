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
    url(r'bindemail', views.bindEmail,name='bindemail'),
    #提交建议 http://127.0.0.1:8000/wx/submit
    url(r'submit', views.submitSuggest,name='submit'),
    #删除车牌http://127.0.0.1:8000/wx/delcar
    url(r'delcar', views.delCar,name='delcar'),
    #查看停车记录http://127.0.0.1:8000/wx/history
    url(r'history', views.History,name='history'),
    #查看钱包余额http://127.0.0.1:8000/wx/wallet
    url(r'wallet', views.Walletm,name='wallet'),
    # 余额充值http://127.0.0.1:8000/wx/wallet
    url(r'recharge', views.Recharge,name='recharge'),
    # 绑定微信http://127.0.0.1:8000/wx/bindwx
    url(r'bindwx', views.Bindwx,name='bindwx'),
    # 绑定账号http://127.0.0.1:8000/wx/bindcount
    url(r'bindcount', views.Bindcount,name='bindcount'),

]
