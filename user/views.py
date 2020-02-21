import datetime

import arrow
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from user.models import AdminProfile, NumberCar, Car


def login(request):
    # 登录
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST['username']  # 获取表单内输入的用户名
        print(username)
        password = request.POST['password']  # 获取表单内输入的密  码
        print(password)
        # TODO 检查参数是否存在

        # 查询用户
        user = AdminProfile.objects.filter(username=username)
        print(user)
        if not user:
            return render(request, 'login.html', {'status': '用户名或密码错误，请重新登陆'})

        user = user[0]
        print(user.password)
        # import hashlib
        # m = hashlib.md5()
        # m.update(password.encode())
        if password != user.password:
            return render(request, 'login.html', {'status': '用户名或密码错误，请重新登陆'})

        # token = make_token(user.id)
        # result = {'code': '200', 'id': user.id, 'token': token.decode()}
        # return JsonResponse(result)
        else:
            request.session['admin'] = username
            request.session['isLogin'] = True
            return redirect('user:index')


# 管理员-首页
def adminIndex(request):
    session_name = request.session.get('admin')  # 从session中获取管理员名字
    # 停车场内当日车辆数量
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    print(now)
    # 停车场当前车辆数量
    carnum = Car.objects.filter(out_date__isnull=True)
    count = len(carnum)
    print(count)
    # 总停车位数
    car = NumberCar.objects.all()
    print(car)
    car = car[0]
    print(car.number)

    empty_number = car.number - count
    ret1 = Car.objects.all().order_by('in_date')
    context = {  # 记录保存传入界面的数据
        'count': count,
        'empty_number': empty_number,
        'session_name': session_name,
        'lists': ret1

    }
    return render(request, 'index.html', context)


# 修改密码
def editpassword(request):
    if request.method == 'GET':
        return render(request, 'passwordEdit.html')

    if request.method == 'POST':
        username = request.POST.get('this_username')
        password = request.POST.get('this_password')
        new_password = request.POST.get('new_password')
        try:
            ret = AdminProfile.objects.get(username=username, password=password)
            AdminProfile.objects.filter(username=username, password=password).update(password=new_password)
            return redirect('login.html')
        except:
            return render(request, 'passwordEdit.html', {"status": "输入的用户名或密码错误"})


# 退出登录
def logout(request):
    return redirect('user:login')


# 车辆管理

# 当日车辆信息
def CarDay(request):
    if request.method == 'GET':
        session_name = request.session.get('admin')
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        ret = Car.objects.filter(in_date__date=now)
        context = {
            'carDayLists': ret,
            'session_name': session_name
        }
        return render(request, 'carDay.html', context)


# 车辆历史查询
def CarHistory(request):
    if request.method == 'GET':
        session_name = request.session.get('admin')
        ret = Car.objects.filter(out_date__isnull=False).order_by('in_date').reverse()
        context = {
            'carHistory': ret,
            'session_name': session_name
        }
        return render(request, 'carHistory.html', context)


# 实时车辆查询
def CarReal(request):
    if request.method == 'GET':
        session_name = request.session.get('admin')
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        local = arrow.now()
        local_zero = local.replace(hour=0, minute=0, second=0)
        today = local_zero.format("YYYY-MM-DD HH:mm:ss")
        ret = Car.objects.filter(Q(out_date__isnull=True) & Q(in_date__lte=now) & Q(in_date__gt=today)).order_by(
            'in_date')
        context = {
            'realLists': ret,
            'session_name': session_name
        }
        return render(request,'carReal.html',context)
