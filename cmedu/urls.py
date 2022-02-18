from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
#from dajaxice.core import dajaxice_autodiscover
from django.views.generic import TemplateView
from filebrowser.sites import site

from django.contrib import admin
admin.autodiscover()
from partners.views import PartnersListView
from photos.views import PGalleriesListView, PGalleriesDetailView
from django.views.generic.base import RedirectView
from medtus.views import medtus403, medtus404, medtus500
from posts.views import Main, Opinion,like
from photos.views import fileupload, addphoto
from rss.rssp import rssfeed
from account.views import admin_statistic
from comments.views import newcomment, rmcomment
from medtus.views import contacts, education, static_page, online, enlargeCounter
from django.contrib.auth.decorators import login_required
from circle import views as circle_views
handler403 = medtus403
handler404 = medtus404
handler500 = medtus500


urlpatterns = [
    url(r'^$', Main, name='mainpage'),
    url(r'^opinion/$', Opinion, name='opinion'),
    url(r'^lecturers/', include('lecturers.urls')),
    url(r'^videos/', include('videos.urls')),
    url(r'^rss/', rssfeed),
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
    url(r'^comments/$', newcomment),
    url(r'^comments/rm/$', rmcomment, name='rmcomment'),
    url(r'^likes/', like),
    url('admin/filebrowser/', site.urls),
    url('grappelli/', include('grappelli.urls')),
    url(r'^admin/statistic/$', admin_statistic),
    url(r'^admin/',      include(admin.site.urls)),
    url(r'^account/',    include('account.urls')),
    url(r'^lenta/',      include('lenta.urls')),
    url(r'^lichnie/',    include('lichnie.urls')),
    url(r'^circle/',     include('circle.urls')),
    url(r'^photo/$',      PGalleriesListView.as_view(), name='galleries_list'),
    url(r'^photo/(?P<pk>\d+)/$', PGalleriesDetailView.as_view(), name='galleries_detail'),
    url(r'^photo/fileupload/(?P<sizex>\d+)/(?P<sizey>\d+)$', fileupload,  name='photos.fileupload'),
    url(r'^photo/add/$',  addphoto,  name='photos.addphoto'),
    url(r'^tinymce/', include('tinymce.urls')),
    #url(r'^mce_filebrowser/', include('mce_filebrowser.urls')),
    url(r'^banners/', include('banners.urls')),
    url(r'^translation/', include('medtus.urls')),
    url(r'^medtus/', include('medtus.urls')),

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

    # url(r'^trs/$', 'medtus.views.trs', name='trs'),
    # url(r'^trs2/$', 'medtus.views.trs2', name='trs2'),
    # url(r'^trs3/$', 'medtus.views.trs3', name='trs3'),
    # url(r'^trs4/$', 'medtus.views.trs4', name='trs4'),
    # url(r'^trs5/$', 'medtus.views.trs5', name='trs5'),
    # url(r'^mediakit/$', 'medtus.views.mediakit', name='mediakit'),
    url(r'^about/$', education, name='education'),
     url(r'^contacts/$', contacts, name='contacts'),
    url(r'^enlargecounter$', login_required(enlargeCounter), name='enlargeCounter'),
    url(r'^online/$', online, name='online'),
    #url(r'^nmo/$', RedirectView.as_view(url='/circle/dialog/nmo', permanent=False), name='nmo'),
    url(r'^nmo/$', login_required(circle_views.NmoDialogView.as_view()), name='nmo'),
    url(r'^contacts/$', contacts, name='contacts'),
    url(r'^(?P<page_alias>.+?)/$', static_page),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


