# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_regions(apps, schema_editor):
    Regions = apps.get_model('medtus', 'Regions')
    Towns = apps.get_model('medtus', 'Towns')

    for town in Towns.objects.all():
        if town.region == 0:
            town.region = 1

        region = Regions.objects.get_or_create(
                    order=town.country_id,
                    country_id=town.country_id,
                    title=u'{}-{}-region'.format(town.country_id,
                                                 town.region))[0]

        town.region = region.id
        town.save()


def revert_create_regions(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('medtus', '0002_auto_20220221_1206'),
    ]

    operations = [
        migrations.RunPython(create_regions, revert_create_regions),
    ]
