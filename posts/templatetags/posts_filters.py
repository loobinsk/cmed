# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils import timezone
import re



register = template.Library()


@register.filter
def deletion_time_left(createdate):
    now = timezone.now()
    return (now - createdate).seconds < getattr(settings, 'POST_DELETION_TIME', 30) * 60


@register.filter
def find(string, args):
    m = re.search(args, string)
    if m:
        return m.group(0)
    return ''
