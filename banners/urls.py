# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import click, view
urlpatterns = [
                       url(r'^click/(?P<banner_id>\d{1,4})/(?P<key>[-\w]+)/$', click, name='banner_click'),
                       url(r'^view/(?P<banner_id>\d+)/(?P<key>[-\w]+)/$', view, name='banner_view'),
]
