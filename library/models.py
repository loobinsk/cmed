# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

class Graduate(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Town(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=128, unique=True)


class Spec(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name
