# -*- coding: utf-8 -*-
import json
import os

from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.conf import settings
from PIL import Image
from django.http import HttpResponse

from django.db.models import Q, Sum

from videos.models import Videos, VideoStatistics
from medtus.models import Specialities, Statistics, MaterialPhoto, MaterialVideo
from account.models import MyUser
from medtus.models import Visited
from fileshandle.views import OneFileUpload


class VideosList(ListView):
    paginate_by = '5'
    context_object_name = 'videos_list'
    search = u'Что ищем?'
    spec_filter = []
    specs = []

    def get_template_names(self):
        if self.request.is_ajax():
            self.template_name = 'videos/videos_ajax.html'
        else:
            self.template_name = 'videos/videos.html'
        return self.template_name

    def get_queryset(self):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
        if self.search != u'Что ищем?' and self.search != '':
            query = Q(title__icontains=self.search) | Q(description__icontains=self.search)
        else:
            query = Q()

        query = Videos.objects.filter(Q(show_medtus=1, status=1) & query)

        format = self.request.GET.get('format')
        if format:
            query = query.filter(format__in=format.split(','))

        specs_queryset = query.values('spec_id').annotate(total=Sum('spec_id'))
        self.specs = [x['spec_id'] for x in specs_queryset]

        self.spec_filter = self.request.GET.get('spec_id')
        if self.spec_filter and self.spec_filter != u'all':
            query = query.filter(spec_id__id__in=self.spec_filter.split(','))
        return query

    def get_context_data(self, **kwargs):
        context = super(VideosList, self).get_context_data(**kwargs)
        user = self.request.user

        if not user.is_anonymous:
            from account.models import EventAccess

            EventAccess.update("videos", user)
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['current_videos_specs'] = Specialities.objects.filter(id__in=self.specs).order_by('name')
        context['spec_filter'] = self.spec_filter and self.spec_filter.split(',') or []
        context['search'] = self.search
        return context


class DetailView(DetailView):
    model = Videos
    template_name = 'videos/detailvideo.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        user = self.request.user
        video = Videos.objects.get(id=self.kwargs['pk'])  

        if not user.is_anonymous:
            VideoStatistics.objects.create(video=video, user=user)
        
        statistics = Statistics.objects.filter(material_id=self.kwargs['pk'], service_id=10)
        if 'text' in self.request.META['HTTP_ACCEPT']:
            if statistics:
                statistics[0].viewings = statistics[0].viewings + 1
                statistics[0].save()
                context['viewings'] = statistics[0].viewings
            else:
                Statistics.objects.create(material_id=self.kwargs['pk'], service_id=10, viewings=1)
                context['viewings'] = 1
        Visited.record(self.get_object())
        return context


def addvideo(request):
    if request.POST:
        error = ""
        spec_id = request.POST.get('data[spec_id]', False)
        type = request.POST.get('data[type]', False)
        title = request.POST.get('data[title]', False)
        description = request.POST.get('data[description]', False)
        public_main = bool(request.POST.get('data[public_main]', False))
        if spec_id == '0':
            error += u'<p>Вы не выбрали специальность</p>'
        if type == '0':
            error += u'<p>Вы не выбрали тип видеоматериала</p>'
        if title == u'Введите заголовок':
            error += u'<p>Введите название видеоматериала</p>'
        if description == u'Введите текст':
            error += u'<p>Введите описание видеоматериала</p>'
        if error == "":
            m = Videos.objects.create(user_id=MyUser(id=request.user.id), spec_id=Specialities(id=spec_id), title=title,
                                      description=description, format=type, createdate=timezone.now(), status=1,
                                      comment_cnt=0,
                                      public_main=public_main)
            media = dict()
            media['photo'] = {}
            media['video'] = {}
            index = 0
            while request.POST.get('data[photo][%s]' % index, False):
                val = request.POST['data[photo][%s]' % index]
                key = index
                index += 1
                src = os.path.join(settings.MEDIA_ROOT, val)
                result = OneFileUpload(file(src), ['post_images', ])
                resultjson = json.loads(result)
                if not resultjson['result']:
                    return HttpResponse("Error!!!:" + resultjson['message'])
                if resultjson['result']:
                    media['photo'][key] = {}
                    media['photo'][key]['photo'] = resultjson['file']
                    media['photo'][key]['thumb'] = resultjson['url']

            index = 0
            while request.POST.get('data[video][%s]' % index, False):
                val = request.POST['data[video][%s]' % index]
                key = index
                index += 1
                src = settings.PUBLIC_HTML_ROOT + val
                dst = os.path.join(settings.MEDIA_ROOT, 'post_images', os.path.basename(val))
                im = Image.open(src)
                im.save(dst, "JPEG")
                media['video'][key] = {}
                media['video'][key]['video'] = dst
            for key, val in sorted(media['photo'].iteritems()):
                pp = MaterialPhoto()
                url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['photo']))
                pp.picture = url
                url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['thumb']))
                pp.thumb = url
                pp.service_id = Videos.SERVICE_ID
                pp.object_id = m.id
                pp.save()
            for key, val in sorted(media['video'].iteritems()):
                pv = MaterialVideo()
                url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['video']))
                pv.preview = url
                video = val['video'].split(".")
                video.pop()
                pv.data = '<iframe width="430" height="315" src="//www.youtube.com/embed/' + os.path.basename(
                    ".".join(video)) + '" frameborder="0" allowfullscreen></iframe>'
                pv.service_id = Videos.SERVICE_ID
                pv.object_id = m.id
                pv.save()
                m.code = pv.data
                m.image = url
            m.save()
            return HttpResponse(json.JSONEncoder().encode({'result': True}))
        else:
            return HttpResponse(json.JSONEncoder().encode({'message': error, 'result': False}))
    else:
        return HttpResponse(json.JSONEncoder().encode({'message': 'error POST query!', 'result': False}))

