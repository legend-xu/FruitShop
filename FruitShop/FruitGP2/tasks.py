from time import sleep

from celery import shared_task, app

from FruitGP2.utils import send_active_email


@shared_task
def send_activate_email_async(username,to_email):
    send_active_email(username,to_email)


