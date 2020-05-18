import datetime
import json
import re

from django.conf import settings
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from dtoken.views import make_token
from user.models import Car

from wx.models import UserProfile, Licenseplate, Suggestions
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
        old_user = UserProfile.objects.filter(usercount=username)
        if old_user:
            result = {'code': 10102, 'message': '用户名已存在'}
            return JsonResponse(result)
        elif passwd != passwd2:
            result = {'code': 10103, 'message': '两次输入密码不一致'}
            return JsonResponse(result)
        m = hashlib.md5()
        m.update(passwd.encode())
        try:
            user = UserProfile.objects.create(usercount=username, email=email, password=m.hexdigest())
        except Exception as e:
            result = {'code': 10104, 'message': '用户名已存在'}
            return JsonResponse(result)
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
            return JsonResponse({'code': 200, 'message': '登录成功', 'token': token.decode(), 'id': old_user[0].id,'openid':user.openid})
        else:
            user = UserProfile.objects.create(openid=openid, nickname=nickname)
            token = make_token(user.id)
            return JsonResponse({'code': 200, 'message': '登录成功', 'token': token.decode(), 'id': user.id,'openid':user.openid})

def Bindwx(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'bindwx'})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        openid = data_obj.get('openid')
        nickname = data_obj.get('nickname')
        id=data_obj.get('id')
        user=UserProfile.objects.filter(id=id)
        if user:
            user.update(nickname=nickname,openid=openid)
            return JsonResponse({'code': 200, 'openid': user[0].openid})
        else:
            return JsonResponse({'code': 201, 'message': '绑定失败'})
# 绑定账号
def Bindcount(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'bindwx'})
    if request.method == 'POST':
        data = request.body
        json_obj = json.loads(data)
        username = json_obj.get('username')
        password = json_obj.get('passwd')
        id=json_obj.get('id')
        user = UserProfile.objects.filter(usercount=username)
        if user:
            return JsonResponse({'code':'201',})

        import hashlib
        m = hashlib.md5()
        m.update(password.encode())
        user_old = UserProfile.objects.filter(id=id)
        user_old.update(password=m.hexdigest(),usercount=username)
        result = {'code': '200'}
        return JsonResponse(result)

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


# 显示车牌
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
                car.append({'id': i.id, 'name': i.license, 'txtStyle': ''})
            return JsonResponse({'code': 200, 'message': car})
        else:
            return JsonResponse({'code': 200, 'message': '你还未绑定车牌'})


# 删除车牌
def delCar(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'showcar'})
    if request.method == 'POST':
        data = request.body
        print("******")
        print(data)
        data_obj = json.loads(data)
        user_id = data_obj.get('user_id')
        print("******")
        print(user_id)
        car_id = data_obj.get('id')
        print(car_id)
        Licenseplate.objects.filter(id=car_id, user_id=user_id).delete()
        return JsonResponse({'code': 200})


# 绑定邮箱
def bindEmail(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'bindemail'})
    if request.method == 'POST':
        data = request.body
        print(data)
        data_obj = json.loads(data)
        id = data_obj.get('user_id')
        email = data_obj.get('email')
        if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',email):
            return JsonResponse({'code': 102, 'message': '请输入正确的邮箱格式'})
        user = UserProfile.objects.filter(id=id)
        old_user = user[0]
        if old_user.email:
            user.update(email=email)
            return JsonResponse({'code': 200, 'message': '邮箱更改成功'})
        else:
            user.update(email=email)
            return JsonResponse({'code': 200, 'message': '绑定成功'})


# 提交建议
def submitSuggest(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'submitSuggest'})
    if request.method == 'POST':
        data = request.body
        print(data)
        data_obj = json.loads(data)
        suggest = data_obj.get('suggest')
        id = data_obj.get('id')
        Suggestions.objects.create(suggest=suggest, user_id=id)
        return JsonResponse({'code': 200})

# 查看历史停车记录
def History(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'history'})
    if request.method == 'POST':
        data = request.body
        print(data)
        data_obj = json.loads(data)
        date = data_obj.get('time')
        print(date)
        print(type(date))
        id = data_obj.get('id')
        plate = Licenseplate.objects.filter(user_id=id)
        # now = datetime.datetime.now().strftime('%Y-%m-%d')
        history_car = []
        if plate:
            for i in plate:
                plate_num = i.license
                car = Car.objects.filter(plate_number=plate_num,in_date__date=date, out_date__isnull=False)
                print(car)
                if car:
                    history_car.append({'car_number':car[0].plate_number,'car_money':car[0].money,'exit_info':car[0].enter_info,'paytime':car[0].out_date,'stop_time':car[0].stay_date})
            return JsonResponse({'code':200,'history':history_car})
        else:
            return JsonResponse({'code':201})
#钱包功能
def Walletm(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'wallet'})
    if request.method == 'POST':
        data = request.body
        print(data)
        data_obj = json.loads(data)
        id = data_obj.get('id')
        print(id)
        user=UserProfile.objects.filter(id=id)
        if user:
            money=user[0].wallet
            print(money)
            return JsonResponse({'code': 200, 'message': money})
        return JsonResponse({'code':'201','message':'error'})

#余额充值
import decimal
def Recharge(request):
    if request.method == 'GET':
        return JsonResponse({'code': 'wallet'})
    if request.method == 'POST':
        data = request.body
        print(data)
        data_obj = json.loads(data)
        id = data_obj.get('id')
        my=data_obj.get('money')
        print(my)
        my=decimal.Decimal(my)
        print(type(my))
        print(id)
        user = UserProfile.objects.filter(id=id)
        if user:
            money = user[0].wallet
            money+=my
            user.update(wallet=money)
            return JsonResponse({'code': 200, 'message': money})
        return JsonResponse({'code': '201', 'message': 'error'})



        


