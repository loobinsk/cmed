from django.shortcuts import render
from django.views.generic.list import ListView
from partners.models import Partner, Rubric

# Create your views here.

class PartnersListView(ListView):

    template_name = 'partners/partners.html'
    model = Partner

    def get_context_data(self, **kwargs):
        context = super(PartnersListView, self).get_context_data(**kwargs)
        context['partners'] = dict()
        for r in Rubric.objects.all():
            context['partners'][r] = Partner.objects.filter(rubric=r)
        return context
