# -*- coding: utf-8 -*-
import sys
import os
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from groups.models import Group, GroupUsers, GroupTypes
from medtus.models import Specialities
from fileshandle.views import ExtractUrlFromPath, CopyFileOnly, CreateFileDir, CreatePathFromUrl
from account.models import MyUser
from django.core.urlresolvers import reverse
from django.conf import settings

#class GroupTypes(models.Model):
#    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=255)
#    user_id = models.IntegerField()
#    createdate = models.DateTimeField(auto_now_add=True)
#class Group(models.Model):
#    id 		= models.IntegerField(primary_key=True, blank=True)
#    title 		= models.CharField(max_length=255, blank=True,verbose_name=u'Название')
#    description	= models.TextField(blank=True)
#    image 		= models.TextField(blank=True)
#    grouptype_id	= models.IntegerField()
#    user_id 		= models.ForeignKey('account.MyUser', db_column='user_id', verbose_name=u'Источник')
#    spec_id 		= models.ForeignKey('medtus.Specialities', db_column='spec_id', null=True, blank=True,verbose_name=u'Специальность')
#    createdate = models.DateTimeField(auto_now_add=True)
#    updatedate = models.DateTimeField(auto_now=True)
#    premoder 		= models.IntegerField(null=True, blank=True)
#class GroupUsers(models.Model):
#    group_id 		= models.ForeignKey('Group', db_column='group_id', verbose_name=u'Группа')
#    user_id 		= models.IntegerField(primary_key=True, blank=True)
#    activated       = models.BooleanField(default=False, blank=True)

template = u'<div class="holder{0}" id="group{1}"><div class="content-block-center-item-head-photo-bg"><a target="_blank" href="{2}">		<div class="content-block-center-item-head-photo" style="background-image:url(/media/group_images/{3}), url({4})"></div></a></div><div class="description"><h3><a target="_blank" href="{5}">{6}</a></h3><span class="info">открытая группа</span><p><em>{7}</em></p><div class="info-panel"><span>Участников: {8}</span><span>Публикаций: {9}</span></div><span class="inform">Создатель группы: <a href="{10}">{11} {12} {13}</a></span></div><div class="links">{14}</div></div>'
#template = '<div class="holder{0}" id="group{1}"><div class="content-block-center-item-head-photo-bg"><a target="_blank" href=""><div>class="content-block-center-item-head-photo" style="background-image:url(/media/group_images/), url()"></div></a></div><div class="description"><h3><a target="_blank" href=""></a></h3><span class="info">открытая группа</span><p><em></em></p><div class="info-panel"><span>Участников: </span><span>Публикаций: </span></div><span class="inform">Создатель группы: <a href="#"></a></span></div><div class="links"></div></div>'

@dajaxice_register
def addgroup(request, Spec_id, Text, Title, File):#(request, Rubrica, Spec_id, Text, Title):
    dajax = Dajax()
    if Title=='':
        dajax.alert("Введите заголовок")
        return dajax.json()
    if Text=='':
        dajax.alert("Введите описание")
        return dajax.json()
    img = ExtractUrlFromPath( CopyFileOnly(os.path.join(settings.MEDIA_ROOT, File), CreateFileDir(('group_images',))) )
    if not img:
        dajax.alert( 'Error' )
        return dajax.json()
    try:
        group = Group.objects.create(title=Title, description=Text, image=img, grouptype_id=0, user_id=MyUser(id=request.user.id), spec_id=Specialities(id=Spec_id), premoder=0)
        gusers = GroupUsers.objects.create(group_id=group, user_id=request.user.id, activated=True)
        dajax.prepend('#groups-area', 'innerHTML', template.format('', group.id, reverse('detailgroup', args=(group.id,)), group.image, group.image, reverse('detailgroup', args=(group.id,)), group.title, '', group.count_users, group.count_posts, reverse('lichnie2', args=(request.user.id,)), request.user.firstname, request.user.lastname, request.user.surname, u'<a class="delete-group" onclick=\'JoinAGroup("%s", "/groups/unjoin");\' href="javascript:void(0)">Выйти<br>из группы</a>' % group.id))
        dajax.alert(u'Группа создана!')
        dajax.script('location.reload();')
        return dajax.json()
    except:
        if group:
            group.delete()
        if gusers:
            gusers.delete()
        dajax.alert('error when created group %s' % sys.exc_info()[0])
        dajax.remove('.content-block-center-write-form-block-2-left-photo-list')
        return dajax.json()
