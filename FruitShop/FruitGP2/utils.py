import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from django.template import loader

from FruitGP2.models import Cart
from FruitShop.settings import EMAIL_HOST_USER


def generate_user_token():
    return uuid.uuid4().hex

def send_active_email(username,to_email):
    subject='FruitShop激活'
    token=generate_user_token()
    cache.set(token,username,60*60*24)
    templater=loader.get_template('jihuo.html')
    activate_url="http://127.0.0.1:8000/fruit/users/?action=activate&token=%s" % token
    htmlmessage=templater.render({
        "username":username,"activate_url":activate_url
    })
    send_mail(subject,"",EMAIL_HOST_USER,[to_email,],html_message=htmlmessage)


def get_total_price(user):
    cars=Cart.objects.filter(c_user=user).filter(is_select=True)
    total=0
    for car in cars:
        total+=car.c_goods_num*car.c_goods.g_price
    return total