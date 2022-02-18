from django.conf.urls import url

from videos import views
from rss.views import RssList, DetailView, rss_hit

urlpatterns = [
    url(r'^$', RssList.as_view(), name='rss'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(), name='detailrss'),
    url(r'^hit/(\d+)/$', rss_hit, name='rss_hit'),

]