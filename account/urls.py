from django.conf.urls import url
from account import views, ajax
import account
urlpatterns = [
                       url(r'^agreement/$', views.agreement, name='agreement'),
                       url(r'^register1/$', views.register1, name='register1'),
                       url(r'^register2/$', views.register2, name='register2'),
                       url(r'^register3/$', views.register3, name='register3'),
                       url(r'^register4/$', views.register4, name='register4'),
                       url(r'^allmsg/$', views.allmsg, name='allmsg'),
                       url(r'^allmsgs/$', views.allmsgs, name='allmsgs'),
                       url(r'^allmsgcodes/$', views.allmsgcodes, name='allmsgcodes'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^timer/$', ajax.timer, name='timer'),
                       url(r'^forgot/$', account.views.password_forgot, name='forgot'),
                       url(r'^changepassword/$', views.password_change, name='change'),
                       url(r'^changepassword/(?P<token>\w{24})/$', views.password_change, name='change'),
                       url(r'^avatarupload/(?P<sizex>\d+)/(?P<sizey>\d+)$', views.avatarupload,
                           name='avatarupload'),
                       url(r'^addimageupload/(?P<sizex>\d+)/(?P<sizey>\d+)$', views.addimageupload,
                           name='addimageupload'),
]
