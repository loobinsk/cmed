# -*- coding: utf-8 -*-
from django.db import models
from tinymce.models import HTMLField

from medtus.models import Translation


SPAM_REPORT_PERIOD_CHOICES = (
    (0, 'за все время'),
    (1, 'за прошедшие сутки'),
    (7, 'за прошедшую неделю')
)


class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    online = models.BooleanField(blank=True, default=0, verbose_name=u'Онлайн-трансляция')
    translation = models.ForeignKey(Translation, blank=True, default=None, null=True, on_delete=models.DO_NOTHING)
    agreement = HTMLField(blank=True)
    spam_report_email = models.EmailField(verbose_name="Email для отчетов о спаме", blank=True, null=True)
    spam_report_period = models.SmallIntegerField(verbose_name="Период, за который формировать отчеты о спаме",
                                                  default=0, choices=SPAM_REPORT_PERIOD_CHOICES)

    def __unicode__(self):
        return u"Настройки проекта"

    class Meta:
        db_table = u'Settings'
        verbose_name = u'Настройка проекта'
        verbose_name_plural = u'Настройки проекта'


class SocialIcons(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название социальной сети')
    icon = models.ImageField(upload_to='social_icons', verbose_name=u'Иконка')
    active = models.BooleanField(default=False, verbose_name=u'Активность')
    url = models.URLField(verbose_name=u'Ссылка на социальную сеть')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Социальная сеть'
        verbose_name_plural = u'Социальные сети'
