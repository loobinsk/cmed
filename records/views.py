# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView
from records.models import Records
from medtus.models import Specialities, Statistics
#from django.contrib.auth.models import User
#from account.models import CustomUser
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse

class RecordsList(ListView):

    paginate_by = '5'
    context_object_name = 'object_list'
    def get_queryset(self):
        if self.request.is_ajax():
            self.template_name = 'records/records_ajax.html'
        else:
            self.template_name = 'records/records.html'
        query = Records.objects.filter(status = 0).order_by('-createdate') #.extra(where=["DATE(`start`)>=DATE(NOW())"]).order_by('start') #(show_medtus=1, status=1)
    #    format=self.request.GET.get('format')
    #    if format:
    #        query=query.filter(format__in=format.split(','))
        spec_id=self.request.GET.get('spec_id')
        if spec_id:
            query=query.filter(spec_id__id__in=spec_id.split(','))
        return query
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RecordsList, self).get_context_data(**kwargs)
        # Add in the publisher
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['title'] = u'Электронный журнал'
        context['path'] = self.request.path
        return context 

class DetailViewRecord(generic.DetailView):
    model = Records
    template_name = 'records/detailrecord.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailViewRecord, self).get_context_data(**kwargs)
        #context['request'] = self.kwargs['pk']
        # Add in the publisher
        statistics = Statistics.objects.filter(material_id = self.kwargs['pk'], service_id = 23)
        if statistics:
            statistics[0].viewings = statistics[0].viewings + 1
            statistics[0].save()
            context['viewings'] = statistics[0].viewings
            #context['likes'] = (statistics[0].likes).split(' ').count
        else:
            Statistics.objects.create(material_id = self.kwargs['pk'], service_id = 23, viewings = 1)
            context['viewings'] = 1
        return context

def addrecord(request):
    try:
        t = request.POST['title']
        d = request.POST['descr']
        r = Records(title=t, content=d, user_id=request.user, rating=0, comment_cnt=0, status=0)
        r.save()
        return HttpResponse( True )
    except:
        return HttpResponse( False )

