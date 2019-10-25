import datetime

from alipay import AliPay
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from FruitGP2.authentications import TokenFruitUserAuthentication
from FruitGP2.constants import ORDER_PAYED, ORDER_RECEIVED, ORDER_SEND, ORDER_COMMENT, ORDER_RETURN, ORDER_ORDERED
from FruitGP2.models import Order, Cart, OrderGoods, GoodsInfo, Gradememory, Address, OrderAddress
from FruitGP2.permissions import LoginPermission
from FruitGP2.serializers import OrderSerializer
from FruitGP2.utils import get_total_price
# from FruitGP2.views import pay_ali
from FruitShop.settings import ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY


def pay_ali(request,no,name,price):
    alipay = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA",  # RSA 或者 RSA2
        debug = True  # 默认False
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=no,#"201910550",
        total_amount=price,  #10,
        subject=name,#"华为P301",
        return_url="http://localhost:8000/fruit/orders/?token=d19bc527fa78470c8d17a8b76dd4d96c&action=pay",
        notify_url="http://localhost:8000"  # 可选, 不填则使用默认notify url
    )
    #账号vtpcmc1362@sandbox.com
    pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string

    return pay_url

class OrderAPIView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = TokenFruitUserAuthentication,
    permission_classes = LoginPermission,

    def handle_post(self,request,*args,**kwargs):
        action=request.query_params.get("action")
        if action == "ordered":#下单
            return self.do_ordered(request)
        elif action == "pay":#付款
            return self.pay(request)
        elif action == "ok":#确认年收获
            return self.order_ok(request)
        elif action == "return":
            return self.return_good(request)
        elif action == "address":
            return self.add_address(request)
        else:
            return self.Unknowaction()

    def do_ordered(self, request):#下单并生成订单
        order=Order()
        order.o_user=request.user
        order.o_price=get_total_price(request.user)
        order.save()#下单
        cars=Cart.objects.filter(c_user=request.user).filter(is_select=True)
        if not cars.exists():
            data={
                "msg":"no select",
                "status":status.HTTP_409_CONFLICT
            }
            return Response(data)
        for car in cars:
            ordergoods=OrderGoods()#订单商品
            ordergoods.o_order=order
            ordergoods.o_goods_num=car.c_goods_num
            ordergoods.save()
            goods=car.c_goods
            goodsinfo=GoodsInfo()
            goodsinfo.g_name=goods.g_name
            goodsinfo.g_bar_code=goods.g_bar_code
            goodsinfo.g_detail =goods.g_detail
            goodsinfo.g_img =goods.g_img
            goodsinfo.g_market_price =goods.g_market_price
            goodsinfo.g_price =goods.g_price
            goodsinfo.g_store_num=goods.g_store_num
            goodsinfo.g_unit=goods.g_unit
            goodsinfo.g_ordergoods=ordergoods
            goods.g_store_num =  goods.g_store_num - car.c_goods_num  #下单后库存-1
            goodsinfo.save()#商品详情
            goods.save()
            car.delete()
        data={
                "msg":"success order",
                "status":status.HTTP_201_CREATED
            }
        return Response(data)

    def pay(self,request):
        order_id=request.data.get("order_id")
        order=Order.objects.filter(o_user=request.user).filter(id=order_id)
        add_id=request.data.get("add_id")
        if not order.exists():
            data={
                "msg":"order not exists",
                "status":status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        # ordergoods=OrderGoods.objects.filter(o_order=order).first()
        order=order.first()
        if  order.o_status != ORDER_ORDERED:
            data = {
                "msg": "cant pay",
                "status": status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        ordergoods=order.ordergoods_set.all()
        name=""
        for ordergood in ordergoods:
            good=GoodsInfo.objects.filter(g_ordergoods=ordergood).first()
            name=name+"/"+good.g_name
        pay_url=pay_ali(request,name=name,price=order.o_price,no=str(201910)+str(order.id))#调用支付宝接口并返货url


        grades=Gradememory.objects.filter(user=request.user)#积分
        if not grades.exists():
            grades=Gradememory()
            grades.g_grade=order.o_price/50*10
            grades.user=request.user
            grades.save()
        else:
            grades=grades.first()
            grades.g_grade+=order.o_price/50*10
            grades.save()
        address=Address.objects.filter(a_user=request.user).filter(id=add_id).first()#一个订单对应一个地址，从地址表单里选取

        orderaddress=OrderAddress()
        orderaddress.p_add=address.p_adds
        orderaddress.o_adress=order
        orderaddress.save()
        order.o_status = ORDER_PAYED  # 订单变成已付款
        order.o_order_time = datetime.datetime.now()
        order.save()
        data = {
            "money": order.o_price,
            "url": pay_url,
            "status": status.HTTP_200_OK
        }
        return JsonResponse(data)

    def order_ok(self,request):
        #自己发货的订单
        orders=Order.objects.filter(o_user=request.user).filter(o_status=2)
        order_id=request.data.get("order_id")
        order=Order.objects.filter(o_user=request.user).filter(o_status=2).filter(id=order_id).first()
        if order not in orders:
            data={
                "msg":"order not exists",
                "status":status.HTTP_404_NOT_FOUND
            }
            return Response(data)
        order.o_status = ORDER_RECEIVED#已收货诶评论
        order.save()
        data={
            "msg":"order ok",
            "status":status.HTTP_200_OK
        }
        return Response(data)

    def Unknowaction(self):
        data={
            "msg":"notfound",
            "status":status.HTTP_404_NOT_FOUND
        }
        return Response(data)

    def return_good(self, request):
        order_pay=Order.objects.filter(o_user=request.user).filter(o_status=ORDER_PAYED)
        order_send = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_SEND)
        order_receive = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_RECEIVED)
        order_comment = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_COMMENT)
        order_id=request.data.get("o_id")
        order=Order.objects.filter(o_user=request.user).filter(id=order_id)
        if not order.exists():
            data={
                "msg":"not exists",
                "status":status.HTTP_404_NOT_FOUND
            }
            return Response(data)
        order=order.first()
        for orders  in [order_pay,order_send,order_receive,order_comment]:#如果满足四个状态，均可以退款
            if order not in orders:
                data={
                    "msg":"cant return",
                    "status":status.HTTP_400_BAD_REQUEST
                }
                return Response(data)
            order.o_status = ORDER_RETURN#退款成功
            order.save()
            data={
                "msg":"return ok",
                "status":status.HTTP_200_OK
            }
            return Response(data)

    def add_address(self,request):
        a_address=request.data.get("address")

        address = Address()#新建地址
        address.a_user = request.user
        address.p_adds=a_address
        address.save()
        data={
            "msg":"ok",
            "status":status.HTTP_201_CREATED
        }
        return Response(data)