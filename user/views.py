import datetime
import json
from django.http import HttpResponse, JsonResponse
import hashlib

from tools.logging_check import login_required
from tools.Email import send_email

from wx.models import UserProfile, Licenseplate

import arrow
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from user.models import AdminProfile, NumberCar, Car, CS


def login(request):
    # 登录
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')  # 获取表单内输入的用户名

        password = request.POST.get('password')  # 获取表单内输入的密码
        # print(type(password))

        # TODO 检查参数是否存在

        # 查询用户
        user = AdminProfile.objects.filter(username=username)

        if not user:
            return render(request, 'login.html', {'status': '用户名或密码错误，请重新登陆'})

        user = user[0]
        if user.stateflag == 0:
            if password != user.password:
                return render(request, 'login.html', {'status': '用户名或密码错误，请重新登陆1'})
            else:
                request.session['admin'] = username
                request.session['isLogin'] = True
                return redirect('user:index')
        else:
            m = hashlib.md5()
            # print(password)
            m.update(password.encode())
            # print(m.hexdigest())
            # print(user.password)
            if m.hexdigest() != user.password:
                return render(request, 'login.html', {'status': '用户名或密码错误，请重新登陆2'})
            else:
                request.session['admin'] = username
                request.session['isLogin'] = True
                return redirect('user:index')


# 管理员-首页
@login_required
def adminIndex(request):
    if request.method == "GET":
        session_name = request.session.get('admin')  # 从session中获取管理员名字
        # 停车场内当日车辆数量
        now = datetime.datetime.now().strftime('%Y-%m-%d')

        # 停车场当前车辆数量
        carnum = Car.objects.filter(out_date__isnull=True)
        count = len(carnum)
        # 总停车位数
        car = NumberCar.objects.all()
        car = car[0]
        empty_number = car.number - count
        # 当日停车人次
        person_num = len(Car.objects.filter(in_date__date=now))
        # 当日费用总额
        money = Car.objects.filter(out_date__date=now)
        moneys = 0
        if money:
            for i in money:
                moneys += i.money
            print(moneys)
        ret1 = Car.objects.all().order_by('in_date')
        context = {  # 记录保存传入界面的数据
            'count': count,
            'empty_number': empty_number,
            'session_name': session_name,
            'lists': ret1,
            'person': person_num,
            'money': moneys
        }
        return render(request, 'index.html', context)


# 修改密码
@login_required
def editpassword(request):
    if request.method == 'GET':
        print(request.session.get('admin'))
        return render(request, 'passwordEdit.html')

    if request.method == 'POST':
        username = request.POST.get('this_username')
        password = request.POST.get('this_password')
        if username != request.session.get('admin'):
            return render(request, 'passwordEdit.html', {"status": "输入的用户名或密码错误hh"})

        new_password = request.POST.get('new_password')

        print(new_password)
        try:
            user = AdminProfile.objects.get(username=username)
            print(user)
            if user.stateflag == 0:
                m = hashlib.md5()
                print(user.stateflag)
                if user.password == password:
                    print(user.password)
                    m.update(new_password.encode())
                    print(m.hexdigest())
                    user.password = m.hexdigest()
                    print(user.password)
                    user.stateflag = 1
                    user.save()
                    print('hha')
                    del request.session['admin']
                    del request.session['isLogin']
                    return redirect('login.html')
                else:
                    return render(request, 'passwordEdit.html', {"status": "输入的用户名或密码错误1"})
            else:
                m = hashlib.md5()
                m.update(password.encode())
                print(m.hexdigest())
                if user.password == m.hexdigest():
                    m = hashlib.md5()
                    m.update(new_password.encode())
                    user.password = m.hexdigest()
                    user.save()
                    del request.session['admin']
                    del request.session['isLogin']
                    return redirect('login.html')
                else:
                    return render(request, 'passwordEdit.html', {"status": "输入的用户名或密码错误2"})
        # try:
        #         ret = AdminProfile.objects.get(username=username, password=password)
        #         AdminProfile.objects.filter(username=username, password=password).update(password=new_password)
        #         return redirect('login.html')
        except Exception as e:
            print(e)
            return render(request, 'passwordEdit.html', {"status": "输入的用户名或密码错误3"})


# 退出登录
@login_required
def logout(request):
    del request.session['admin']
    del request.session['isLogin']
    return redirect('user:login')


