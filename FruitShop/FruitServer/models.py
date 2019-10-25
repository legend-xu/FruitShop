from django.db import models

# Create your models here.
class GoodsTypeOne(models.Model):
    g_name=models.CharField(max_length=32,unique=True,verbose_name="一级目录")

    def __str__(self):
        return self.g_name
class GoodsTypeTwo(models.Model):
    g_name = models.CharField(max_length=32)
    g_one=models.ForeignKey(GoodsTypeOne,related_name='goodstypetwos')

    def __str__(self):
        return self.g_name
class Goods(models.Model):
    g_name=models.CharField(max_length=64)
    g_price=models.FloatField(default=0)
    g_market_price=models.FloatField(default=0)
    g_unit=models.CharField(max_length=32)
    g_detail=models.TextField()
    g_img=models.CharField(max_length=128)
    g_bar_code=models.CharField(max_length=64)
    g_store_num=models.IntegerField(default=10)
    g_type=models.ForeignKey(GoodsTypeTwo)

    def __str__(self):
        return self.g_name