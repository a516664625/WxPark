from django.db import models


# Create your models here.
class UserProfile(models.Model):
    nickname = models.CharField(max_length=50, verbose_name='用户名')
    openid = models.CharField(max_length=100, verbose_name='openid')
    email = models.EmailField(null=True)
    isStop = models.CharField(max_length=5, default=False)
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return 'id:%s' % (self.id)


class Licenseplate(models.Model):
    license = models.CharField(max_length=20, verbose_name='车牌')
    user = models.ForeignKey(UserProfile)

    class Meta:
        db_table = 'license_info'


class Suggestions(models.Model):
    suggest = models.CharField(max_length=200, verbose_name='建议')
    user = models.ForeignKey(UserProfile)
    class Meta:
        db_table='feed_info'

