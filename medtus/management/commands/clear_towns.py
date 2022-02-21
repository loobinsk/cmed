# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from medtus.models import Towns
from events.models import Events
from account.models import MyUser


class Command(BaseCommand):
    help = u'Убирает дубли городов'

    def handle(self, *args, **options):
        pass
        # for town in Towns.objects.order_by('id'):
        #     duplicates = Towns.objects.filter(name=town.name, country_id=town.country_id, region=town.region) \
        #         .exclude(pk=town.pk)
        #     for dtown in duplicates:
        #         Events.objects.filter(town_id=dtown).update(town_id=town)
        #         MyUser.objects.filter(town=dtown).update(town=town)
        #         dtown.delete()
