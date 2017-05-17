from django.conf.urls import patterns, include, url
 
 
urlpatterns = patterns('',
    # url(r'^$',             'lenta.views.mainpage',    name='lenta'),
    url(r'^fileupload/$',  'lenta.views.fileupload',  name='fileupload'),
    url(r'^filedelete/$',  'lenta.views.filedelete',  name='filedelete'),
    url(r'^videoupload/$', 'lenta.views.videoupload', name='videoupload'),
    url(r'^videodelete/$', 'lenta.views.videodelete', name='videodelete'),
    url(r'^savepost/$',    'lenta.views.savepost',    name='savepost'),
)
