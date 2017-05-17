from django.conf.urls import patterns, url

from medtus.views import translation


urlpatterns = patterns('',
    # url(r'^$', translation.as_view(), name='translation'),
    url(r'^(?P<pk>\d+)/$', translation.as_view(), name='detailtranslation'),
)