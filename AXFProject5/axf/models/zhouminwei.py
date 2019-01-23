from django.db import models
from axf.models import User
# 收货地址模型
class ShippingAddress(models.Model):
    linkman = models.CharField(max_length=30)
    area = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    postal = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    telephone = models.CharField(max_length=20)
    remark = models.CharField(max_length=200)
    shiadd = models.ForeignKey(User,on_delete=models.CASCADE)

    class Mete:
        db_table = 'adders'

class Userinfo(models.Model):
    nickname = models.CharField(max_length=100)
    realname = models.CharField(max_length=100)
    qq = models.IntegerField(max_length=30)
    sex = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    cellphone = models.CharField(max_length=20)
    idcard = models.CharField(max_length=30)
    area = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    marital = models.CharField(max_length=10)
    income = models.CharField(max_length=30)
    hobbies = models.CharField(max_length=300)
    info_id = models.ForeignKey(User,on_delete=models.CASCADE)
