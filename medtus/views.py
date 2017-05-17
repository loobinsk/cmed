# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views import generic
from django.utils import timezone
from datetime import timedelta

from models import Translation, ContentPage, TranslationVisit


class translation(generic.DetailView):
    model = Translation
    template_name = 'medtus/translation.html'

    def get_object(self, queryset=None):
        try:
            object = super(translation, self).get_object()
        except Http404:
            object = Translation.objects.all().first()

        return object

    def get_context_data(self, **kwargs):
        context = super(translation, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated() and \
                not TranslationVisit.objects.filter(post=self.object, user=self.request.user,
                                                    dt_update__gte=timezone.now() - timedelta(minutes=3)).exists():
            context['visit'] = TranslationVisit.objects.create(post=self.object, user=self.request.user)
        return context


def medtus403(request):
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response


def medtus404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def medtus500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def trs(request):
    page = ContentPage.objects.first()
    return render(request, 'medtus/content_page.html', {'page': page})