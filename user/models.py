from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class AdminProfile(models.Model):
    username = models.CharField(max_length=11, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')

    class Meta:
        db_table = 'admin_profile'

    def __str__(self):
        return 'id:%s username:%s' % (self.id, self.username)


# 停车位总数量
class NumberCar(models.Model):
    number = models.IntegerField(verbose_name='车位数', primary_key=True)

    # car=models.IntegerField(verbose_name='当前车数量',default=0)
    # personnum=models.IntegerField(verbose_name='人数',default=0)

    class Meta:
        db_table = 'Parking_digits'


# 停车场内车辆信息
class Car(models.Model):
    plate_number = models.CharField(max_length=20,null=False)  # 车牌号码
    in_date = models.DateTimeField(auto_now_add=True)  # 进入时间
    out_date = models.DateTimeField(null=True)  # 离开时间
    stay_date = models.IntegerField(null=True)  # 停车时间
    car_type = models.CharField(max_length=20)  # 车辆类型
    enter_info = models.CharField(max_length=20)  # 入口信息
    exit_info = models.CharField(max_length=20, null=True)  # 出口信息

    class Meta:
        db_table = 'park_car_info'
