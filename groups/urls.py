from django.conf.urls import patterns, url

from groups import views
from groups.views import GroupsList, DetailViewGroup, ParticipantsList

urlpatterns = patterns('',
    url(r'^$', GroupsList.as_view(), name='groups'),
    url(r'^(?P<pk>\d+)/$', DetailViewGroup.as_view(), name='detailgroup'),
    url(r'^join/$', views.join, name='join'),
    url(r'^unjoin/$', views.unjoin, name='unjoin'),
    url(r'^add/$', views.add, name='addgroup'),
    url(r'^invitation/$', views.invitation, name='invitation'),
    url(r'^activated/$', views.activated, name='activated'),
    url(r'^fileupload/$',  'groups.views.fileupload',  name='fileupload'),
    url(r'^filedelete/$',  'groups.views.filedelete',  name='filedelete'),
    url(r'^addpost/$', views.addpost, name='addpost'),
    url(r'^avatarupload/(?P<sizex>\d+)/(?P<sizey>\d+)/(?P<groupid>\d+)$', 'groups.views.avatarupload',
                           name='avatarupload'),
    url(r'^participants/(?P<pk>\d+)/$', ParticipantsList.as_view(), name='participants'),
)
