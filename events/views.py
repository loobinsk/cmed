# -*- coding: utf-8 -*-
import os
import json
import re
from datetime import datetime

from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic
from django.db.models import Q

from events.models import Events
from medtus.models import Specialities, Statistics, Countries, Towns, MaterialPhoto, MaterialVideo
from medtus.models import Visited
from fileshandle.views import CopyFileOnly, CreateFileDir, GetThumbName, \
    ExtractUrlFromPath
from cmedu.settings import FORMATS_LIST


class EventsList(ListView):
    paginate_by = '30'
    context_object_name = 'videos_list'
    search = ''
    archive = False

    def __init__(self, *args, **kwargs):
        super(EventsList, self).__init__(*args, **kwargs)

        if kwargs.get('archive', False):
            self.archive = True

    def get_queryset(self):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
        if self.search != u'Что ищем?' and self.search != '':
            query = Q(content__icontains=self.search) | Q(title__icontains=self.search)
        else:
            query = Q()
        if self.request.is_ajax():
            self.template_name = 'events/events_ajax.html'
        else:
            self.template_name = 'events/events.html'
        query = Events.objects.filter(Q(type_id__in=[1, 2, 3, 5, 6, 11]) & query)
        format = self.request.GET.get('format')
        if format:
            query = query.filter(type_id__in=format.split(','))
        spec_id = self.request.GET.get('spec_id')
        if spec_id:
            query = query.filter(spec_id__id__in=spec_id.split(','))

        start = self.request.GET.get('start')
        query_params = []
        if start and start != "0":
            try:
                start_date = datetime.strptime(start, '%Y-%m-%d')
                query_params.append(start_date)
                sql = "DATE(`end`) >= %s"
            except ValueError:
                sql = "DATE(`end`) >= CURDATE()"
        elif self.archive:
            sql = "DATE(`end`) < CURDATE()" #DATE(NOW() - INTERVAL 4 HOUR)
        else:
           # self.paginate_by = 50
            sql = "DATE(`end`) >= CURDATE()" #DATE(NOW() - INTERVAL 4 HOUR)

        end = self.request.GET.get('end')
        if end and end != "0":
            try:
                end_date = datetime.strptime(end, '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                query_params.append(end_date)
                sql += " AND DATE(`end`) <= %s"
            except ValueError:
                pass



        order_param = ['start']
        if self.archive:
            order_param = ['-start']

        query = query.extra(where=[sql],
                            select={'date_end': "DATE(`end` + INTERVAL 4 HOUR)",
                                     'date_start': "DATE(`start` + INTERVAL 4 HOUR)"
                            },
                            order_by=order_param, params=query_params)

        town_id = self.request.GET.get('town')
        if town_id and town_id != "0":
            query = query.filter(town_id__id=town_id)[:100]
        else:
            country_id = self.request.GET.get('country')
            if country_id and country_id != "0":
                query = query.filter(country_id__id=country_id)


        return query

    def get_context_data(self, **kwargs):
        context = super(EventsList, self).get_context_data(**kwargs)
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['countries_list'] = Countries.objects.all().order_by('title')
        context['towns_list'] = Towns.objects.filter(country_id=1).order_by('name')
        context['search'] = self.search

        if not self.request.user.is_anonymous():
            from account.models import EventAccess
            EventAccess.update("events", self.request.user)

        if self.archive:
            context['archive'] = True
        return context


class DetailViewEvent(generic.DetailView):
    model = Events
    template_name = 'events/detailevent.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailViewEvent, self).get_context_data(**kwargs)
        # context['request'] = self.kwargs['pk']
        # Add in the publisher
        statistics = Statistics.objects.filter(material_id=self.kwargs['pk'], service_id=6)
        if statistics:
            statistics[0].viewings = statistics[0].viewings + 1
            statistics[0].save()
            context['viewings'] = statistics[0].viewings
            # context['likes'] = (statistics[0].likes).split(' ').count
        else:
            Statistics.objects.create(material_id=self.kwargs['pk'], service_id=6, viewings=1)
            context['viewings'] = 1
        Visited.record(self.get_object())

        return context


def addevent(request):
    if request.POST:
        error = ""
        daystart = request.POST.get('daystart')
        monthstart = request.POST.get('monthstart')
        yearstart = request.POST.get('yearstart')
        dayend = request.POST.get('dayend')
        monthend = request.POST.get('monthend')
        yearend = request.POST.get('yearend')
        timestart = request.POST.get('time', None)
        title = request.POST.get('title')
        spec_id = request.POST.get('spec_id', None)
        country_id = request.POST.get('country', None)
        town_id = request.POST.get('town', None)
        type_id = request.POST.get('type_id', False)
        data = json.JSONDecoder().decode(request.POST['data'])
        content = request.POST.get('description')
        if daystart == u'день' or monthstart == u'месяц' or yearstart == u'год':
            error += u'<p>Введите дату начала мероприятия</p>'
        if dayend == u'день' or monthend == u'месяц' or yearend == u'год':
            error += u'<p>Введите дату окончания мероприятия</p>'
        if title == u'Название мероприятия':
            error += u'<p>Введите название мероприятия</p>'
        if content == u'Описание мероприятия':
            error += u'<p>Введите описание мероприятия</p>'
        if not spec_id:
            error += u'<p>Выберите специальность</p>'
        if country_id == u'Выберите страну':
            error += u'<p>Выберите страну</p>'

        if error == "":
            public_main = data['public_main']
            startdate = yearstart + '-' + monthstart + '-' + daystart + " 04:00:00"
            enddate = yearend + '-' + monthend + '-' + dayend + " 23:59:00"
            startime = re.sub("^\s+|\n|\r|\s+$", '', timestart) if timestart else None
            if town_id == '0':
                town_id = None

            try:
                event = Events.objects.create(user_id=request.user, spec_id_id=spec_id,
                                              country_id_id=country_id, town_id_id=town_id, start=startdate,
                                              end=enddate, starttime=startime, title=title, content=content, status=0,
                                              type_id=type_id or 2, public_main=public_main, createdate=timezone.now())
                event.save()
            except Exception as e:
                raise ValueError('ERROR: can not create Event')

            for j, val in sorted(data['photo'].iteritems()):
                basen = os.path.basename(val)
                fname = CreateFileDir(('temporary', 'post', request.user.login, basen))
                thumb = GetThumbName(fname)
                img = ExtractUrlFromPath(CopyFileOnly(fname, CreateFileDir(('post_images',))))
                tmb = ExtractUrlFromPath(CopyFileOnly(thumb, CreateFileDir(('post_images',))))
                if img and tmb:
                    pp = MaterialPhoto()
                    pp.picture = img
                    pp.thumb = tmb
                    pp.service_id = Events.SERVICE_ID
                    pp.object_id = event.id
                    pp.save()
                else:
                    event.delete()
                    raise ValueError('ERROR: can not save photo')

            for k, val in sorted(data['video'].iteritems()):
                basen = os.path.basename(val)
                fname = CreateFileDir(('temporary', 'post', request.user.login, 'video', basen))
                vdo = ExtractUrlFromPath(CopyFileOnly(fname, CreateFileDir(('post_images',))))
                if vdo:
                    pv = MaterialVideo()
                    pv.preview = vdo
                    pv.data = '<iframe width="430" height="315" src="//www.youtube.com/embed/' + os.path.basename(
                        vdo) + '" frameborder="0" allowfullscreen></iframe>'
                    pv.service_id = Events.SERVICE_ID
                    pv.object_id = event.id
                    pv.save()
                else:
                    event.delete()
                    raise ValueError('ERROR: can not save video basen=%s fname=%s vdo=%s' % (basen, fname, vdo))

            object_list = Events.objects.filter(id=event.id)
            context = {'object_list': object_list}
            return render(request, 'events/events_ajax.html', context)
        else:
            context = {'error': error}
            return render(request, 'events/error.html', context, status=500)
    else:
        specialities_list = Specialities.objects.all().order_by('name')
        countries_list = Countries.objects.all().order_by('title')
        towns_list = Towns.objects.filter(country_id=1).order_by('name')

        context = {
            'specialities_list': specialities_list,
            'countries_list': countries_list,
            'towns_list': towns_list,
            'type_list': FORMATS_LIST
        }
        return render(request, 'events/addevent.html', context)