# 车辆管理

# 当日车辆信息
@login_required
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
@login_required
def CarHistory(request):
    if request.method == 'GET':
        session_name = request.session.get('admin')
        ret = Car.objects.filter(out_date__isnull=False).order_by('in_date').reverse()
        context = {
            'carHistory': ret,
            'session_name': session_name
        }
        return render(request, 'carHistory.html', context)


# 实时车辆查询24小时
@login_required
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
        return render(request, 'carReal.html', context)


# 收费管理
# 收费标准设定
@login_required
def ChargeStandard(request):
    if request.method == 'GET':
        session_name = request.session.get('admin')
        ret = CS.objects.all()
        ret1 = CS.objects.values('id', 'able')
        print(ret1)
        dict = {}
        for i in ret1:
            dict2 = {i['id']: i['able']}
            dict.update(dict2)
        context = {
            'chargeStandardLists': ret,
            'session_name': session_name,
            'dict': json.dumps(dict)
        }
        return render(request, 'chargeStandard.html', context)


# 是否启用收费标准
@login_required
def toEnable(request):
    if request.method == 'POST':
        cid = request.POST.get('e')
        ables = request.POST.get('able')
        # print(cid, ables)
        if ables == '0':
            CS.objects.filter(id=int(cid)).update(able=0)
        if ables == '1':
            CS.objects.filter(id=int(cid)).update(able=1)
        return HttpResponse()
    else:
        return render(request, 'chargeStandard.html')


# 删除收费标准
@login_required
def del_chargestandard(request):
    if request.method == 'POST':
        cid = request.POST.get('e')
        CS.objects.filter(id=cid).delete()
        return render(request, 'chargeStandard.html')


# 增加收费标准
@login_required
def add_chargestandard(request):
    if request.method == 'POST':
        hourmoney = request.POST.get('hourMoney')
        print(hourmoney)
        sixmoney = request.POST.get('sixMoney')
        aftermoney = request.POST.get('afterMoney')
        ret = CS.objects.create(hour_money=hourmoney, six_money=sixmoney, after_money=aftermoney, able=0)
        if ret != None:
            return redirect('user:chargeStandard')
        else:
            return render(request, 'chargeStandard.html')


# 用户管理
@login_required
def userManage(request):
    if request.method == 'GET':
        session_name = request.session.get('admin')
        ret = UserProfile.objects.all()
        context = {
            'users': ret,
            'session_name': session_name

        }
        return render(request, 'userManage.html', context)


# 删除用户
@login_required
def DeleteUser(request):
    if request.method == 'POST':
        names = request.POST.getlist('name')
        print(names)
        for i in range(len(names)):
            id = names[i]
            UserProfile.objects.filter(id=id).delete()
        return HttpResponse()
    else:
        return render(request, 'userManage.html')


# 查看收费记录
@login_required
def record(request):
    if request.method == 'GET':
        session_name = request.session.get('admin')
        car = Car.objects.filter(out_date__isnull=False)
        context = {
            'recordLists': car,
            'session_name': session_name

        }
        return render(request, 'chargeRecord.html', context)


@login_required
def Qianfei(request):
    if request.method == 'GET':
        session_name = request.session.get('admin')
        car = Car.objects.filter(Q(isout='1') & Q(out_date__isnull=True))
        plate = []
        for i in car:
            info = {}
            info['plate'] = i.plate_number
            info['id'] = i.id
            info['money'] = i.money
            info['stay_time'] = i.stay_date
            info['in_time'] = i.in_date
            plate.append(info)

        context = {
            'info': plate,
            'session_name': session_name

        }
        return render(request, 'Arrearageuser.html', context)


# 邮件提醒用户
@login_required
def Emailremind(request):
    if request.method == 'POST':
        names = request.POST.getlist('name')
        print(names)
        email_list = []
        for i in range(len(names)):
            id = names[i]
            print(id)
            plate_number = Car.objects.filter(id=id)[0]
            print(plate_number.plate_number)
            user_id = Licenseplate.objects.filter(license=plate_number.plate_number)
            print(user_id[0])
            for j in user_id:
                user = UserProfile.objects.filter(id=j.user_id)[0]
                print(user.email)
                email_list.append(user.email)
        send_email(email_list)
        return JsonResponse({'code': 200})
    else:
        return render(request, 'Arrearageuser.html')
