from django.conf.urls import url

from FruitServer import views
from FruitServer.views import GoodsTypeAPIView

urlpatterns=[
    url(r'goodstype/',views.GoodsTypeAPIView.as_view(
        actions={
            "get":"get_goodstypes"
        }
    )),
    url(r'goods/',views.GoodsAPIView.as_view(
        actions={
            "get":"list"
        }
    ))
]