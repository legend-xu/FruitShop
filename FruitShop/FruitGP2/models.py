from django.contrib.auth.hashers import check_password
from django.db import models

from FruitGP2.constants import ORDER_ORDERED
from FruitServer.models import Goods, GoodsTypeTwo


class FruitUser(models.Model):

    f_name = models.CharField(max_length=32, unique=True)
    f_password = models.CharField(max_length=256)
    f_age = models.IntegerField(default=1)
    # False代表女  True代表男
    f_sex = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    is_forbidden = models.BooleanField(default=False)
    f_email = models.CharField(max_length=64, unique=True)
    f_register_date = models.DateTimeField(auto_now_add=True)
    f_icon = models.CharField(max_length=128, null=True)
    is_activite=models.BooleanField(default=False)
    def verify_password(self, password):
        return check_password(password, self.f_password)


class Cart(models.Model):
    c_user = models.ForeignKey(FruitUser)
    c_goods = models.ForeignKey(Goods)
    c_goods_num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)

class Order(models.Model):
    o_user = models.ForeignKey(FruitUser)
    o_status = models.IntegerField(default=ORDER_ORDERED)
    o_price = models.FloatField(default=0)
    o_order_time = models.DateTimeField(auto_now_add=True)

class OrderGoods(models.Model):
    o_order = models.ForeignKey(Order)
    o_goods_num = models.IntegerField(default=1)


class GoodsInfo(models.Model):
    g_ordergoods = models.OneToOneField(OrderGoods)
    g_name = models.CharField(max_length=64)
    g_price = models.FloatField(default=0)
    g_market_price = models.FloatField(default=0)
    g_unit = models.CharField(max_length=32)
    g_detail = models.TextField()
    g_img = models.CharField(max_length=128)
    g_bar_code = models.CharField(max_length=64)
    g_store_num = models.IntegerField(default=10)

class Comments(models.Model):
    c_content=models.TextField()
    c_user=models.ForeignKey(FruitUser)
    c_goods=models.ForeignKey(Goods)
class Gradememory(models.Model):
    g_grade=models.IntegerField(default=0)
    user=models.ForeignKey(FruitUser)

class Address(models.Model):
    a_user=models.ForeignKey(FruitUser)
    p_adds = models.CharField(max_length=100)

class OrderAddress(models.Model):
    o_adress=models.OneToOneField(Order)
    p_add=models.CharField(max_length=100)


class Tickets(models.Model):
    t_user=models.ForeignKey(FruitUser)
    t_order=models.OneToOneField(Order)
    t_price=models.IntegerField(default=10)
