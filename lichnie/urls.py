from django.conf.urls import patterns, include, url
from lichnie.views import Profile
from django.contrib.auth.decorators import login_required
 
 
urlpatterns = patterns('',
    url(r'^lichnie1/$',                  'lichnie.views.lichnie1',     name='lichnie1'),
    url(r'^lichnie2/(?P<userid>\d+)$',   login_required(Profile.as_view()),     name='lichnie2'), #'lichnie.views.lichnie2',     name='lichnie2'),
    url(r'^lichnie2/$',                  login_required(Profile.as_view()),     name='lichnie2'), #'lichnie.views.lichnie2',     name='lichnie2'),
    url(r'^saveprofile/$',               'lichnie.views.saveprofile',  name='saveprofile'),
    url(r'^fileupload/(?P<sizex>\d+)/(?P<sizey>\d+)$',                'lichnie.views.fileupload',  name='lichnie.fileupload'),
    url(r'^filedelete/$',                'lichnie.views.filedelete',  name='lichnie.filedelete'),
    #url(r'^resavepass/$',  'lichnie.views.resavepass',   name='resavepass'),
)
