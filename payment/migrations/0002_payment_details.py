# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-09 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='details',
            field=models.CharField(default='', max_length=128),
        ),
    ]
