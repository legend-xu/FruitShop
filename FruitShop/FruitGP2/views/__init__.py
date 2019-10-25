import logging

from django.http import JsonResponse
from alipay import AliPay
from FruitGP2.views.car_view import CartsAPIView
from FruitGP2.views.user_view import FruitUsersAPIView
from FruitGP2.views.order_view import OrderAPIView
from FruitShop.settings import ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY


def learn_log(request):
    logger=logging.getLogger('gp2_learn')
    logger.warning('asasasasas')
    logger.error('sdsdsdsdsd')
    return JsonResponse({
        "msg":"logging"
    })

#
# def pay_ali(request,no,name,price):
#     alipay = AliPay(
#         appid=ALIPAY_APPID,
#         app_notify_url=None,  # 默认回调url
#         app_private_key_string=APP_PRIVATE_KEY,
#         # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#         alipay_public_key_string=ALIPAY_PUBLIC_KEY,
#         sign_type="RSA",  # RSA 或者 RSA2
#         debug = True  # 默认False
#     )
#
#     order_string = alipay.api_alipay_trade_page_pay(
#         out_trade_no=no,#"201910550",
#         total_amount=price,  #10,
#         subject=name,#"华为P301",
#         return_url="http://localhost:8000",
#         notify_url="http://localhost:8000"  # 可选, 不填则使用默认notify url
#     )
#
#     pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
#
#     return pay_url