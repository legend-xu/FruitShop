from django.contrib import admin

# Register your models here.
from FruitServer.models import GoodsTypeOne, GoodsTypeTwo, Goods


class GoodsTypeOneAdmin(admin.ModelAdmin):
    pass

admin.site.register(GoodsTypeOne,GoodsTypeOneAdmin)

class GoodsTypeTwoAdmin(admin.ModelAdmin):
    pass

admin.site.register(GoodsTypeTwo,GoodsTypeTwoAdmin)

class GoodsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Goods,GoodsAdmin)