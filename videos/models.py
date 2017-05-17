# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from comments.models import Comments
from medtus.models import Statistics, MaterialPhoto, MaterialVideo
from cmedu.settings import VIDEO_FORMATS_LIST
from tinymce.models import HTMLField

class Videos(models.Model):
    SERVICE_ID = 10
    spec_id = models.ForeignKey('medtus.Specialities', db_column='spec_id')
    user_id = models.ForeignKey('account.MyUser', db_column='user_id')
    code = models.TextField(blank=True)
    status = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, verbose_name=u'Заголовок')
    description = HTMLField(verbose_name=u'Описание')
    image = models.CharField(max_length=255, blank=True)
    createdate = models.DateTimeField(null=True, blank=True)
    updatedate = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)
    popular = models.BooleanField(blank=True, default=False)
    format = models.IntegerField(verbose_name=u'Формат')
    comment_cnt = models.IntegerField(null=True, blank=True)
    comment_show = models.BooleanField(blank=True, default=True)
    popular = models.BooleanField(blank=True, default=0)
    show_cmedu = models.BooleanField(blank=True, default=0)
    show_medtus = models.BooleanField(blank=True, default=1)
    public_main = models.BooleanField(blank=True, default=0)

    def get_absolute_url(self):
        return reverse('detailvideos', args=[self.pk])

    def calculateFormat(self):
        verbose_name = u'Формат'
        if self.format in VIDEO_FORMATS_LIST:
            return VIDEO_FORMATS_LIST[self.format]

    def treeComments(self, pid=0, level=0, overflow=0, arr=[], start=0, end=None):
        query = Comments.objects.filter(object_id=self.id, service_id=10, parent_id=pid).order_by('createdate')[
                start:end]
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
        start = Comments.objects.filter(object_id=self.id, service_id=10, parent_id=0).count() - 2
        if start < 0:
            start = 0
        return self.treeComments(0, 0, 0, [], start, None)

    def calcHiddenComments(self):
        end = Comments.objects.filter(object_id=self.id, service_id=10, parent_id=0).count() - 2
        if end > 0:
            return self.treeComments(0, 0, 0, [], 0, end)

    def calcStatistics(self):
        statistics = Statistics.objects.get(material_id=self.id, service_id=10)
        return statistics

    def calcPhotos(self):
        photos = MaterialPhoto.objects.filter(object_id=self.id, service_id=self.SERVICE_ID)
        return photos

    def calcVideos(self):
        videos = MaterialVideo.objects.filter(object_id=self.id, service_id=self.SERVICE_ID)
        return videos

    comments_list = property(calcComments)
    hidden_comments = property(calcHiddenComments)
    format_string = property(calculateFormat)
    statistics = property(calcStatistics)
    photos = property(calcPhotos)
    videos = property(calcVideos)

    class Meta:
        db_table = u'Videos'
        ordering = ['-createdate']
        verbose_name = u'Видео материалл'
        verbose_name_plural = u'Видео материаллы'

