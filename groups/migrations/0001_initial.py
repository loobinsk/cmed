# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2021-10-11 16:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('description', tinymce.models.HTMLField()),
                ('image', models.ImageField(blank=True, upload_to=b'group_images')),
                ('grouptype_id', models.IntegerField()),
                ('createdate', models.DateTimeField(auto_now_add=True)),
                ('updatedate', models.DateTimeField(auto_now=True)),
                ('premoder', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Groups',
                'verbose_name': '\u0413\u0440\u0443\u043f\u043f\u0430',
                'verbose_name_plural': '\u0413\u0440\u0443\u043f\u043f\u044b',
            },
        ),
        migrations.CreateModel(
            name='GroupTypes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('user_id', models.IntegerField()),
                ('createdate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'GroupTypes',
            },
        ),
        migrations.CreateModel(
            name='GroupUsers',
            fields=[
                ('user_id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('activated', models.BooleanField(default=False)),
                ('group_id', models.ForeignKey(db_column=b'group_id', on_delete=django.db.models.deletion.CASCADE, to='groups.Group', verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430')),
                ('invite', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='\u041f\u0440\u0438\u0433\u043b\u0430\u0448\u0430\u044e\u0449\u0438\u0439')),
            ],
            options={
                'db_table': 'GroupUsers',
            },
        ),
    ]
