# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-10-22 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FruitServer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodstypeone',
            name='g_name',
            field=models.CharField(max_length=32, unique=True, verbose_name='一级目录'),
        ),
    ]
