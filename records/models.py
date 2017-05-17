# -*- coding: utf-8 -*-
from django.db import models
from comments.models import Comments
from medtus.models import Statistics

class Records(models.Model):
    id 		= models.IntegerField(primary_key=True, blank=True)
    spec_id 		= models.ForeignKey('medtus.Specialities', db_column='spec_id', null=True, blank=True,verbose_name=u'Специальность')
    user_id 		= models.ForeignKey('account.MyUser', db_column='user_id', verbose_name=u'Источник')
    title 		= models.CharField(max_length=255, blank=True,verbose_name=u'Название')
    content 		= models.TextField(blank=True)
    status 		= models.IntegerField()
    createdate	= models.DateTimeField(auto_now_add=True)
    updatedate	= models.DateTimeField(auto_now=True)
    #votes
    rating 		= models.IntegerField(null=True, blank=True)
    comment_cnt 	= models.IntegerField(null=True, blank=True)
    drugs		= models.CharField(max_length=255, blank=True,)

    def treeComments(self, pid=0, level=0, overflow=0, arr=[], start=0, end=None):
        query = Comments.objects.filter(object_id=self.id, service_id=23, parent_id=pid).order_by('createdate')[start:end]
        if pid==0:
            arr=[]
        for comment in query:
            statistics = Statistics.objects.filter(material_id=comment.id, service_id=9999)
            if statistics:
                arr.append([comment, level, 350-level, statistics[0]])
            else:
                arr.append([comment, level, 350-level, ''])
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
        start = Comments.objects.filter(object_id=self.id, service_id=23, parent_id=0).count()-2
        if start < 0:
            start = 0
        return self.treeComments(0, 0, 0, [], start, None)
    
    def calcHiddenComments(self):
        end = Comments.objects.filter(object_id=self.id, service_id=23, parent_id=0).count()-2
        if end > 0:
            return self.treeComments(0, 0, 0, [], 0, end)

    def calcStatistics(self):
        statistics = Statistics.objects.get(material_id=self.id, service_id=23)
        return statistics

    comments_list = property(calcComments)
    hidden_comments = property(calcHiddenComments)
    statistics = property(calcStatistics)
        
    class Meta:
        db_table 		= u'Records'
	verbose_name		=u'Электронный журнал'
	verbose_name_plural	=u'Электронный журнал'

