# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from comments.models import Comments
from medtus.models import Statistics, MaterialPhoto, MaterialVideo
from cmedu.settings import FORMATS_LIST
from tinymce.models import HTMLField

from events.managers import EventsManager


class Events(models.Model):
    SERVICE_ID = 6
    id = models.AutoField(primary_key=True, blank=True)
    spec_id = models.ForeignKey('medtus.Specialities', db_column='spec_id', null=True, blank=True,
                                verbose_name=u'Специальность')
    user_id = models.ForeignKey('account.MyUser', db_column='user_id', verbose_name=u'Источник')
    country_id = models.ForeignKey('medtus.Countries', db_column='country_id', null=True, blank=True,
                                   verbose_name=u'Страна')
    town_id = models.ForeignKey('medtus.Towns', db_column='town_id', null=True, blank=True, verbose_name=u'Город')
    start = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата начала')
    end = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата окончания')
    starttime = models.TimeField(null=True, blank=True, default='00:00', verbose_name=u'Время начала')
    title = models.CharField(max_length=255, blank=True, verbose_name=u'Название')
    content = HTMLField(verbose_name=u'Описание')
    place = models.CharField(max_length=255, blank=True)
    status = models.IntegerField()
    type_id = models.IntegerField()
    comment_cnt = models.IntegerField(null=True, blank=True)
    comment_show = models.BooleanField(blank=True, default=True)
    popular = models.BooleanField(blank=True, default=False)
    votes = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    show_cmedu = models.BooleanField(blank=True, default=0)
    show_medtus = models.BooleanField(blank=True, default=1)
    public_main = models.BooleanField(blank=True, default=0)
    createdate = models.DateTimeField(auto_now_add=True)

    saved_query = None

    objects = EventsManager()

    def get_absolute_url(self):
        return reverse('detailevent', args=[self.pk])

    def calculateFormat(self):
        verbose_name = u'Формат'
        if self.type_id in FORMATS_LIST:
            return FORMATS_LIST[self.type_id]

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

    @staticmethod
    def make_tree(arr):
        tree = {}
        for comment in arr:
            if comment.id in tree.keys():
                tree[comment.parent_id].append(comment)
            else:
                tree[comment.parent_id] = [comment, ]

        return tree


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
        statistics = Statistics.objects.get(material_id=self.id, service_id=self.SERVICE_ID)
        return statistics

    def calcPhotos(self):
        photos = MaterialPhoto.objects.filter(object_id=self.id, service_id=self.SERVICE_ID).order_by('id')
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
        db_table = u'MEvents'
        verbose_name = u'Мероприятие'
        verbose_name_plural = u'Мероприятия'

