# -*- coding: utf-8 -*
from django import template

from posts.models import Posts
from django.core.serializers import serialize
from datetime import datetime, date, time

# For render tag
from django.template import RequestContext
from django.template import Template
from random import shuffle
from random import choice
import re

register = template.Library()

@register.simple_tag(takes_context=True)
def datepicker(context, tpl='posts/datepicker.html'):
    events_list = []
    

    try:        
        events = Posts.objects.filter(type=3, begindate__gte = '2021-05-19 00:00:00')
    except:
        events = False

        
    if(len(events) > 0):
        for event in events:            
            event.begindate = datetime.date(event.begindate).strftime("%Y-%m-%d")       


    context['events'] = events
    context['count'] = len(events)

    t = template.loader.get_template(tpl)
    return t.render(context.flatten())

@register.simple_tag(takes_context=True)
def datepicker2(context, tpl='posts/datepicker2.html'):
    events_list = []


    try:
        events = Posts.objects.filter(type=3, begindate__gte = '2021-05-19 00:00:00')
    except:
        events = False


    if(len(events) > 0):
        for event in events:
            event.begindate = datetime.date(event.begindate).strftime("%Y-%m-%d")


    context['events'] = events
    context['count'] = len(events)

    t = template.loader.get_template(tpl)
    return t.render(context.flatten())

# block render
@register.simple_tag(takes_context=True)
def render(context, content):
    try:
        tpl = Template(content)
        content = RequestContext(context)
        return tpl.render(content.flatten())
    except:
        return 'Render Error'
