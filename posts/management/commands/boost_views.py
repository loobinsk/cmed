# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from posts.models import Posts
from medtus.models import Statistics
from django.db.models import F

class Command(BaseCommand):
    help = u'Накрутка просмотров новостей'

    def handle(self, *args, **options):
        ids = Posts.objects.filter(type = 1).order_by('-createdate')[:30].values_list('id', flat=True)
        ids = list(ids)
        Statistics.objects.filter(material_id__in=ids, service_id = 18).update(viewings = F('viewings') + 30)

  	# service_id = 18
    # .update(views = F('views') + 5)
