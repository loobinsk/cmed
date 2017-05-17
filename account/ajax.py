# -*- coding: utf-8 -*-
import json

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

from medtus.models import Towns, TranslationVisit, Translation


@dajaxice_register
def updatecombo(request, option):
    dajax = Dajax()
    town_list = Towns.objects.filter(country_id=option).order_by('name')
    out = []
    out.append(u'<option value="0">Выберите город</option>')
    for town in town_list:
        out.append(u'<option value="{0}">{1}</option>'.format(town.id, town.name))
    dajax.assign('select[name="town"]', 'innerHTML', ''.join(out))
    dajax.script(
        '$("select[name=\'town\']")[0].jcf.selectList.style.height=\'200px\';$("select[name=\'town\']")[0].jcf.selectList.style.overflowY=\'auto\';$("select[name=\'town\']")[0].jcf.selectList.style.overflowX=\'hidden\';$("select[name=\'town\']")[0].jcf.buildDropdown();$("select[name=\'town\']")[0].jcf.refreshState();')
    return dajax.json()


def timer(request):
    from account.models import Timer

    if request.POST.get('id') and request.user.is_authenticated():
        try:
            timers = Timer.objects.get_or_create(user_id=request.user.id, post_id=request.POST.get('id'))
            timers[0].increment()
        except Timer.MultipleObjectsReturned:
            timers = Timer.objects.filter(user_id=request.user.id, post_id=request.POST.get('id'))[:1].values_list("id",
                                                                                                                   flat=True)
            Timer.objects.exclude(pk__in=list(timers)).delete()

            timers = Timer.objects.get_or_create(user_id=request.user.id, post_id=request.POST.get('id'))
            timers[0].increment()
        last_visit = TranslationVisit.objects.filter(user_id=request.user.id, post_id=request.POST.get('id')).order_by('-dt_create').first()
        if last_visit is None:
            translation = get_object_or_404(Translation, id=request.POST.get('id'))
            last_visit = TranslationVisit.objects.create(post=translation, user=request.user)
        last_visit.dt_update = timezone.now()
        last_visit.save()
        return HttpResponse(json.JSONEncoder().encode({'success': True}))
    else:
        return HttpResponse(json.JSONEncoder().encode({'success': False}))
