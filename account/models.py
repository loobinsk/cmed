# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager
)
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)
from django.contrib import auth
from django.conf import settings

from medtus.models import TranslationVisit
from tinymce.models import HTMLField


logger = logging.getLogger(__name__)


class Category(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return self.name


class MyUserManager(BaseUserManager):
    def create_user(self, email, login, firstname, lastname, spec_id, town, country, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not login:
            raise ValueError('Users must have an login')
        if not firstname:
            raise ValueError('Users must have a firstname')
        if not lastname:
            raise ValueError('Users must have a lastname')
        if not spec_id:
            raise ValueError('Users must have a spec_id')
        if not town:
            raise ValueError('Users must have a town')
        if not country:
            raise ValueError('Users must have a country')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            # password=password,
            email=MyUserManager.normalize_email(email),
            login=login,
            firstname=firstname,
            lastname=lastname,
            spec_id=spec_id,
            town=town,
            country=country
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, firstname, lastname, spec_id, town, country, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not login:
            raise ValueError('Users must have an login')
        if not firstname:
            raise ValueError('Users must have a firstname')
        if not lastname:
            raise ValueError('Users must have a lastname')
        if not spec_id:
            raise ValueError('Users must have a spec_id')
        if not town:
            raise ValueError('Users must have a town')
        if not country:
            raise ValueError('Users must have a country')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            # password=password,
            email=MyUserManager.normalize_email(email),
            login=login,
            firstname=firstname,
            lastname=lastname,
            spec_id=spec_id,
            town=town,
            country=country
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AbstractBaseUser_(models.Model):
    password = models.CharField(db_column='pass', max_length=128, blank=True, null=True)
    last_login = models.DateTimeField('last login', default=timezone.now)

    is_active = True
    is_anonymous = False
    is_authenticated = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_username(self):
        """Return the identifying username for this User"""
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    #def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
    #    return False

    #def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
    #    return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_full_name(self):
        raise NotImplementedError()

    def get_short_name(self):
        raise NotImplementedError()


"""
id
spec_id
login
pass
firstname
lastname
surname
avatar
email
status
createdate
updatedate
lastvisit
lastaccess
type
user_ptr_id
"""


class MyUser(AbstractBaseUser_, PermissionsMixin):
    id = models.AutoField(primary_key=True, db_column='id')
    login = models.CharField(max_length=255, unique=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    avatar = models.FileField(upload_to='profile_images', blank=True)
    sex = models.CharField(max_length=256, blank=True, null=True)
    birthday = models.DateField(max_length=256, blank=True, null=True)
    spec_id = models.ForeignKey('medtus.Specialities', db_column='spec_id', null=True, blank=True,
                                verbose_name=u'Специальность', related_name='myuser_spec_id', db_index=True)
    experience = models.CharField(max_length=256, blank=True, null=True)
    addspeciality = models.ForeignKey('medtus.Specialities', db_column='addspeciality', null=True, blank=True,
                                      verbose_name=u'Дополнительная специальность', related_name='myuser_addspeciality')
    addexperience = models.CharField(max_length=256, blank=True, null=True)
    graduate = models.ForeignKey('library.Graduate', null=True, blank=True, db_index=True,
                                 verbose_name=u'Ученая степень')
    dissertation = models.CharField(max_length=256, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    addtitle = models.CharField(max_length=256, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, db_index=True)
    organization = models.CharField(max_length=256, blank=True, null=True)
    job = models.CharField(max_length=256, blank=True, null=True)
    site = models.CharField(max_length=256, blank=True, null=True)
    school = models.CharField(max_length=256, blank=True, null=True)
    graduate_year = models.CharField(max_length=256, blank=True, null=True)
    faculty = models.CharField(max_length=256, blank=True, null=True)
    cathedra = models.CharField(max_length=256, blank=True, null=True)
    country = models.ForeignKey('medtus.Countries', db_column='country', null=True, blank=True, verbose_name=u'Страна', db_index=True)
    region = models.ForeignKey('medtus.Regions', db_column='region', null=True, blank=True, verbose_name=u'Регион', db_index=True)
    town = models.ForeignKey('medtus.Towns', db_column='town', null=True, blank=True, verbose_name=u'Город', db_index=True)
    phone_number = models.CharField(max_length=256, blank=True, null=True)
    phone_visible = models.CharField(max_length=256, blank=True, null=True)
    email_visible = models.CharField(max_length=256, blank=True, null=True)
    ICQ_Skype = models.CharField(max_length=256, blank=True, null=True)
    social = models.CharField(max_length=256, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    surname = models.CharField(max_length=256)
    status = models.IntegerField(default=0)
    createdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now=True)
    lastvisit = models.DateTimeField(default=timezone.now)
    lastaccess = models.DateTimeField(default=timezone.now)
    type = models.IntegerField(default=0, blank=True, null=True)
    user_ptr_id = models.IntegerField(default=0)
    awords = models.ForeignKey('account.Aword', null=True, blank=True, verbose_name=u'Достижения')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login', 'firstname', 'lastname', 'spec_id', 'town', 'country']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return unicode(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        if self.is_staff and perm in ('posts.delete_posts', 'comments.delete_comments', 'events.delete_events',
                                      'photos.delete_pgalleries', 'rss.delete_posts', 'videos.delete_videos'):
            return True
        for backend in auth.get_backends():
            if hasattr(backend, "has_perm"):
                if backend.has_perm(self, perm, obj):
                    return True
        return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def calcAdditionalImage(self):
        images = AdditionalImage.objects.filter(user_id=self.id)
        return images

    def get_groups(self):
        """
            Groups created by user and groups user's joined
        """
        from groups.models import Group
        groups = Group.objects.raw("""select g.* from Groups g
                                    where g.user_id = '{user_id}'
                                    UNION
                                    select g.* from `GroupUsers` as gu
                                    join Groups g ON gu.group_id = g.id
                                    where gu.user_id = '{user_id}';""".format(user_id=self.id))
        return dict((g.pk, g) for g in groups)

    images = property(calcAdditionalImage)

    class Meta:
        index_together = [
            ['id', 'town'],
            ['id', 'spec_id'],
        ]


class AdditionalImage(models.Model):
    image = models.FileField(upload_to='user_image')
    user_id = models.IntegerField(default=0)

    def calcData(self):
        try:
            fname = os.path.basename(self.image.name)
            dirname = os.path.dirname(self.image.name)
        except:
            fname = os.path.basename(self.image.name.encode('ascii', 'ignore'))
            dirname = os.path.dirname(self.image.name.encode('ascii', 'ignore'))
        return {
            u'thumb': os.path.join(settings.MEDIA_URL, os.path.join(dirname, u'thumb_{0}'.format(fname))),
            u'image': os.path.join(settings.MEDIA_URL, os.path.join(dirname, u'{0}'.format(fname))),
        }

    data = property(calcData)


class Aword(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(MyUser)

    def __unicode__(self):
        return self.name


class Timer(models.Model):
    user = models.ForeignKey(MyUser)
    post = models.ForeignKey('medtus.Translation')
    time = models.IntegerField(default=0)

    def increment(self):
        self.time += 30
        self.save()


class PassToken(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, unique=True)
    token = models.CharField(max_length=60)
    time = models.DateTimeField(auto_now_add=True, auto_created=True)

    def __unicode__(self):
        return self.token


class EventAccess(models.Model):
    user = models.ForeignKey(MyUser)
    time = models.DateTimeField(auto_now_add=True, auto_created=True)
    event_type = models.CharField(max_length=256)

    @classmethod
    def update(cls, event_type, user, time=False):
        if not isinstance(user, MyUser):
            user = MyUser.objects.get(pk=user)

        if cls.objects.filter(event_type=event_type, user=user).count() > 1:
            cls.objects.filter(event_type=event_type, user=user).delete()

        item = cls.objects.get_or_create(event_type=event_type, user=user, defaults={
            'time': timezone.now()
        })

        if not item[1]:
            item[0].time = timezone.now()
            item[0].save()

    @classmethod
    def check_new(cls, event_type, user, time=False):
        if not time:
            time = timezone.now()
        if not isinstance(user, MyUser):
            user = MyUser.objects.get(pk=user)
        try:
            items = cls.objects.filter(event_type=event_type, user=user, time__gt=time)[:1]
            if not items:
                raise EventAccess.DoesNotExist
            return items[0].time
        except cls.DoesNotExist:
            return False

    @classmethod
    def last_access(cls, event_type, user):
        if not isinstance(user, MyUser):
            user = MyUser.objects.get(pk=user)
        try:
            items = cls.objects.filter(event_type=event_type, user=user).order_by('-time')[:1]
            if not items:
                raise EventAccess.DoesNotExist
            return items[0].time
        except cls.DoesNotExist:
            return False

    class Meta:
        index_together = [
            ['event_type', 'user'],
            ['event_type', 'user', 'time'],
        ]

DEFAULT_USER_ID = 1
class AllMsg(models.Model):
    """
        Рассылка массовых сообщений пользователям
    """
    user = models.ForeignKey(MyUser, default=DEFAULT_USER_ID, related_name='receiver')
    msgs = HTMLField(default='', blank=True)
    datetime = models.TextField(default='', blank=True)
    type = models.PositiveSmallIntegerField(default=0)
    unreaded = models.PositiveSmallIntegerField(default=0)
