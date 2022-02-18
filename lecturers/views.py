# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView

from medtus.models import Specialities
from lecturers.models import Lecturer
from django.db.models import Q



class LecturersList(ListView):
    paginate_by = '5'
    search = ''

    def get_queryset(self):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
        if self.search != u'Что ищем?' and self.search != '':
            query = Q(surname__istartswith=self.search) | Q(content__icontains=self.search)
        else:
            query = Q()
        if 'letter' in self.request.GET:
            query &= Q(surname__istartswith=self.request.GET.get('letter'))
        if self.request.is_ajax():
            self.template_name = 'lecturers/lecturers_ajax.html'
        else:
            self.template_name = 'lecturers/lecturers.html'
        if self.request.user.is_authenticated:
            query = Lecturer.objects.filter(query).order_by('surname')
        else:
            query = Lecturer.objects.none()	
        return query

    def get_context_data(self, **kwargs):
        context = super(LecturersList, self).get_context_data(**kwargs)
        if context['page_obj'].number > 1 and context['object_list'] and \
                        context['paginator'].page(context['page_obj'].previous_page_number())[-1].surname[:1] == \
                        context['object_list'][0].surname[:1]:
            context['hide_first_letter'] = True
        context['show_search'] = True
        context['show_filter'] = False
        context['title'] = u'Лекторы'
        context['path'] = self.request.path
        context['search'] = self.search
        context['lecturers_letters'] = Lecturer.objects.all().extra(select={'letter': 'LEFT(surname, 1)'})\
            .order_by('letter').values_list('letter', flat=True).distinct()
	return context


class DetailViewLecturer(DetailView):
    model = Lecturer
    template_name = 'lecturers/detail_lecturer.html'

    def get_context_data(self, **kwargs):
        context = super(DetailViewLecturer, self).get_context_data(**kwargs)

        context['lecturers_letters'] = Lecturer.objects.all().extra(select={'letter': 'LEFT(surname , 1)'})\
            .order_by('letter').values_list('letter', flat=True).distinct()
        return context