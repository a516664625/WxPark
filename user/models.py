from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class AdminProfile(models.Model):
    username = models.CharField(max_length=11, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    stateflag=models.IntegerField(verbose_name='修改状态',default=0)#0是初始状态未经过修改

    class Meta:
        db_table = 'admin_profile'
        verbose_name='管理员信息'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '用户:%s' % (self.username)


# 停车位总数量
class NumberCar(models.Model):
    number = models.IntegerField(verbose_name='车位数', primary_key=True)

    class Meta:
        db_table = 'Parking_digits'
        verbose_name = '停车场车位'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '车位:%s' % (self.number)


# 停车场内车辆信息
class Car(models.Model):
    plate_number = models.CharField(max_length=20, null=False)  # 车牌号码
    in_date = models.DateTimeField(auto_now_add=True)  # 进入时间
    out_date = models.DateTimeField(null=True)  # 离开时间
    stay_date = models.CharField(max_length=100,null=True)  # 停车时间
    car_type = models.CharField(max_length=20)  # 车辆类型
    enter_info = models.CharField(max_length=20)  # 入口信息
    exit_info = models.CharField(max_length=20, null=True)  # 出口信息
    money = models.DecimalField(max_digits=6, decimal_places=2, null=True,default=None)
    isout=models.CharField(max_length=2,default=0)

    class Meta:
        db_table = 'park_car_info'


# 收费标准表
class CS(models.Model):
    # 一小时内的金额
    hour_money = models.DecimalField(max_digits=5, decimal_places=2)
    # 六小时内的每小时金额
    six_money = models.DecimalField(max_digits=5, decimal_places=2)
    # 大于6小时后的每小时金额
    after_money = models.DecimalField(max_digits=5, decimal_places=2)
    # 是否可用
    able = models.IntegerField()

    class Meta:
        db_table = 'charge_standard'
