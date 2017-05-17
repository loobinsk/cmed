# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from tinymce.models import HTMLField

from cmedu.settings import RSS_PASS_DEFAULT  # ,30
from cmedu.settings import VIDEO_FORMATS_LIST
from comments.models import Comments
from medtus.models import Statistics, MaterialPhoto, MaterialVideo


class Filters(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")
    words = models.CharField(max_length=250, verbose_name="Список слов")
    active = models.BooleanField(default=True, verbose_name="Активно")
    passval = models.IntegerField(default=RSS_PASS_DEFAULT, verbose_name="порог")

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = 'Фильтры'
        verbose_name_plural = 'Фильтры'
        db_table = 'rss_filters'


class Feeds(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")
    url = models.CharField(max_length=200, verbose_name="url")
    filters = models.ManyToManyField(Filters, null=True, blank=True, verbose_name="Фильтры")
    active = models.BooleanField(default=True, verbose_name="Активно")

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = 'Rss стримы'
        verbose_name_plural = 'Rss стримы'
        db_table = 'rss_feeds'


class Posts(models.Model):
    SERVICE_ID = 69
    feed = models.ForeignKey(Feeds)
    spec_id = models.ForeignKey('medtus.Specialities', db_column='spec_id', related_name='rss_post', null=True,
                                blank=True, verbose_name='Категория')
    published = models.DateTimeField()
    createdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedate = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    text = HTMLField(max_length=250, verbose_name="Описание")
    href = models.CharField(max_length=200, verbose_name="Ссылка", null=True, blank=True)
    show = models.BooleanField(default=False, verbose_name="Показывать")
    code = models.TextField(blank=True)
    status = models.IntegerField(null=True, blank=True, verbose_name="Активность")
    image = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    popular = models.BooleanField(blank=True, default=False)
    format = models.IntegerField(verbose_name=u'Формат')
    comment_cnt = models.IntegerField(null=True, blank=True)
    comment_show = models.BooleanField(blank=True, default=True)
    show_cmedu = models.BooleanField(blank=True, default=0)
    show_medtus = models.BooleanField(blank=True, default=1)
    public_main = models.BooleanField(blank=True, default=0)

    def get_absolute_url(self):
        return reverse('detailrss', args=[self.pk])

    def calculateFormat(self):
        verbose_name = u'Формат'
        if self.format in VIDEO_FORMATS_LIST:
            return VIDEO_FORMATS_LIST[self.format]

    def treeComments(self, pid=0, level=0, overflow=0, arr=[], start=0, end=None):
        query = Comments.objects.filter(object_id=self.id, service_id=69, parent_id=pid).order_by('createdate')[
                start:end]
        if pid == 0:
            arr = []
        for comment in query:
            statistics = Statistics.objects.filter(material_id=comment.id, service_id=69)
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
        start = Comments.objects.filter(object_id=self.id, service_id=69, parent_id=0).count() - 2
        if start < 0:
            start = 0
        return self.treeComments(0, 0, 0, [], start, None)

    def calcHiddenComments(self):
        end = Comments.objects.filter(object_id=self.id, service_id=69, parent_id=0).count() - 2
        if end > 0:
            return self.treeComments(0, 0, 0, [], 0, end)

    def calcStatistics(self):
        statistics = Statistics.objects.get(material_id=self.id, service_id=69)
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
        ordering = ['-id']
        verbose_name = u'Посты'
        verbose_name_plural = u'Посты'

    def __unicode__(self):
        return u"%s" % (self.title)
