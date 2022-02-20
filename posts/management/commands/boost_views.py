# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from posts.utils import boost_views_for_latest_news


class Command(BaseCommand):
    help = u'Накрутка просмотров новостей'

    def handle(self, *args, **options):
        boost_views_for_latest_news()
