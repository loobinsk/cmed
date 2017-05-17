# -*- coding: utf-8 -*-
from rss.models import Posts,Posts,Feeds

from feedgen.feed import FeedGenerator
from django.conf import settings

from django.http import HttpResponse

def rssfeed(request):
    fg = FeedGenerator()
    fg.id('http://'+settings.SITE_URL+'/rssfeed')
    fg.link(href='http://'+settings.SITE_URL+'/rssfeed', rel='alternate')
    fg.description(u'Новости Медицины')
    fg.title(u'Новости Медицины')
    fg.language('ru')
    for entry in Posts.objects.filter(show=True):
        fe = fg.add_entry()
        
        fe.id('http://'+settings.SITE_URL+'/rssfeed/'+str(entry.id))
        fe.title(entry.title)
        fe.published(entry.published)
        fe.summary(entry.text)
    return HttpResponse(fg.rss_str(pretty=True))
