# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from photo.models import PGalleries
from medtus.models import Specialities, Statistics
from django.db.models import Q


class PhotosList(ListView):
    paginate_by = '50'
    context_object_name = 'videos_list'
    search = ''

    def get_queryset(self):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
        if self.search != u'Что ищем?' and self.search != '':
            query = Q(title__contains=self.search)
        else:
            query = Q()
        if self.request.is_ajax():
            self.template_name = 'photos/photo_ajax.html'
        else:
            self.template_name = 'photos/photos.html'
        query = PGalleries.objects.filter(Q(status=1) & query)  # filter(show_medtus=1, status=1)
        format = self.request.GET.get('format')
        if format:
            query = query.filter(format__in=format.split(','))
        spec_id = self.request.GET.get('spec_id')
        if spec_id:
            query = query.filter(spec_id__id__in=spec_id.split(','))
        return query

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PhotosList, self).get_context_data(**kwargs)

        # Add in the publisher
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['search'] = self.search
        return context


class DetailView(DetailView):
    model = PGalleries
    template_name = 'photos/detailphotos.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        # Add in the publisher
        statistics = Statistics.objects.filter(material_id=self.kwargs['pk'], service_id=10)
        if statistics:
            statistics[0].viewings = statistics[0].viewings + 1
            statistics[0].save()
            context['viewings'] = statistics[0].viewings
        else:
            Statistics.objects.create(material_id=self.kwargs['pk'], service_id=10, viewings=1)
            context['viewings'] = 1
        return context
