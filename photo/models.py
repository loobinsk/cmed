# -*- coding: utf-8 -*-
from django.db import models
from comments.models import Comments
from medtus.models import Statistics
from django.contrib.contenttypes import generic

FORMATS_LIST = dict([
    (u'',u'Тип видео'),
    (1,u'Медицинская анимация'),
    (2,u'Конференция'),
    (3,u'Телевизор'),
    (4,u'Хирургическая операция'),
    (5,u'Вебинар'),
    (6,u'Онлайн-трансляция'),
    (7,u'Эксклюзивное интервью'),
    (8,u'Лекционный курс')]
)

class PGalleries(models.Model):
    id			= models.IntegerField(primary_key=True, blank=True)
    user_id		= models.ForeignKey('account.MyUser', db_column='user_id')
    title		= models.CharField(max_length=255, blank=True,verbose_name=u'Заголовок')
    description	= models.TextField(blank=True,verbose_name=u'Описание')
    image		= models.CharField(max_length=255, blank=True)
    premoder	= models.IntegerField(null=True, blank=True)
    status		= models.IntegerField(null=True, blank=True)
    createdate	= models.DateTimeField(null=True, blank=True)


    def __unicode__(self):
        return self.title

    def calculateFormat(self):
        verbose_name=u'Формат'
        if self.format in FORMATS_LIST:
            return FORMATS_LIST[self.format]

    def treeComments(self, pid=0, level=0, overflow=0, arr=[], start=0, end=None):
        query = Comments.objects.filter(object_id=self.id, service_id=10, parent_id=pid).order_by('createdate')[start:end]
        if pid==0:
            arr=[]
        for comment in query:
            arr.append([comment, level, 350-level])
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
        start = Comments.objects.filter(object_id=self.id, service_id=10, parent_id=0).count()-2
        if start < 0:
            start = 0
        return self.treeComments(0, 0, 0, [], start, None)
    
    def calcHiddenComments(self):
        end = Comments.objects.filter(object_id=self.id, service_id=10, parent_id=0).count()-2
        if end > 0:
            return self.treeComments(0, 0, 0, [], 0, end)

    def calcStatistics(self):
        statistics = Statistics.objects.get(material_id=self.id, service_id=10)
        return statistics

    comments_list = property(calcComments)
    hidden_comments = property(calcHiddenComments)
    format_string = property(calculateFormat)
    statistics = property(calcStatistics)
        
    class Meta:
        db_table		= u'PGalleries'
        ordering		= ['-createdate']
        verbose_name		= u'Фото материалл'
        verbose_name_plural	= u'Фото материаллы'

