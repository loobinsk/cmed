from django.conf.urls import url

from medtus.views import translation
from django.contrib.auth.decorators import login_required
from medtus import ajax

urlpatterns = [
    # url(r'^$', translation.as_view(), name='translation'),
    url(r'^(?P<pk>\d+)/$', translation.as_view(), name='detailtranslation'),
    url(r'^feedback/$', login_required(ajax.feedback), name='feedback'),
    url(r'^getAccess/$', login_required(ajax.getAccess), name='getAccess'),
]