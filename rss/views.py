# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from medtus.models import Statistics
from medtus.models import Visited, Specialities
from rss.models import Posts, Feeds


def update_rss_statistics(pk, context):
    statistics = Statistics.objects.filter(material_id=pk, service_id=69)
    if statistics:
        statistics[0].viewings = statistics[0].viewings + 1
        statistics[0].save()
        context['viewings'] = statistics[0].viewings
    else:
        Statistics.objects.create(material_id=pk, service_id=69, viewings=1)
        context['viewings'] = 1


class RssList(ListView):
    paginate_by = '5'
    context_object_name = 'rss_list'
    search = u'Что ищем?'
    spec_filter = []
    specs = []

    def get_template_names(self):
        if self.request.is_ajax():
            self.template_name = 'rss/rss_ajax.html'
        else:
            self.template_name = 'rss/rss.html'
        return self.template_name

    def get_queryset(self):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
        if self.search != u'Что ищем?' and self.search != '':
            query = Q(title__icontains=self.search) | Q(text__icontains=self.search)
        else:
            query = Q()

        query = Posts.objects.filter(Q(show_medtus=1, show=1) & query)
        query.filter(show=True)

        cat = self.request.GET.get('cat', '')
        if cat and cat != 'all_cat':
            query = query.filter(spec_id__name=cat)

        feed = self.request.GET.get('feed', '')
        if feed and feed != 'all_feed':
            query = query.filter(feed__name=feed)

        return query

    def get_context_data(self, **kwargs):
        context = super(RssList, self).get_context_data(**kwargs)
        user = self.request.user

        if not user.is_anonymous():
            from account.models import EventAccess
            EventAccess.update("rss", user)
        context['search'] = self.search
        context['cat_list'] = Specialities.objects.raw(
            'SELECT * FROM Specialities WHERE EXISTS (SELECT * FROM rss_posts WHERE rss_posts.spec_id = Specialities.id AND rss_posts.show = 1) ORDER BY name')
        context['feed_list'] = Feeds.objects.filter(active=True).order_by('name')
        context['cat'] = self.request.GET.get('cat', '')
        context['feed'] = self.request.GET.get('feed', '')
        return context


class DetailView(DetailView):
    model = Posts
    template_name = 'rss/detailrss.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        update_rss_statistics(self.kwargs['pk'], context)
        Visited.record(self.get_object())
        return context


def rss_hit(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if request.is_ajax():
        update_rss_statistics(pk, {})
        Visited.record(post)
    return HttpResponse('')


from feedgen.feed import FeedGenerator
from django.conf import settings


def rssfeed(request):
    fg = FeedGenerator()
    fg.id('http://' + settings.SITE_URL + '/rssfeed')
    fg.link(href='http://' + settings.SITE_URL + '/rssfeed', rel='alternate')
    fg.description(u'Новости Медицины')
    fg.title(u'Новости Медицины')
    fg.language('ru')
    for entry in Posts.objects.filter(show=True):
        fe = fg.add_entry()

        fe.id('http://' + settings.SITE_URL + '/rssfeed/' + str(entry.id))
        fe.title(entry.title)
        fe.published(entry.published)
        fe.summary(entry.text)
    return HttpResponse(fg.rss_str(pretty=True))
