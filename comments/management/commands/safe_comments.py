# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.admin.models import LogEntry
from comments.models import Comments


class Command(BaseCommand):
    help = u'Помечает комметарии, которые редактировались через админку, безопасными'

    def handle(self, *args, **options):
        ids = LogEntry.objects.filter(content_type_id=27).values_list('object_id', flat=True)
        Comments.objects.filter(id__in=ids).update(safe=True)