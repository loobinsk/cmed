from django.conf.urls import include, url
from lenta import views
 
urlpatterns = [
    # url(r'^$',             views.mainpage,    name='lenta'),
    url(r'^fileupload/$',  views.fileupload,  name='fileupload'),
    url(r'^filedelete/$',  views.filedelete,  name='filedelete'),
    url(r'^videoupload/$', views.videoupload, name='videoupload'),
    url(r'^videodelete/$', views.videodelete, name='videodelete'),
    url(r'^savepost/$',    views.savepost,    name='savepost'),
]
