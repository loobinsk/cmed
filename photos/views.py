# -*- coding: utf-8 -*-
import os
import json

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import generic
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from photos.models import PGPhotos, PGalleries
from fileshandle.views import FileUploadTo, CopyFileOnly, CreateFileDir, \
    GetThumbName, ExtractUrlFromPath
from medtus.models import Specialities


class PGalleriesListView(ListView):
    context_object_name = "pgalleries_list"
    template_name = 'photos/photos.html'
    model = PGalleries
    paginate_by = 5

    def get_queryset(self):
        photos = PGalleries.objects.all().order_by("-createdate")

        if self.request.is_ajax():
            self.template_name = 'photos/photo_ajax.html'
        else:
            self.template_name = 'photos/photos.html'
        return photos

    def get_context_data(self, **kwargs):

        if not self.request.user.is_anonymous():
            from account.models import EventAccess
            EventAccess.update("pgalleries", self.request.user)

        context = super(PGalleriesListView, self).get_context_data(**kwargs)
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['show_filter'] = False
        context['show_search'] = False
        return context


class PGalleriesDetailView(generic.DetailView):
    model = PGalleries
    template_name = 'photos/detailphotos.html'


@csrf_exempt
def fileupload(request, sizex=0, sizey=0):
    result = FileUploadTo(request, ['pgphotos_images', ], int(sizex), int(sizey))
    resultjson = json.loads(result)
    if resultjson['result'] == False:
        return HttpResponse(result)
    photos = PGPhotos()
    photos.image = resultjson['file']
    photos.user = request.user
    photos.save()
    return HttpResponse(json.JSONEncoder().encode(resultjson))


def addphoto(request):
    if request.POST:
        error = ""
        data = json.JSONDecoder().decode(request.POST['data'])
        spec_id = data['spec_id']
        type = data['type']
        title = data['title']
        description = data['description']
        public_main = data['public_main']
        service_id = 10
        if spec_id == '0':
            error = error + u'<p>Вы не выбрали специальность</p>'
        if (title == u''):
            error = error + u'<p>1</p>'
        if (description == u'1'):
            error = error + u'<p>2</p>'
        if (error == ""):
            m = PGalleries.objects.create(user_id=request.user.id, spec_id_id=spec_id, title=title, description=description,
                                          createdate=timezone.now(), status=1, premoder=1, public_main=public_main)
            for val in data['photo'].iteritems():
                try:
                    basen = os.path.basename(val[1])
                    fname = CreateFileDir(('temporary', 'post', request.user.login, basen))

                    thumb = GetThumbName(fname)
                    img = ExtractUrlFromPath(CopyFileOnly(fname, CreateFileDir(('post_images',))))
                    tmb = ExtractUrlFromPath(CopyFileOnly(thumb, CreateFileDir(('post_images',))))
                    if img and tmb:
                        if not m.image:
                            m.image = img
                            m.save()
                        pp = PGPhotos()
                        pp.gallery = m
                        pp.user = request.user
                        pp.title = title
                        pp.description = description
                        pp.image = img
                        pp.status = True
                        pp.comment_cnt = 0
                        pp.rating = 0
                        pp.votes = 0
                        pp.save()
                    # else:
                    #     m.delete()
                    #     raise ValueError('ERROR: can not save photo')
                except:
                    pass

            object_list = PGalleries.objects.filter(id=m.id)
            context = {'object_list': object_list}
            return render(request, 'photos/photo_ajax.html', context)
        else:
            context = {'error': error}
            return render(request, 'events/error.html', context)
    else:
        context = {'error': '3'}
        return render(request, 'events/error.html', context)
