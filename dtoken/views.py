import json

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


from wx.models import UserProfile
import jwt
import time
from django.conf import settings


# Create your views here.
def tokens(request):
    # 登录
    if not request.method == 'POST':
        result = {'code': '10201', 'error': 'Please use POST'}
        return JsonResponse(result)

    data = request.body

    json_obj = json.loads(data)
    username = json_obj.get('username')
    password = json_obj.get('passwd')
    # TODO 检查参数是否存在

    # 查询用户
    user = UserProfile.objects.filter(usercount=username)
    if not user:
        result = {'code': 10202, 'error': 'username or password is wrong'}
        return JsonResponse(result)

    user = user[0]
    import hashlib
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        result = {'code': 10203, 'error': 'username or password is wrong'}
        return JsonResponse(result)
    # 生成token

    token = make_token(user.id)
    if user.openid:
        result = {'code': '200', 'id': user.id, 'token': token.decode(),'openid':user.openid}
    else:
        result = {'code': '200', 'id': user.id, 'token': token.decode()}
    return JsonResponse(result)


def make_token(id, expire=3600 * 24):
    # 注册/登录成功后 签发token 默认一天有效期
    key = settings.JWT_TOKEN_KEY
    now = time.time()

    payload = {'id': id, 'exp': now + expire}
    return jwt.encode(payload, key, algorithm='HS256')




