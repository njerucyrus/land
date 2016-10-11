# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-11 19:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('land', '0006_landsales_transfer_made'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandTransFerFeePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=128)),
                ('phone_number', models.CharField(max_length=13)),
                ('payment_mode', models.CharField(max_length=32)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('details', models.CharField(default='', max_length=200)),
                ('status', models.CharField(max_length=32)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('land', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='land.Land')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
