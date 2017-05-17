# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from groups.models import Group, GroupUsers
from medtus.models import Specialities
from posts.models import Posts
from django.contrib.auth.models import User
#from account.models import MyUser
from django.views import generic
from django.utils import timezone

class GroupsList(ListView):
    paginate_by = '15'
    def get_queryset(self):
        if self.request.is_ajax():
            self.template_name = 'groups/groups_ajax.html'
        else:
            self.template_name = 'groups/groups.html'
        query = Group.objects.order_by('-createdate') #.exclude(user_id__id=self.request.user.id)
        spec_id=self.request.GET.get('spec_id')
        if spec_id:
            query=query.filter(spec_id__id__in=spec_id.split(','))
        return query
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GroupsList, self).get_context_data(**kwargs)
        # Add in the publisher
        #context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['mygroupscreate_list'] = Group.objects.filter(user_id__id=self.request.user.id).order_by('-createdate')
        context['mygroups_list'] = GroupUsers.objects.filter(user_id=self.request.user.id, activated=1).exclude(group_id__user_id__id=self.request.user.id).order_by('-group_id__createdate')
        #context['array_mygroups_list'] = 
        grs = GroupUsers.objects.filter(user_id=self.request.user.id, activated=1).values('group_id')
        arr = []
        for gr in grs:
            arr.append(gr['group_id'])
        context['array_mygroups_list'] = arr
        #if not (context['mygroups_list']):
        context['title'] = 'Группы, в которых вы состоите:'
        context['path'] = self.request.path
        context['nonactivated'] = GroupUsers.objects.filter(user_id=self.request.user.id, activated=0).count()
        return context 

class DetailViewGroup(DetailView):
    model = Group
    def get_context_data(self, **kwargs):

        if self.request.is_ajax():
            self.template_name = 'posts/posts_ajax.html'
        else:
            self.template_name = 'groups/detailgroup.html'

        # Call the base implementation first to get a context
        context = super(DetailViewGroup, self).get_context_data(**kwargs)
        # Add in the publisher
        #context['specialities_list'] = Specialities.objects.all().order_by('name')
        #context['mygroupscreate_list'] = Group.objects.filter(user_id__id=self.request.user.id).order_by('-createdate')
        #context['mygroups_list'] = GroupUsers.objects.filter(user_id=self.request.user.id).exclude(group_id__user_id__id=self.request.user.id).order_by('-group_id__createdate')
        #context['title'] = 'Публикации в группе'
   #     context['object_list'] = Posts.objects.filter(service_id__type=15, status = 0, service_id__object_id = self.object.id).order_by('-createdate')
        context['path'] = self.request.path
        return context 

def join(request):
    j = GroupUsers.objects.create(user_id=request.user.id, group_id=Group(request.GET['id']))
    context = {'mygroups_list': GroupUsers.objects.filter(user_id=request.user.id).exclude(group_id__user_id__id=request.user.id).order_by('-group_id__createdate')}
    return render(request, 'groups/join.html', context)

def unjoin(request):
    j = GroupUsers.objects.filter(user_id=request.user.id, group_id=Group(request.GET['id'])).delete()
    context = {'mygroups_list': GroupUsers.objects.filter(user_id=request.user.id).exclude(group_id__user_id__id=request.user.id).order_by('-group_id__createdate')}
    return render(request, 'groups/join.html', context)

