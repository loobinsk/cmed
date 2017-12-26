from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover
from django.views.generic import TemplateView

dajaxice_autodiscover()

from django.contrib import admin
admin.autodiscover()
from partners.views import PartnersListView
from photos.views import PGalleriesListView, PGalleriesDetailView
from django.views.generic.base import RedirectView
from medtus.views import medtus403, medtus404, medtus500

handler403 = medtus403
handler404 = medtus404
handler500 = medtus500


urlpatterns = patterns('',
    url(r'^$', 'posts.views.Main', name='mainpage'),
    url(r'^opinion/$', 'posts.views.Opinion', name='opinion'),
    url(r'^lecturers/', include('lecturers.urls')),
    url(r'^videos/', include('videos.urls')),
    url(r'^rss/','rss.rssp.rssfeed'),
    url(r'^newsrss/', include('rss.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^consultations/', include('posts.urls')),
    url(r'^practice/', include('posts.urls')),
    url(r'^articles/', include('posts.urls')),
    url(r'^magazines/', include('posts.urls')),
    url(r'^tranings/', include('posts.urls')),
    url(r'^vacancies/', include('posts.urls')),
    url(r'^doctor/', include('posts.urls')),
    url(r'^posts/', include('posts.urls')),
    url(r'^groups/', include('groups.urls')),
    url(r'^groups_posts/', include('groups_posts.urls')),
    url(r'^partners/$', PartnersListView.as_view(), name='partners_list'),
    url(r'^records/',    include('records.urls')),
    url(r'^comments/$', 'comments.views.newcomment'),
    url(r'^comments/rm/$', 'comments.views.rmcomment', name='rmcomment'),
    url(r'^likes/', 'posts.views.like'),
    url(r'^dajaxice/',   include('dajaxice.urls')),
    url(r'^admin/statistic/$', 'account.views.admin_statistic'),
    url(r'^admin/',      include(admin.site.urls)),
    url(r'^account/',    include('account.urls')),
    url(r'^lenta/',      include('lenta.urls')),
    url(r'^lichnie/',    include('lichnie.urls')),
    url(r'^circle/',     include('circle.urls')),
    url(r'^photo/$',      PGalleriesListView.as_view(), name='galleries_list'),
    url(r'^photo/(?P<pk>\d+)/$', PGalleriesDetailView.as_view(), name='galleries_detail'),
    url(r'^photo/fileupload/(?P<sizex>\d+)/(?P<sizey>\d+)$', 'photos.views.fileupload',  name='photos.fileupload'),
    url(r'^photo/add/$',      'photos.views.addphoto',  name='photos.addphoto'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^mce_filebrowser/', include('mce_filebrowser.urls')),
    url(r'^banners/', include('banners.urls')),
    url(r'^translation/', include('medtus.urls')),

    #tests
    url(r'^quiz/', include('quiz.urls')),

    #redirects
    url(r'^video/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailvideos', permanent=True), name='detailvideos_old'),
    url(r'^events/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailevent', permanent=True), name='detailevent_old'),
    url(r'^photogallery/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='galleries_detail', permanent=True), name='galleries_detail_old'),
    url(r'^groups/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailgroup', permanent=True), name='detailgroup_old'),

    #posts
    url(r'^news/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailpractice', permanent=True), name='detailpractice_old'),
    url(r'^articles/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailpractice', permanent=True), name='detailpractice_old'),
    url(r'^vacancies/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailpractice', permanent=True), name='detailpractice_old'),
    url(r'^magazines/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailpractice', permanent=True), name='detailpractice_old'),
    url(r'^practice/view/(?P<pk>\d+)/?$', RedirectView.as_view(pattern_name='detailpractice', permanent=True), name='detailpractice_old'),

    url(r'^trs/$', 'medtus.views.trs', name='trs'),
     url(r'^about/$', 'medtus.views.education', name='education'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

