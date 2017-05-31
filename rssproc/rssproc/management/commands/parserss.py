# -*- coding: UTF-8 -*-
from datetime import datetime

import feedparser
from django.core.management.base import BaseCommand
from django.utils import timezone
from fuzzywuzzy import process
from rssproc.models import Specialities, Feeds, Posts
from textblob.classifiers import NaiveBayesClassifier


def proces(entrie, feed, categorys, cl):
    ok = False
	
    for filt in feed.filters.filter(active=True):
        words = filt.words.split(' ')
        points = process.extractOne(entrie.summary, words)[1] if words else 0
        if points >= filt.passval:
            ok = True
            break
    ok = True if not feed.filters.filter(active=True) else ok
    if ok:
        try:
            pub = datetime.strptime(''.join(entrie.published.split(', ')[1].split(' ')[:4]), '%d%b%Y%H:%M:%S')
        except:
            pub = timezone.now()

        prob_dist = cl.prob_classify(entrie.summary)
        max_dist = prob_dist.max()
        cat = Specialities.objects.filter(title=max_dist)
        cat = cat[0] if cat else None
        if cat and round(prob_dist.prob(max_dist), 3) * 100 >= 20:		    
            Posts.objects.create(feed=feed, spec_id=cat, published=pub, title=entrie.title[:249], text=entrie.summary,
                                 href=entrie.get('link'), code='', format=0, show=1)


class Command(BaseCommand):
    help = 'Парсим rss'
    def handle(self, *args, **options):
        categorys = [(cat.words or '', cat.title) for cat in Specialities.objects.filter(show=True) if cat.words]
        cl = NaiveBayesClassifier(categorys)
        for feed in Feeds.objects.filter(active=True):
            data = feedparser.parse(feed.url)
            for entrie in data.get('entries', []):
                if 'summary' in entrie:
                    try:
                        post = Posts.objects.filter(text=entrie.summary)
                    except:
                        post = None

                    if not post:
                        proces(entrie=entrie, feed=feed, categorys=categorys, cl=cl)
