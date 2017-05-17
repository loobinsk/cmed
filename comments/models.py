# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from tinymce.models import HTMLField


class Comments(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')  #models.IntegerField(primary_key=True, db_column='id')
    user_id = models.ForeignKey('account.MyUser', db_column='user_id')  #models.IntegerField()
    parent_id = models.IntegerField(null=True)
    service_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    content = HTMLField()  #models.TextField(blank=True)
    votes = models.IntegerField(null=True, blank=True, default=0)
    rating = models.IntegerField(null=True, blank=True)
    createdate = models.DateTimeField(null=True, blank=True)
    updatedate = models.DateTimeField(null=True, blank=True)
    content_type_id = models.IntegerField(null=True, blank=True, default=47)  #models.ForeignKey(ContentType)
    safe = models.BooleanField(verbose_name='Показывать как HTML', default=False)

    def get_link(self):
        link = ''
        if self.service_id == 10:
            link = reverse('detailvideos', args=[self.object_id])
        if self.service_id == 6:
            link = reverse('detailevent', args=[self.object_id])
        if self.service_id == 18:
            link = reverse('detailpractice', args=[self.object_id])
        if self.service_id == 23:
            link = reverse('detailrecord', args=[self.object_id])
        return link

    link = property(get_link)

    class Meta:
        db_table = u'Comments'
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

