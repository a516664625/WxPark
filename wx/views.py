import json

from django.conf import settings
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from dtoken.views import make_token
from wx.models import UserProfile
import hashlib


def register(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})

    if request.method == 'POST':
        data = request.body
        print(data)
        if not data:
            result = {'code': 10101, 'message': '请输入完整信息'}
            return JsonResponse(result)
        json_obj = json.loads(data)
        email = json_obj.get('email')
        username = json_obj.get('username')
        passwd = json_obj.get('passwd')
        passwd2 = json_obj.get('passwd2')
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10102, 'message': '用户名已存在'}
            return JsonResponse(result)
        elif passwd != passwd2:
            result = {'code': 10103, 'message': '两次输入密码不一致'}
            return JsonResponse(result)
        m = hashlib.md5()
        m.update(passwd.encode())
        try:
            user = UserProfile.objects.create(username=username, email=email, password=m.hexdigest())
        except Exception as e:
            result = {'code': 10104, 'message': '用户名已存在'}
            return JsonResponse(result)
        token = make_token(username)

        return JsonResponse({'code': 200, 'message': '注册成功', 'username': username,
                             'token': token.decode()})


def getid(request):
    if request.method == 'POST':
        data = request.body
        code_obj = json.loads(data)
        code = code_obj.get('wxcode')
        data = get_openid(code)
        return JsonResponse(data)


def get_openid(code):
    url = settings.WX_APP_URI + '?appid=' + settings.WX_APP_ID + '&secret=' + settings.WX_APP_SECRET + '&js_code=' + code + "&grant_type=authorization_code"
    res = requests.get(url)
    try:
        openid = res.json()['openid']
        session_key = res.json()['session_key']
    except KeyError:
        return 'fail'
    else:
        data = {'openid': openid, 'session': session_key}
        return (data)


def Wxlogin(request):
    if request.method == 'POST':
        data = request.body
        data_obj=json.loads(data)
        openid=data_obj.get('openid')

