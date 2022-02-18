# -*- coding: utf-8 -*-
import json
import logging
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

from medtus.models import Towns, TranslationVisit, Translation



def timer(request):
    from account.models import Timer

    if request.POST.get('id') and request.user.is_authenticated:
        try:
            timers = Timer.objects.get_or_create(user_id=request.user.id, post_id=request.POST.get('id'))
            timers[0].increment()
            
        except Timer.MultipleObjectsReturned:
            logging.basicConfig(filename="timers.log", level=logging.INFO)
            logging.debug("Timer exception worked")
            # timers = Timer.objects.filter(user_id=request.user.id, post_id=request.POST.get('id'))[:1].values_list("id",
            #                                                                                                        flat=True)
            # Timer.objects.exclude(pk__in=list(timers)).delete()

            # timers = Timer.objects.get_or_create(user_id=request.user.id, post_id=request.POST.get('id'))
            # timers[0].increment()
        last_visit = TranslationVisit.objects.filter(user_id=request.user.id, post_id=request.POST.get('id')).order_by('-dt_create').first()
        if last_visit is None:
            translation = get_object_or_404(Translation, id=request.POST.get('id'))
            last_visit = TranslationVisit.objects.create(post=translation, user=request.user)
        last_visit.dt_update = timezone.now()
        last_visit.save()
        return HttpResponse(json.JSONEncoder().encode({'success': True}))
    else:
        return HttpResponse(json.JSONEncoder().encode({'success': False}))
