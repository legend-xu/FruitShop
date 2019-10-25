
from django.shortcuts import render
from rest_framework import viewsets, status, exceptions
# Create your views here.
from rest_framework.response import Response

from FruitServer.goods_sort_rule import sort_rules, PRICE_UP, PRICE_DOWN
from FruitServer.models import GoodsTypeOne
from FruitServer.serializers import TypeOneSerializer


class GoodsTypeAPIView(viewsets.ModelViewSet):
    queryset = GoodsTypeOne.objects.all()
    serializer_class = TypeOneSerializer
    def get_goodstypes(self,request):
        data={
            "msg":"ok",
            "status":status.HTTP_200_OK,
            "types":self.list(request).data,
            "sortrule":sort_rules
        }
        return Response(data)

class GoodsAPIView(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        typeone=self.request.query_params.get("typeone")
        typetwo = self.request.query_params.get("typetwo")
        sortrule = self.request.query_params.get("sortrule")
        if not typeone:
            raise exceptions.APIException(detail="请提供正确的参数")
        queryset=queryset.filter(g_type_g_one_id=typeone)
        if typetwo:
            queryset=queryset.filter(g_type_id=typetwo)
        if sortrule ==PRICE_UP:
            queryset=queryset.order_by("g_price")
        elif sortrule ==PRICE_DOWN:
            queryset=queryset.order_by("-g_price")
        return queryset