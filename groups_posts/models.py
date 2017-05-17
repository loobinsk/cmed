# -*- coding: utf-8 -*-
from django.db import models
from medtus.models import PostLinks
from posts.models import Posts

class Group(models.Model):
    #id 		= models.IntegerField(primary_key=True, blank=True)
    title 		= models.CharField(max_length=255, blank=True,verbose_name=u'Название')
    description	= models.TextField(blank=True)
    image 		= models.TextField(blank=True)
    grouptype_id	= models.IntegerField()
    user_id 		= models.ForeignKey('account.MyUser', db_column='user_id', verbose_name=u'Источник')
    spec_id 		= models.ForeignKey('medtus.Specialities', db_column='spec_id', null=True, blank=True,verbose_name=u'Специальность')
    createdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now=True)
    premoder 		= models.IntegerField(null=True, blank=True)

    def calcCountUsers(self):
        return GroupUsers.objects.filter(group_id=self.id).count()

    def calcCountPosts(self):
        #return Posts.objects.filter(service_id__type=15, status = 0, service_id__object_id = self.id).count() #PostLinks.objects.filter(object_id=self.id).count()
        return PostLinks.objects.filter(type=15, object_id=self.id).count()

    def calc_is_owner_join(self):
        try:
            o = GroupUsers.objects.get(group_id__id=self.id, user_id=self.user_id.id)
            return True
        except:
            return False

    count_users	= property(calcCountUsers)
    count_posts	= property(calcCountPosts)
    is_owner_join = property(calc_is_owner_join)

    class Meta:
        db_table 		= u'Groups'
        verbose_name		=u'Группа'
        verbose_name_plural	=u'Группы'

class GroupUsers(models.Model):
    group_id 		= models.ForeignKey('Group', db_column='group_id', verbose_name=u'Группа')
    user_id 		= models.IntegerField(primary_key=True, blank=True)
    activated       = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return u'%s' % self.user_id

    class Meta:
        db_table 		= u'GroupUsers'

class GroupTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    createdate = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = u'GroupTypes'
