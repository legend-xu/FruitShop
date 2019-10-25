
from rest_framework import serializers

from FruitServer.models import GoodsTypeTwo, GoodsTypeOne, Goods


class TypeTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsTypeTwo
        fields=["id","g_name"]


class TypeOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsTypeOne
        fields = ["id", "g_name","goodstypetwos"]

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Goods
        fields="__all__"
