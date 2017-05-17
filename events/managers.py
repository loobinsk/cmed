from django.db import models


class EventsManager(models.Manager):
    def get_queryset(self):
        return super(EventsManager, self).get_queryset().select_related('user_id__spec_id', 'country_id', 'town_id', 'spec_id')
