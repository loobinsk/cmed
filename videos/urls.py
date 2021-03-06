from django.conf.urls import url

from videos import views
from videos.views import VideosList, DetailView

urlpatterns = [
    url(r'^$', VideosList.as_view(), name='videos'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(), name='detailvideos'),
    url(r'^add/$', views.addvideo, name='addvideo'),
]
