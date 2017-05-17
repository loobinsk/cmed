from django.conf.urls import patterns, url
from groups_posts.views import PostsList

urlpatterns = patterns('',
    url(r'^$', PostsList.as_view(), name='practice'),
)
