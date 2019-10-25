from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response

from FruitGP2.authentications import TokenFruitUserAuthentication
from FruitGP2.models import Cart
from FruitGP2.permissions import LoginPermission
from FruitGP2.serializers import CartSerializer
from FruitServer.models import Goods


class CartsAPIView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes =TokenFruitUserAuthentication,
    permission_classes =LoginPermission,
    def handle_post(self,request,*args,**kwargs):
        action=request.query_params.get('action')
        if action == "add_car":#添加购物车
            return self.add(request)
        elif action=="all":#全选
            return self.all_select(request)
        elif action== "add_num":#增
            return self.add_num(request)
        elif action == "reducenum":#减
            return self.reduce_num(request)
        elif action == "delete":
            return self.delete(request)
        else:
            return self.Unknowaction()

    def add(self,request):
        good_id=request.data.get("goods_id")
        good_num=request.data.get("goods_num")
        # good_num=int(good_num)
        car=Cart.objects.filter(c_user=request.user).filter(c_goods_id=good_id)
        if not car.exists():
            car=Cart()
            car.c_goods_id=good_id
            goods=Goods.objects.filter(id=good_id).first()
            if good_num <= goods.g_store_num:
                if good_num == 0 :#数量至少为1
                    data={
                        "msg":"least 1",
                        "status":status.HTTP_400_BAD_REQUEST
                    }
                    return Response(data)
                car.c_goods_num=good_num
            else:#数量超过库存
                data={
                    "msg":"too many",
                    "Status":status.HTTP_400_BAD_REQUEST
                }
                return Response(data)
        else:
            car=car.first()
            car.c_goods_num=car.c_goods_num+int(good_num)
        car.c_user=request.user
        car.save()
        data={
            "msg":"successful add",
            "status":status.HTTP_200_OK,
            "data":self.get_serializer(car).data
        }
        return Response(data)
    def all_select(self,request):
        car_all=Cart.objects.filter(c_user=request.user).all()
        #选中
        car_t=Cart.objects.filter(c_user=request.user).filter(is_select=True)
        #未选中
        car_f=Cart.objects.filter(c_user=request.user).filter(is_select=False)
        if not car_all.exists():
            data={
                "msg":"car no goods",
                "status":status.HTTP_400_BAD_REQUEST
            }

        if car_t.exists() and  car_f.exists():#有1个选中的就全选
            for car in car_f:
                car.is_select=True
                car.save()
        elif car_t.exists() and not car_f.exists():#全不选
            for car in car_t:
                car.is_select=False
                car.save()
        elif car_f.exists() and not car_t.exists():#全选
            for car in car_f:
                car.is_select=True
                car.save()
        data={
            "msg":"OK",
            "status":status.HTTP_200_OK
        }
        return Response(data)

    def add_num(self, request):
        g_id = request.data.get("g_id")
        car = Cart.objects.filter(c_user=request.user).filter(c_goods_id=g_id)
        if not car.exists():  # 没有该商品
            data = {
                "msg": "car no this good",
                "status": status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        car = car.first()
        print("+++++++++++++++++++++++++++++++", car)
        goods = car.c_goods
        if car.c_goods_num >= goods.g_store_num:  # 添加量超过库存
            data = {
                "msg": "add failed",
                "status": status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        car.c_goods_num = car.c_goods_num + 1
        # car.c_user=request.user
        car.save()
        data = {
            "msg": "OK",
            "status": status.HTTP_200_OK
        }
        return Response(data)

    def reduce_num(self, request):
        g_id = request.data.get("g_id")
        car = Cart.objects.filter(c_user=request.user).filter(c_goods_id=g_id)
        if not car.exists():  # 没有该商品
            data = {
                "msg": "car no this good",
                "status": status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        car = car.first()
        if car.c_goods_num == 1:#至少有一件
            data={
                "msg":"num cannot = 0",
                "status":status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        car.c_goods_num -= 1
        car.save()
        data = {
            "msg": "OK",
            "status": status.HTTP_200_OK
        }
        return Response(data)
    def delete(self,request):
        cars=Cart.objects.filter(c_user=request.user).filter(is_select=True)
        if not cars.exists():
            data={
                "msg":"not exists",
                "status":status.HTTP_404_NOT_FOUND
            }
            return Response(data)
        for car in cars:
            car.delete()
        data={
            "msg":"delete succeed",
            "status":status.HTTP_200_OK
        }
        return Response(data)
    def Unknowaction(self):
        data={
            "msg":"not found",
            "status":status.HTTP_404_NOT_FOUND
        }
        return Response(data)