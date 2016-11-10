# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-02 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0002_landtransfer_map_sheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandTransferCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=13)),
                ('code', models.CharField(max_length=20)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
