from django.conf.urls import url

from groups import views
from groups.views import GroupsList, DetailViewGroup, ParticipantsList, fileupload, filedelete

urlpatterns = [
    url(r'^$', GroupsList.as_view(), name='groups'),
    url(r'^(?P<pk>\d+)/$', DetailViewGroup.as_view(), name='detailgroup'),
    url(r'^join/$', views.join, name='join'),
    url(r'^unjoin/$', views.unjoin, name='unjoin'),
    url(r'^add/$', views.add, name='addgroup'),
    url(r'^invitation/$', views.invitation, name='invitation'),
    url(r'^activated/$', views.activated, name='activated'),
    url(r'^fileupload/$',  fileupload,  name='fileupload'),
    url(r'^filedelete/$',  filedelete,  name='filedelete'),
    url(r'^addpost/$', views.addpost, name='addpost'),
    url(r'^avatarupload/(?P<sizex>\d+)/(?P<sizey>\d+)/(?P<groupid>\d+)$', views.avatarupload,
                           name='avatarupload'),
    url(r'^participants/(?P<pk>\d+)/$', ParticipantsList.as_view(), name='participants'),
]
