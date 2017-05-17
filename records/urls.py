from django.conf.urls import patterns, url

from records import views
from records.views import RecordsList, DetailViewRecord, addrecord

urlpatterns = patterns('',
    url(r'^$', RecordsList.as_view(), name='records'),
    url(r'^(?P<pk>\d+)/$', DetailViewRecord.as_view(), name='detailrecord'),
    url(r'^addrecord/$', addrecord, name='addrecord'),
)
