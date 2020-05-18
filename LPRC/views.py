import datetime
import json

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from .jsmoney import charge

# Create your views here.

# 剩余停车位
from user.models import NumberCar, Car, CS
from wx.models import Licenseplate, UserProfile


def empty_car_num(request):
    if request.method == 'GET':
        # 总停车位
        all_number = NumberCar.objects.all()
        all_number = all_number[0].number
        # 停车场现有车辆
        carnum = Car.objects.filter(out_date__isnull=True)
        count = len(carnum)
        emptyNum = all_number - count
        return JsonResponse({'code': 200, 'emptyNum': emptyNum})


# 停车状态
def statusStop(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        id = data_obj.get('id')
        plate = Licenseplate.objects.filter(user_id=id)
        stop_car = []
        for i in plate:
            plate_num = i.license
            car = Car.objects.filter(plate_number=plate_num, out_date__isnull=True)
            if car:
                stop_car.append(car[0].plate_number)
        if stop_car:
            stop_car = ''.join(stop_car)
            return JsonResponse({'code': 200, 'message': stop_car})
        else:
            return JsonResponse({'code': '200', 'message': '未停车'})


# 车辆订单
def orders(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        id = data_obj.get('id')
        plate = Licenseplate.objects.filter(user_id=id)
        stop_car = []
        for i in plate:
            plate_num = i.license
            car = Car.objects.filter(plate_number=plate_num, out_date__isnull=True)
            if car:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                nowd = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
                stay_time = (nowd - car[0].in_date).total_seconds()
                stay_time = float(('%.2f' % (stay_time / 3600)))
                money = charge(stay_time)
                stop_car.append(
                    {'id': car[0].id, 'plate': car[0].plate_number, 'time': car[0].in_date, 'enter': car[0].enter_info,
                     'money': money,
                     'stay_time': stay_time})
        if stop_car:
            return JsonResponse({'code': 200, 'message': stop_car})
        else:
            return JsonResponse({'code': 201})


# 查询车辆订单
def payOrders(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        platenumber = data_obj.get('plateDigit')
        car = Car.objects.filter(plate_number=platenumber, out_date__isnull=True)
        stop_car = []
        if car:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nowd = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
            stay_time = (nowd - car[0].in_date).total_seconds()
            stay_time = float(('%.2f' % (stay_time / 3600)))
            print(stay_time)
            money = charge(stay_time)
            print(money)
            stop_car.append(
                {'id': car[0].id, 'plate': car[0].plate_number, 'time': car[0].in_date, 'enter': car[0].enter_info,
                 'money': money,
                 'stay_time': stay_time})
            return JsonResponse({'code': 200, 'message': stop_car})


# 是否已经出停车场
def isOutpark(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        car_id = data_obj.get('id')
        car = Car.objects.filter(id=car_id)
        car1 = car[0]
        if car1.isout == '0':
            # 没有出场
            return JsonResponse({'code': 201})
        elif car1.isout == '1':
            stay_date = float(car1.stay_date)
            print(stay_date)
            money = charge(stay_date)
            print(money)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            car.update(money=money)
            return JsonResponse({'code': 200, 'message': money})


# 确认支付
def pay(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        car_id = data_obj.get('id')
        user_id = data_obj.get('user_id')

        user = UserProfile.objects.filter(id=user_id)
        car = Car.objects.filter(id=car_id)

        if user[0].wallet >= car[0].money:
            # car = Car.objects.filter(id=car_id)
            money = user[0].wallet - car[0].money
            user.update(wallet=money)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            car.update(out_date=now)
            return JsonResponse({'code': 200})
        elif user[0].wallet < car[0].money:
            return JsonResponse({'code': 201})

