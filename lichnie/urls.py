from django.conf.urls import include, url
from lichnie.views import Profile
from django.contrib.auth.decorators import login_required
from lichnie import views, ajax
 
urlpatterns = [
    url(r'^lichnie1/$',                  views.lichnie1,     name='lichnie1'),
    url(r'^changepass/$',  ajax.changepass,     name='changepass'),
    url(r'^lichnie2/(?P<userid>\d+)$',   login_required(Profile.as_view()),     name='lichnie2'), #'lichnie.views.lichnie2',     name='lichnie2'),
    url(r'^lichnie2/$',                  login_required(Profile.as_view()),     name='lichnie2'), #'lichnie.views.lichnie2',     name='lichnie2'),
    url(r'^saveprofile/$',               views.saveprofile,  name='saveprofile'),
    url(r'^fileupload/(?P<sizex>\d+)/(?P<sizey>\d+)$',                views.fileupload,  name='lichnie.fileupload'),
    url(r'^filedelete/$',                views.filedelete,  name='lichnie.filedelete'),
    #url(r'^resavepass/$',  views.resavepass,   name='resavepass'),
]
