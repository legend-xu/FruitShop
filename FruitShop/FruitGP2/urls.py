from django.conf.urls import url

from FruitGP2 import views
from FruitGP2.views.comments_view import CommentAPIView

urlpatterns = [
    url(r'^users/$', views.FruitUsersAPIView.as_view(
        actions={
            "post": "handle_post",
            "get":"handle_get"
        }
    )),
    url(r'^cars/',views.CartsAPIView.as_view(
        actions={
            "post":"handle_post"
        }
    )),
    url(r'^orders/',views.OrderAPIView.as_view(
        actions={
            "post":"handle_post"
        }
    )),
    # url(r'^alipay/',views.pay_ali),
    url(r'^comments/',CommentAPIView.as_view(
        actions={
            "post":"handle_post"
        }
    )),
    # url(r'^users/(?P<pk>\d+)/', views.FruitUsersAPIView.as_view(
    #     actions={
    #
    #     }
    # )),
]