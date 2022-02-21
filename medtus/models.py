# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from datetime import datetime, timedelta
from django.utils import timezone
from tinymce.models import HTMLField

from cmedu.settings import RSS_CATEGORY_DEFAULT


class Specialities(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)

    words = models.CharField(
            max_length=250, null=True, blank=True,
            verbose_name="Список слов через пробел для детектирования rss")
    passval = models.IntegerField(
            default=RSS_CATEGORY_DEFAULT,
            verbose_name="порог для детектирования rss")
    show = models.BooleanField(default=True, verbose_name="Показывать в rss")

    class Meta:
        db_table = u'Specialities'
        verbose_name = u'Специальность'
        verbose_name_plural = u'Специальности'

    def __unicode__(self):
        return u"%s" % (self.name)


class PostLinks(models.Model):
    """
        Post - Group Relation
    """
    post_id = models.IntegerField(primary_key=True)
    service_id = models.IntegerField()
    object_id = models.IntegerField()  # group of posts
    type = models.IntegerField()

    class Meta:
        db_table = u'PostLinks'


class Countries(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.IntegerField()
    title = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'Countries'
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'
        ordering = ('id', )

    def __unicode__(self):
        return u"%s" % (self.title)


class Regions(models.Model):
    country_id = models.IntegerField(db_index=True, default=1)
    order = models.IntegerField(default=65000)
    title = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = u'Regions'
        verbose_name = u'Регион'
        verbose_name_plural = u'Регионы'
        ordering = ('order', )

    def __unicode__(self):
        return u"%s" % (self.title)


class Towns(models.Model):
    # country_id = models.IntegerField(db_index=True, default=1)
    region_id = models.IntegerField(db_index=True)
    order = models.IntegerField(default=65000)
    name = models.CharField(max_length=255, blank=True, db_index=True)
    checked = models.IntegerField(default=1, db_index=True)
    okrug = models.IntegerField(default=0)
    size = models.IntegerField(default=1)

    class Meta:
        db_table = u'Towns'
        unique_together = ['region_id', 'name']
        index_together = [
            ['region_id', 'name'],
        ]
        verbose_name = u'Город'
        verbose_name_plural = u'Города'

    def __unicode__(self):
        return u"%s" % (self.name)


class Statistics(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    material_id = models.IntegerField(null=True, blank=True)
    service_id = models.IntegerField(null=True, blank=True)
    viewings = models.IntegerField(null=True, blank=True)
    likes = models.TextField()

    class Meta:
        db_table = u'statistics'
        verbose_name = u'Статистика'
        verbose_name_plural = u'Статистика'

        # def __unicode__(self):
        # return u"%s" % (self.viewings)


class Like(models.Model):
    material_id = models.IntegerField(null=True, blank=True)
    service_id = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey('account.MyUser')
    createdate = models.DateTimeField(auto_now_add=True)


class Visited(models.Model):
    material_id = models.IntegerField(null=True, blank=True)
    counter = models.IntegerField(default=0)
    lastview = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType)
    content_object = fields.GenericForeignKey('content_type', 'material_id')

    @classmethod
    def record(cls, obj):
        # try:
        now = timezone.now()
        if obj.createdate and obj.createdate > now - timedelta(weeks=24):
            content_type = ContentType.objects.get_for_model(obj)
            v, _ = Visited.objects.get_or_create(content_type=content_type, material_id=obj.id)
            v.counter += 3000
            v.lastview = datetime.now()
            v.save()
            # except:
            #     pass


class MaterialPhoto(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    object_id = models.IntegerField(null=True, blank=True)
    service_id = models.IntegerField(null=True, blank=True)
    picture = models.ImageField(upload_to='post_images')
    thumb = models.ImageField(upload_to='post_images', blank=True)


class MaterialVideo(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    object_id = models.IntegerField(null=True, blank=True)
    service_id = models.IntegerField(null=True, blank=True)
    data = models.CharField(max_length=255, unique=False)
    preview = models.CharField(max_length=255, unique=False, blank=True)


class Translation(models.Model):
    """
        Translation
    """
    title = models.CharField(max_length=255, blank=False, default=u'Трансляция')
    data_open = HTMLField(default=None, blank=True, verbose_name=u'Открытые данные')
    data = HTMLField(default=None, blank=True, verbose_name=u'Данные')
    begindate = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата и время начала трансляции')
    enddate = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата и время окончания трансляции')
    is_accredited = models.BooleanField(blank=True, default=0, verbose_name=u'Аккредитован НМО')
    checks_count = models.IntegerField(default=0, verbose_name=u'Кол-во проверок присутствия пользователя на странице', blank=True)
    active = models.BooleanField(default=True, verbose_name=u'Активность')

    def __unicode__(self):
        return u"%s" % (self.title,)

    def translation_link(self):
        from django.core.urlresolvers import reverse
        from django.utils.safestring import mark_safe

        url = reverse('detailtranslation', kwargs={'pk': self.pk})
        return mark_safe(u'<a target="_blank" href="{url}" target="_blank">{url}</a>'.format(url=url))

    class Meta:
        verbose_name = u'Трансляция'
        verbose_name_plural = u'Трансляции'

    link = property(translation_link)


class TranslationModal(models.Model):
    translation = models.ForeignKey('medtus.Translation')
    datetime = models.DateTimeField(null=False, blank=False, verbose_name=u'Дата и время проверки')


class TranslationVisit(models.Model):
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_update = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('account.MyUser')
    post = models.ForeignKey('medtus.Translation')

    class Meta:
        ordering = ['-dt_create']


class TranslationViewer(models.Model):
    user = models.ForeignKey('account.MyUser')
    post = models.ForeignKey('medtus.Translation')
    checks_counter = models.IntegerField(default=0, blank=False)
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dt_create']


class Feedback(models.Model):
    """
        Feedback
    """
    topic = models.CharField(max_length=255, blank=False, verbose_name=u"Тема обращения")
    name = models.CharField(max_length=255, blank=False, verbose_name=u"Имя")
    contact = models.CharField(max_length=255, blank=False, verbose_name=u"Контактные данные")
    position = models.CharField(max_length=255, blank=False, verbose_name=u"Должность")
    text = models.TextField(verbose_name=u"Текст обращения")
    answered = models.BooleanField(default=False, verbose_name=u"Обработано")
    datetime = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name=u"Время")

    def __unicode__(self):
        return u"%s" % (self.topic,)

    class Meta:
        verbose_name = u'Сообщение обратной связи'
        verbose_name_plural = u'Сообщения обратной связи'


class ContentPage(models.Model):
    css = models.TextField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    content = HTMLField()
    private = models.BooleanField(default=False, verbose_name="Закрыть страницу")
    page_alias = models.CharField(max_length=100, blank=False, default="trs321", verbose_name=u"Ссылка")
    email_field = models.BooleanField(default=False, verbose_name=u"Показывать поле email?")
    phone_field = models.BooleanField(default=False, verbose_name=u"Показывать поле телефон?")

    def __unicode__(self):
        return u"%s" % (self.title,)

    class Meta:
        verbose_name = u'Страницы'
        verbose_name_plural = u'Страницы'


class PrivateContentPageUsers(models.Model):
    full_name = models.CharField(max_length=255, blank=False, verbose_name=u"ФИО")
    email = models.CharField(max_length=255, blank=True, verbose_name=u"email")
    phone = models.CharField(max_length=255, blank=True, verbose_name=u"phone")
    city = models.CharField(max_length=255, blank=False, verbose_name=u"Город")
    speciality = models.CharField(max_length=255, blank=False, verbose_name=u"Специальность")
    page = models.ForeignKey('medtus.ContentPage', verbose_name=u"Страница")
    dt_create = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % (self.full_name,)

    class Meta:
        verbose_name = u'Заявка на доступ с popup'
        verbose_name_plural = u'Заявка на доступ с popup'
