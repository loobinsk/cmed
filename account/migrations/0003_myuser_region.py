# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-02-21 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medtus', '0004_auto_20220221_1420'),
        ('account', '0002_auto_20211011_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='region',
            field=models.ForeignKey(blank=True, db_column=b'region', null=True, on_delete=django.db.models.deletion.CASCADE, to='medtus.Regions', verbose_name='\u0420\u0435\u0433\u0438\u043e\u043d'),
        ),
    ]
