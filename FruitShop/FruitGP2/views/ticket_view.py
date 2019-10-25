from rest_framework import viewsets, status
from rest_framework.response import Response

from FruitGP2.models import Tickets, Order
from FruitGP2.serializers import TicketSerializer


class TicketAPIView(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class =TicketSerializer

    def handle_post(self,request,*args,**kwargs):
        action=request.query_params.get("action")
        if action == "add":
            return self.add(request)
        else:
            return self.Unknowaction()

    def add(self, request):
        price=request.data.get("price")
        order_id=request.data.get("order_id")
        order=Order.objects.filter(id=order_id).first()
        ticket=Tickets()
        ticket.t_user=request.user
        ticket.t_price=price
        ticket.t_order=order#只能给一个订单使用
    def Unknowaction(self):
        data={
            "msg":"not found",
            "status":status.HTTP_404_NOT_FOUND
        }
        return Response(data)