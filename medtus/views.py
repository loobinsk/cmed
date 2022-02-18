# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
import json
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views import generic
from django.utils import timezone
from datetime import  datetime, date, time, timedelta

from models import Translation, ContentPage, TranslationVisit, TranslationViewer
from settings.models import Settings
import json as simplejson

class translation(generic.DetailView):
    model = Translation
    template_name = 'medtus/translation.html'

    def get_object(self, queryset=None):
        try:
            object = super(translation, self).get_object()
            if object.is_accredited:
                try:
                    object.begindate = object.begindate.strftime("%Y/%m/%d %H:%M:%S")
                    object.enddate = object.enddate.strftime("%Y/%m/%d %H:%M:%S")
                except:
                    object.begindate = None
                    object.enddate = None
        except Http404:
            object = Translation.objects.all().first()

        return object

    def get_context_data(self, **kwargs):
        context = super(translation, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated and \
                not TranslationVisit.objects.filter(post=self.object, user=self.request.user,
                                                    dt_update__gte=timezone.now() - timedelta(minutes=3)).exists():
            context['visit'] = TranslationVisit.objects.create(post=self.object, user=self.request.user)        
       
        return context

def enlargeCounter(request):
    if request.is_ajax and request.method == "POST":
        response_data = {}
        translation = request.POST.get('translation', None)
        user = request.user.id
        translationViewer = TranslationViewer.objects.filter(post_id = translation, user_id = user).first()
        if not translationViewer:
            translationViewer = TranslationViewer(post_id = translation, user_id = user, checks_counter = 1)            
        else:
            translationViewer.checks_counter = translationViewer.checks_counter + 1
        
        try:
            translationViewer.save()
            response_data['result'] = 'success'
            response_data['message'] = 'Success save'
        except Exception as e:
            response_data['result'] = 'error'
            response_data['message'] = '%s (%s)' % (e.message, type(e))
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')

    raise Http404("Not Found")

def online(request):
    
    online_translations = Settings.objects.all()
    
    return render(request, 'medtus/online_translations.html', {'online_translations': online_translations})
    

def medtus403(request):
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response


def medtus404(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def medtus500(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

def static_page(request, page_alias):    # page_alias holds the part of the url
    request.META['CSRF_COOKIE_USED'] = True
    client = request.session
    try:
        page = ContentPage.objects.get(page_alias=page_alias)
        return render(request, 'medtus/content_page.html', {'page': page})
    except ContentPage.DoesNotExist:
        raise Http404("Page does not exist")



# class static_page(generic.DetailView):
#     model = ContentPage
#     template_name = 'medtus/content_page.html'

#     def get_context_data(self, **kwargs):
#         context = super(DetailView, self).get_context_data(**kwargs)
#         page_alias = self.kwargs['page_alias']
#         context['page'] = ContentPage.objects.get(page_alias=page_alias)
#         return context


def trs(request):
    # page = ContentPage.objects.first()
    page = ContentPage.objects.get(id=1)
    return render(request, 'medtus/content_page.html', {'page': page})

def trs2(request):
    # page = ContentPage.objects.first()
    page = ContentPage.objects.get(id=3)
    return render(request, 'medtus/content_page.html', {'page': page})


def trs3(request):
    # page = ContentPage.objects.first()
    page = ContentPage.objects.get(id=5)
    return render(request, 'medtus/content_page.html', {'page': page})   

def trs4(request):
    # page = ContentPage.objects.first()
    page = ContentPage.objects.get(id=6)
    return render(request, 'medtus/content_page.html', {'page': page})   

def trs5(request):
    # page = ContentPage.objects.first()
    page = ContentPage.objects.get(id=7)
    return render(request, 'medtus/content_page.html', {'page': page})

def mediakit(request):
    # page = ContentPage.objects.first()
    page = ContentPage.objects.get(id=9)
    return render(request, 'medtus/content_page.html', {'page': page})        

def contacts(request):
    page = ContentPage.objects.get(id=2)
    return render(request, 'medtus/content_page_contacts.html', {'page': page})

def education(request):
    page = ContentPage.objects.get(id=2)
    return render(request, 'medtus/content_page_about.html', {'page': page})




