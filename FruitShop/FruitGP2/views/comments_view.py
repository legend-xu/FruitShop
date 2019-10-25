
from rest_framework import viewsets, status
from rest_framework.response import Response

from FruitGP2.authentications import TokenFruitUserAuthentication
from FruitGP2.constants import ORDER_RECEIVED, ORDER_COMMENT, ORDER_ADDCOMMENT
from FruitGP2.models import Comments, Order, GoodsInfo, OrderGoods
from FruitGP2.permissions import LoginPermission
from FruitGP2.serializers import CommentSerializer
from FruitServer.models import Goods


class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = TokenFruitUserAuthentication,
    permission_classes = LoginPermission,
    def handle_post(self,request,*args,**kwargs):
        action=request.query_params.get("action")
        if action == "docomment":
            return self.do_comment(request)
        elif action == "addcomment":
            return self.addcom(request)
        else:
            return self.Unknowaction()

    def Unknowaction(self):
        data = {
            "msg": "notfound",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data)

    def do_comment(self, request):
        comment=request.data.get("comment")
        goods_id=request.data.get("goods_id")
        good=Goods.objects.filter(id=goods_id)
        order_id=request.data.get("order_id")
        order=Order.objects.filter(id=order_id)
        if not order.exists():
            data={
                "msg":"not exists order",
                "Status":status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        order=order.first()
        ordergoods=order.ordergoods_set.all()

        if not good.exists():
            data={
                    "msg":"goods not exists",
                    "status":status.HTTP_404_NOT_FOUND
                }
            return Response(data)

        if order.o_status != ORDER_RECEIVED:#未评价的订单
            data={
                "msg":"no need commented",
                "status":status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        comment_good = []  # 订单未评价的商品列表
        for ordergood in ordergoods:
            comment_good.append(ordergood.goodsinfo.g_name)  # 订单未评价的商品
        goods = good.first()
        if goods.g_name not in comment_good:
           data={
               "msg":"no need content",
               "status":status.HTTP_400_BAD_REQUEST
           }
           return Response(data)
        c = Comments()
        c.c_content = comment
        c.c_goods = goods
        c.c_user = request.user
        c.save()
        comment_good.remove(goods.g_name)  # 列表删除该商品
        if len(comment_good) == 0:  # 如果列表为空，说明全部评价完成
            order.o_status = ORDER_COMMENT
            order.save()
            data = {
                "msg": "have commented ok",
                "Status": status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        data = {
            "msg": "comment ok",
            "Status": status.HTTP_201_CREATED
        }
        return Response(data)

    def addcom(self, request):
        order_id=request.data.get("order_id")
        order=Order.objects.filter(o_user=request.user).filter(id=order_id)
        comment = request.data.get("comment")#追加的评论
        goods_id = request.data.get("goods_id")
        good=Goods.objects.filter(id=goods_id).first()
        if not order.exists():
            data={
                "msg":"no this order",
                "status":status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        order=order.first()
        if not order.o_status==ORDER_COMMENT:
            data={
                "msg":"dont comment or have commented",
                "status":status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        ordergoods=order.ordergoods_set.all()
        goods_list = []
        for ordergood in ordergoods:#只能评论已买的商品
            goodsinfo=GoodsInfo.objects.filter(g_ordergoods=ordergood).first()
            goods_list.append(goodsinfo.g_name)
        if good.g_name not in goods_list:
            data={
                "msg":"dont comment or dont buy",
                "status":status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        c=Comments.objects.filter(c_user=request.user).filter(c_goods=good).first()
        c.c_content+=comment#追加评论
        c.save()
        order.o_status=ORDER_ADDCOMMENT
        order.save()
        data={
            "msg":"add succeed",
            "status":status.HTTP_200_OK
        }
        return Response(data)
