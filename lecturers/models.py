# -*- coding: utf-8 -*-
import os
import random
import string

from django.db import models
from tinymce.models import HTMLField


def lecturer_img_file_name(instance, filename):
    _, ext = os.path.splitext(filename)
    dstname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    return 'lecturers/%s%s' % (dstname, ext)


class Lecturer(models.Model):
    createdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now=True)
    surname = models.CharField(max_length=50, verbose_name=u'Фамилия')
    firstname = models.CharField(max_length=50, verbose_name=u'Имя')
    secondname = models.CharField(max_length=50, verbose_name=u'Отчество')
    content = HTMLField(verbose_name=u'Описание')
    image = models.ImageField(upload_to=lecturer_img_file_name)
    short_desc = models.TextField(verbose_name=u'Краткое описание')

    def __unicode__(self):
        return u'%s %s %s' % (self.surname, self.firstname, self.secondname)

    @property
    def fio(self):
        return u'%s %s %s' % (self.surname, self.firstname, self.secondname)

    @property
    def fio_short(self):
        return u'%s %s. %s.' % (self.surname, self.firstname[:1], self.secondname[:1])

    class Meta:
        verbose_name = u'Лектор'
        verbose_name_plural = u'Лекторы'


class LecturerLink(models.Model):
    lecturer = models.ForeignKey(Lecturer, related_name='links')
    link = models.CharField(max_length=200, verbose_name=u'Ссылка')
    text = models.CharField(max_length=200, verbose_name=u'Текст')

    class Meta:
        verbose_name = u'Лектор-Ссылка'
        verbose_name_plural = u'Лектор-Ссылки'