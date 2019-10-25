import os

import celery
from celery import Celery

# set the default Django settings module for the 'celery' program.

import FruitShop

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FruitShop.settings')

app = Celery('FruitShop')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))