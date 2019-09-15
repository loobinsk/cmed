# -*- coding: utf-8 -*
from django import template

from banners.models import Banner
from banners.models import BannerGroup
from banners.models import URL


# For render tag
from django.template import Context
from django.template import Template
from random import shuffle
from random import choice
import re

register = template.Library()


@register.simple_tag(takes_context=True)
def banner_group(context, group, tpl='banners/group.html'):

    try:
        page_url = context['request'].path_info
        
        group = BannerGroup.objects.get(slug=group)
        context['my'] = False
        good_urls = []

        for url in URL.objects.filter(public=True):
            
            if url.regex:
                url_re = re.compile(url.url)
                
                if url_re.findall(page_url):

                    good_urls.append(url)                  
            elif page_url == url.url:
                good_urls.append(url)
        


        banners_all = Banner.objects.filter(public=True, group=group, urls__in=good_urls)

        banners = [banner for banner in banners_all if banner.often == 10]

        banners_ids = [x for y in [[banner.id] * banner.often for banner in banners_all if banner.often < 10] for x in y]
        if(banners_ids):
            shuffle(banners_ids);
            banner_id = choice(banners_ids)
            banners.append([el for el in banners_all if el.id == banner_id][0])
    except:
        banners = False
        group = False
    if (banners and group):
        context['banners'] = banners
        context['group'] = group

    t = template.loader.get_template(tpl)
    return t.render(template.Context(context))


@register.simple_tag(takes_context=True)
def banner_one(context, banner_id, tpl='banners/banner.html'):
    try:
        page_url = context['request'].path_info
        good_urls = []
        for url in URL.objects.filter(public=True):
            if url.regex:
                url_re = re.compile(url.url)
                if url_re.findall(page_url):
                    good_urls.append(url)
            elif page_url == url.url:
                good_urls.append(url)

        banner = Banner.objects.get(id=banner_id, public=True, urls__in=good_urls)
    except:
        banner = False

    context['banner'] = banner

    t = template.loader.get_template(tpl)
    return t.render(template.Context(context))


# block render
@register.simple_tag(takes_context=True)
def render(context, content):
    try:
        tpl = Template(content)
        content = Context(context)
        return tpl.render(content)
    except:
        return 'Render Error'
