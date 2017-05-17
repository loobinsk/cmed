# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from tinymce.models import HTMLField

from comments.models import Comments
from medtus.models import Statistics, PostLinks, MaterialPhoto, MaterialVideo
from cmedu.settings import POST_FORMATS_LIST


class Posts(models.Model):
    SERVICE_ID = 18
    id = models.AutoField(primary_key=True, blank=True)
    spec_id = models.ForeignKey('medtus.Specialities', db_column='spec_id', null=True, blank=True,
                                verbose_name=u'Специальность')
    user_id = models.ForeignKey('account.MyUser', db_column='user_id', verbose_name=u'Источник')
    title = models.CharField(max_length=255, blank=True, verbose_name=u'Название')
    anons = models.TextField(blank=True)
    content = HTMLField()
    status = models.IntegerField()
    createdate = models.DateTimeField(null=True, blank=True)
    begindate = models.DateTimeField(null=True, blank=True)
    updatedate = models.DateTimeField(null=True, blank=True)
    # votes
    rating = models.IntegerField(null=True, blank=True)
    comment_cnt = models.IntegerField(null=True, blank=True)
    comment_show = models.BooleanField(blank=True, default=True)
    popular = models.BooleanField(blank=True, default=False)
    archive = models.BooleanField(blank=True, default=False)
    type = models.IntegerField()
    format = models.IntegerField(verbose_name=u'Формат', blank=True)
    code = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    public_main = models.BooleanField(blank=True, default=0, verbose_name=u'Публиковать на главной')

    def get_absolute_url(self):
        return reverse('detailpractice', args=[self.pk])

    def treeComments(self, pid=0, level=0, overflow=0, arr=[], start=0, end=None):
        query = Comments.objects.filter(object_id=self.id, service_id=self.SERVICE_ID, parent_id=pid).order_by(
            'createdate')[start:end]
        if pid == 0:
            arr = []
        for comment in query:
            statistics = Statistics.objects.filter(material_id=comment.id, service_id=9999)
            if statistics:
                arr.append([comment, level, 350 - level, statistics[0]])
            else:
                arr.append([comment, level, 350 - level, ''])
            level = level + 20
            if level > 40:
                level = 40
                overflow = overflow + 1
            self.treeComments(comment.id, level, overflow, arr, 0, None)
            overflow = overflow - 1
            if overflow < 0:
                level = level - 20
                overflow = 0
        return arr

    def calcComments(self):
        start = Comments.objects.filter(object_id=self.id, service_id=self.SERVICE_ID, parent_id=0).count() - 2
        if start < 0:
            start = 0
        return self.treeComments(0, 0, 0, [], start, None)

    def calcHiddenComments(self):
        end = Comments.objects.filter(object_id=self.id, service_id=self.SERVICE_ID, parent_id=0).count() - 2
        if end > 0:
            return self.treeComments(0, 0, 0, [], 0, end)

    def calcStatistics(self):
        try:
            statistics = Statistics.objects.get(material_id=self.id, service_id=self.SERVICE_ID)
        except Statistics.DoesNotExist:
            statistics = False

        return statistics

    def calcService_id(self):
        service_id = PostLinks.objects.filter(object_id=self.id)
        return service_id

    def calcGroup_ids(self):
        groups = PostLinks.objects.filter(post_id=self.id)
        return groups

    def calculateFormat(self):
        if self.type in POST_FORMATS_LIST:
            format_is = POST_FORMATS_LIST[self.type]
            if self.type == "11": format_is == "---"
            return format_is
        else:
            return ""

    def calcPhotos(self):
        photos = MaterialPhoto.objects.filter(object_id=self.id, service_id=self.SERVICE_ID).order_by('pk')
        return photos

    def calcVideos(self):
        videos = MaterialVideo.objects.filter(object_id=self.id, service_id=self.SERVICE_ID)
        return videos

    comments_list = property(calcComments)
    hidden_comments = property(calcHiddenComments)
    format_string = property(calculateFormat)
    statistics = property(calcStatistics)
    service_id = property(calcService_id)
    groups = property(calcGroup_ids)
    photos = property(calcPhotos)
    videos = property(calcVideos)

    class Meta:
        db_table = u'Posts'
        verbose_name = u'Пост'
        verbose_name_plural = u'Посты'

