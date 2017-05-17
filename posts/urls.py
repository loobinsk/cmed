from django.conf.urls import patterns, url

from posts import views
from posts.views import PostsList, DetailViewPost, DeletePost

urlpatterns = patterns('',
    url(r'^$', PostsList.as_view(), name='practice'),
    url(r'^archive$', PostsList.as_view(), name='posts_archive'),
    url(r'^(?P<pk>\d+)/?$', DetailViewPost.as_view(), name='detailpractice'),
    url(r'^add/$', views.addpost, name='addpost'),
    url(r'^rm/$', views.rmpost, name='rmpost'),
    url(r'^delete/(?P<pk>\d+)/?$', DeletePost.as_view(), name='user_delete_post'),
)