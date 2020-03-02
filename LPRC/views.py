import json

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

# Create your views here.

# 剩余停车位
from user.models import NumberCar, Car
from wx.models import Licenseplate


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
# def orders(request):
#     if request.method == 'GET':
#         return JsonResponse({'code': 200})
#     if request.method == 'POST':
#         data = request.body
#         data_obj = json.loads(data)
#         id = data_obj.get('id')
#         plate = Licenseplate.objects.filter(user_id=id)
#         stop_car=[]
#         for i in plate:
#             plate_num = i.license
#             car = Car.objects.filter(plate_number=plate_num, out_date__isnull=True)
#             if car:
#                 stop_car.append({'plate':car[0].plate_number,'time':car[0].in_date,'emter':car[0].enter_info})
#         if stop_car:
#             return JsonResponse({'code': 200, 'message': stop_car})
# #查询车辆订单
def payOrders(request):
    if request.method == 'GET':
        return JsonResponse({'code': 200})
    if request.method == 'POST':
        data = request.body
        data_obj = json.loads(data)
        platenumber = data_obj.get('plateDigit')
        car = Car.objects.filter(plate_number=platenumber, out_date__isnull=True)
        stop_car=[]
        if car:
            stop_car.append({'plate': car[0].plate_number, 'time': car[0].in_date, 'enter': car[0].enter_info})
            return JsonResponse({'code': 200, 'message': stop_car})
