# -*- coding: UTF-8 -*-
from django.db import models

from rss.settings import RSS_PASS_DEFAULT, RSS_CATEGORY_DEFAULT  # ,30

from tinymce.models import HTMLField


class Specialities(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)

    words = models.CharField(max_length=250, verbose_name="Список слов через пробел для детектирования rss")
    passval = models.IntegerField(default=RSS_CATEGORY_DEFAULT, verbose_name="порог для детектирования rss")
    show = models.BooleanField(default=True, verbose_name="Показывать в rss")

    class Meta:
        db_table = u'Specialities'
        verbose_name = u'Специальность'
        verbose_name_plural = u'Специальности'

    def __unicode__(self):
        return u"%s" % (self.name)


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
    spec_id = models.ForeignKey(Specialities, db_column='spec_id', null=True, blank=True, verbose_name='Категория')
    published = models.DateTimeField()
    createdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedate = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    text = HTMLField(max_length=250, verbose_name="Описание")
    href = models.CharField(max_length=200, verbose_name="Ссылка", null=True)
    show = models.BooleanField(default=True, verbose_name="Показывать")
    code = models.TextField(blank=True)
    status = models.IntegerField(null=True, blank=True)
    image = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    popular = models.BooleanField(blank=True, default=False)
    format = models.IntegerField(verbose_name=u'Формат')
    comment_cnt = models.IntegerField(null=True, blank=True)
    comment_show = models.BooleanField(blank=True, default=True)
    show_cmedu = models.BooleanField(blank=True, default=0)
    show_medtus = models.BooleanField(blank=True, default=1)
    public_main = models.BooleanField(blank=True, default=0)

    class Meta:
        db_table = 'rss_posts'
        ordering = ['-id']
        verbose_name = u'Посты'
        verbose_name_plural = u'Посты'

    def __unicode__(self):
        return u"%s" % (self.title)
