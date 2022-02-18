# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2021-10-11 16:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('medtus', '0001_initial'),
        ('auth', '0007_alter_validators_add_error_messages'),
        ('library', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medtus.Translation'),
        ),
        migrations.AddField(
            model_name='timer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='passtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AddField(
            model_name='eventaccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='aword',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allmsg',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='myuser',
            name='addspeciality',
            field=models.ForeignKey(blank=True, db_column=b'addspeciality', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='myuser_addspeciality', to='medtus.Specialities', verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u0430\u044f \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='awords',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Aword', verbose_name='\u0414\u043e\u0441\u0442\u0438\u0436\u0435\u043d\u0438\u044f'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Category'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='country',
            field=models.ForeignKey(blank=True, db_column=b'country', null=True, on_delete=django.db.models.deletion.CASCADE, to='medtus.Countries', verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='graduate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.Graduate', verbose_name='\u0423\u0447\u0435\u043d\u0430\u044f \u0441\u0442\u0435\u043f\u0435\u043d\u044c'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='spec_id',
            field=models.ForeignKey(blank=True, db_column=b'spec_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='myuser_spec_id', to='medtus.Specialities', verbose_name='\u0421\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='town',
            field=models.ForeignKey(blank=True, db_column=b'town', null=True, on_delete=django.db.models.deletion.CASCADE, to='medtus.Towns', verbose_name='\u0413\u043e\u0440\u043e\u0434'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterIndexTogether(
            name='eventaccess',
            index_together=set([('event_type', 'user', 'time'), ('event_type', 'user')]),
        ),
        migrations.AlterIndexTogether(
            name='myuser',
            index_together=set([('id', 'spec_id'), ('id', 'town')]),
        ),
    ]
