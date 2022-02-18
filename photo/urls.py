from django.conf.urls import url

#from photo import PGalleries
from photo.views import PhotosList, DetailView

urlpatterns = [
    url(r'^$', PhotosList.as_view(), name='photo'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(), name='detailphoto'),
]