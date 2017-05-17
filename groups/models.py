# -*- coding: utf-8 -*-
from django.db import models
from tinymce.models import HTMLField
from medtus.models import PostLinks


class Group(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'Название')
    description = HTMLField()
    image = models.ImageField(upload_to='group_images',blank=True)
    grouptype_id = models.IntegerField()
    user_id = models.ForeignKey('account.MyUser', db_column='user_id', verbose_name=u'Источник', related_name='user_id')
    spec_id = models.ForeignKey('medtus.Specialities', db_column='spec_id', null=True, blank=True,
                                verbose_name=u'Специальность', related_name='spec_id')
    createdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now=True)
    premoder = models.IntegerField(null=True, blank=True)

    def calcCountUsers(self):
        return GroupUsers.objects.filter(group_id=self.id).count()

    def calcCountPosts(self):
        posts = PostLinks.objects.raw("""select pl.* from PostLinks pl \
                                    JOIN Posts p ON p.id = pl.post_id \
                                    where pl.object_id = '{group_id}' AND `pl`.`type`='15';""".format(group_id=self.id))
        return len(list(posts))

    def calc_is_owner_join(self):
        try:
            o = GroupUsers.objects.get(group_id__id=self.id, user_id=self.user_id.id)
            return True
        except:
            return False

    def group_users(self):
        """
            Return groups members queryset
        """
        from account.models import MyUser

        users_ids = [g.user_id for g in GroupUsers.objects.filter(group_id=self.id)]
        users = MyUser.objects.filter(pk__in=users_ids)
        return users

    count_users = property(calcCountUsers)
    count_posts = property(calcCountPosts)
    is_owner_join = property(calc_is_owner_join)
    members = property(group_users)

    class Meta:
        db_table = u'Groups'
        verbose_name = u'Группа'
        verbose_name_plural = u'Группы'


class GroupUsers(models.Model):
    group_id = models.ForeignKey('Group', db_column='group_id', verbose_name=u'Группа')
    user_id = models.IntegerField(primary_key=True, blank=True)
    activated = models.BooleanField(default=False, blank=True)
    invite = models.ForeignKey('account.MyUser', verbose_name=u'Приглашающий', default=None, null=True, blank=True,
                               on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return u'%s' % self.user_id

    class Meta:
        db_table = u'GroupUsers'


class GroupTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    createdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = u'GroupTypes'
