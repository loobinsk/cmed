from django.conf.urls import url
from groups_posts.views import PostsList

urlpatterns = [
    url(r'^$', PostsList.as_view(), name='practice'),
]
