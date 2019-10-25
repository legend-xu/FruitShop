from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from FruitGP2.models import FruitUser, Cart, Order, OrderGoods, GoodsInfo, Comments, Tickets


class FruitUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password_hash = make_password(validated_data.get("f_password"))
        validated_data["f_password"] = password_hash
        return super().create(validated_data)

    class Meta:
        model = FruitUser
        fields = ["id", "f_name", "f_age", "f_email", "f_sex", "f_register_date", "f_icon"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"
class OrdergoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderGoods
        fields="__all__"

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        mode=GoodsInfo
        fields="__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=["c_content"]
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tickets
        fields=["t_price"]