import json

from django.conf import settings
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from dtoken.views import make_token


from wx.models import UserProfile, Licenseplate
import hashlib

dist1 = {}


def register(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})

    if request.method == 'POST':
        data = request.body
        print(data, '->re')
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
        # try:
        #     user = UserProfile.objects.create(username=username, email=email, password=m.hexdigest())
        # except Exception as e:
        #     result = {'code': 10104, 'message': '用户名已存在'}
        #     return JsonResponse(result)
        # token = make_token(username)
        dist1['email'] = email
        dist1['username'] = username
        dist1['passwd'] = passwd

        return JsonResponse({'code': 200})


def getid(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body

        print(data)
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
    if request.method == 'GET':
        return JsonResponse({'code': 'Wxlogin'})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        openid = data_obj.get('openid')
        nickname = data_obj.get('nickname')
        old_user = UserProfile.objects.filter(openid=openid)
        if old_user:
            user = old_user[0]
            token = make_token(user.id)
            return JsonResponse({'code': 200, 'message': '登录成功', 'token': token.decode(), 'id': user.id})
        else:
            user = UserProfile.objects.create(openid=openid, nickname=nickname)
            token = make_token(user.id)
            return JsonResponse({'code': 200, 'message': '登录成功', 'token': token.decode(), 'id': old_user.id})


def reid(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body
        print(data, '->getidr')
        code_obj = json.loads(data)
        code = code_obj.get('wxcode')
        data = get_openid(code)
        return JsonResponse(data)


def wxre(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body
        print(data, '->wxloginre')
        data_obj = json.loads(data)
        openid = data_obj.get('openid')
        nickname = data_obj.get('nickname')
        passwd = dist1['passwd']
        email = dist1['email']
        username = dist1['username']
        old_user = UserProfile.objects.filter(openid=openid)
        m = hashlib.md5()
        m.update(passwd.encode())
        if old_user:
            old_user.update(username=username, password=m.hexdigest(), email=email)
            return JsonResponse({'code': 200, 'message': '注册成功'})
        else:
            user = UserProfile.objects.create(openid=openid, username=username, nickname=nickname,
                                              password=m.hexdigest(),
                                              email=email)
            token = make_token(user.id)
            return JsonResponse({'code': 200, 'token': token.decode(), 'id': user.id, 'message': '注册成功'})


def addcar(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'addcar'})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        id = data_obj.get('id')
        carnumber = data_obj.get('carnum')

        carnumber = ''.join(carnumber)
        car = Licenseplate.objects.filter(license=carnumber)
        if car:
            return JsonResponse({'code': 1111, 'message': '车牌已存在!'})
        else:
            Licenseplate.objects.create(license=carnumber, user_id=id)
            return JsonResponse({'code': 200, 'message': '添加车牌信息成功!'})


def showcar(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'showcar'})
    if request.method == 'POST':
        data = request.body
        print(data)
        data_obj = json.loads(data)
        id = data_obj.get('id')
        print(id)
        # 用户名下是否存在车牌
        user = Licenseplate.objects.filter(user_id=id)
        print(type(user))
        car = []
        if user:
            for i in user:
                car.append(i.license)
            return JsonResponse({'code': 200, 'message': car})
        else:
            return JsonResponse({'code': 200, 'message': '你还未绑定车牌'})
