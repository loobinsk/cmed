# -*- coding: utf-8 -*-
import sys
import os

from django.core.urlresolvers import reverse
from django.conf import settings

from groups.models import Group, GroupUsers
from medtus.models import Specialities
from fileshandle.views import ExtractUrlFromPath, CopyFileOnly, CreateFileDir
from account.models import MyUser
from django.http import HttpResponse

template = u'<div class="holder{0}" id="group{1}"><div class="content-block-center-item-head-photo-bg"><a target="_blank" href="{2}">		<div class="content-block-center-item-head-photo" style="background-image:url(/media/group_images/{3}), url({4})"></div></a></div><div class="description"><h3><a target="_blank" href="{5}">{6}</a></h3><span class="info">открытая группа</span><p><em>{7}</em></p><div class="info-panel"><span>Участников: {8}</span><span>Публикаций: {9}</span></div><span class="inform">Создатель группы: <a href="{10}">{11} {12} {13}</a></span></div><div class="links">{14}</div></div>'


def addgroup(request):
    Spec_id=request.GET.get('Spec_id')
    Text=request.GET.get('Text')
    Title=request.GET.get('Title')
    File=request.GET.get('File')
    if Title == '':
        result="Введите заголовок"
        return HttpResponse(result)
    if Text == '':
        result="Введите описание"
        return HttpResponse(result)
    img = ExtractUrlFromPath(CopyFileOnly(os.path.join(settings.MEDIA_ROOT, File), CreateFileDir(('group_images',))))
    if not img:
        result='Error'
        return HttpResponse(result)
    try:
        group = Group.objects.create(title=Title, description=Text, image=img, grouptype_id=0,
                                     user_id=MyUser(id=request.user.id), spec_id=Specialities(id=Spec_id), premoder=0)
        gusers = GroupUsers.objects.create(group_id=group, user_id=request.user.id, activated=True)
        # dajax.prepend('#groups-area', 'innerHTML',
        #               template.format('', group.id, reverse('detailgroup', args=(group.id,)), group.image, group.image,
        #                               reverse('detailgroup', args=(group.id,)), group.title, '', group.count_users,
        #                               group.count_posts, reverse('lichnie2', args=(request.user.id,)),
        #                               request.user.firstname, request.user.lastname, request.user.surname,
        #                               u'<a class="delete-group" onclick=\'JoinAGroup("%s", "/groups/unjoin");\' href="javascript:void(0)">Выйти<br>из группы</a>' % group.id))
        result=u'Группа создана!'
        return HttpResponse(result)
    except:
        if group:
            group.delete()
        if gusers:
            gusers.delete()
        result='error when created group %s' % sys.exc_info()[0]
        return HttpResponse(result)
