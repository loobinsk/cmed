from django.conf.urls import url

from events import views
from events.views import EventsList, DetailViewEvent
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', EventsList.as_view(), name='events'),
    url(r'^archive$', EventsList.as_view(archive=True), name='events_archive'),
    url(r'^(?P<pk>\d+)/$', DetailViewEvent.as_view(), name='detailevent'),
    url(r'^view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailevent', permanent=True), name='detailevent_old'),
    url(r'^add/$', views.addevent, name='addevent'),
]