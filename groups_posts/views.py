# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from groups.models import Group, GroupUsers
from medtus.models import PostLinks, Statistics, Visited
from posts.models import Posts

from django.views import generic
from django.utils import timezone
from fileshandle.views import FileUpload, FileDelete, InitDir, CopyFileOnly, CreateFileDir, GetThumbName, \
    ExtractUrlFromPath
from django.http import HttpResponse
from medtus.models import Specialities, MaterialPhoto, MaterialVideo
from django.db.models import Q

from account.models import MyUser
import os
from django.views.decorators.csrf import csrf_exempt
import json


TYPE_LIST = dict([
    (u'', u'Тип материала'),
    (u'/', ['1,2,4,5,9', u'Главная лента', '0', 'Y']),
    (u'/news/', ['1', u'Новости', '0', 'Y']),
    (u'/articles/', ['2', u'Статьи', '0', 'Y']),
    (u'/consultations/', ['3', u'Он-лайн консультация', '0', 'N']),
    (u'/questions/', ['4', u'Вопрос коллегам', '0', 'Y']),
    (u'/opinions/', ['5', u'Частное мнение', '0', 'Y']),
    (u'/magazines/', ['6', u'Книги и журналы', '0', 'N']),
    (u'/tranings/', ['7', u'Тренинги', '0', 'N']),
    (u'/vacancies/', ['8', u'Резюме и вакансии', '0', 'N']),
    (u'/preparations/', ['9', u'Обсуждение препарата', '0', 'Y']),
    (u'/doctor/', ['11', u'Доктор с Большой Буквы', '20', 'N']),
    (u'/practice/', ['11', u'Опросы и исследования', '14', 'N']),
    (u'/groupsposts/', ['15', u'Публикации в группе', '21', 'Y']),
    (u'/partners/', ['50', u'Партнёры', '50', 'N'])]
)


class PostsList(ListView):
    paginate_by = 5

    search = ''

    def __init__(self, *args, **kwargs):
        super(PostsList, self).__init__(**kwargs)
        self.post_links = dict()
        self.groups = dict()

    @staticmethod
    def get_postslinks(request, **kwargs):
        if kwargs.get('groups', False):
            groups = kwargs.get('groups')
        else:
            groups = request.user.get_groups()

        post_links = list(set((pl.post_id, pl.object_id) for pl in PostLinks.objects.filter(type=15, object_id__in=groups.keys())))
        return dict(post_links)

    def get_queryset(self):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
        if self.search != u'Что ищем?' and self.search != '':
            query = Q(content__icontains=self.search) | Q(title__icontains=self.search)
        else:
            query = Q()
        if self.request.is_ajax():
            self.template_name = 'posts/posts_ajax.html'
        else:
            self.template_name = 'posts/posts.html'

        if self.request.user.is_authenticated:
            self.groups = self.request.user.get_groups()
        else:
            self.groups = dict((g.pk, g) for g in Group.objects.all())

        self.post_links = self.get_postslinks(self.request, groups=self.groups)
        query = Posts.objects.filter(Q(status=0) & query).filter(id__in=self.post_links.keys()).order_by('-createdate')
        return query

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostsList, self).get_context_data(**kwargs)

        if not self.request.user.is_anonymous:
            from account.models import EventAccess
            EventAccess.update("postlinks", self.request.user)

        # Add in the publisher
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['is_group_user'] = 1
        context['title'] = "Публикации в ваших группах"
        context['path'] = self.request.path
        context['search'] = self.search
        context['show_filter'] = False
        context['show_search'] = False
        context['groups_posts'] = False
        context['post_group_names'] = dict((pid, self.groups.get(gid, {'title': ''}).__dict__.get('title')) for pid, gid in self.post_links.iteritems())
        context['post_group_urls'] = dict((pid, gid) for pid, gid in self.post_links.iteritems())
        return context


class DetailViewPost(generic.DetailView):
    model = Posts
    template_name = 'posts/detailpost.html'

    def get_context_data(self, **kwargs):
        context = super(DetailViewPost, self).get_context_data(**kwargs)
        statistics = Statistics.objects.filter(material_id=self.kwargs['pk'], service_id=18)
        if statistics:
            statistics[0].viewings += 1
            statistics[0].save()
            context['viewings'] = statistics[0].viewings
        else:
            Statistics.objects.create(material_id=self.kwargs['pk'], service_id=18, viewings=1)
            context['viewings'] = 1
        Visited.record(self.get_object())
        return context


class DetailViewGroup(DetailView):
    model = Group

    def get_context_data(self, **kwargs):

        if self.request.is_ajax():
            self.template_name = 'posts/posts_ajax.html'
        else:
            self.template_name = 'posts/posts.html'

        context = super(DetailViewGroup, self).get_context_data(**kwargs)
        postslinks = list(set([f.post_id for f in PostLinks.objects.filter(type=15,
                                                                           object_id__in=GroupUsers.objects.filter(
                                                                               user_id=self.request.user.id,
                                                                               activated=1).exclude(
                                                                               group_id__user_id__id=self.request.user.id).order_by(
                                                                               '-group_id__createdate'))]))
        context['object_list'] = Posts.objects.filter(id__in=postslinks).order_by('-createdate')
        context['path'] = self.request.path
        context['is_no_my_group'] = True
        for f in GroupUsers.objects.filter(user_id=self.request.user.id, activated=1):
            try:
                g = Group.objects.get(id=f.group_id.id)
                if g.id == self.object.id:
                    context['is_no_my_group'] = False
                    break
            except:
                pass
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        return context


def join(request):
    j = GroupUsers.objects.create(user_id=request.user.id, group_id=Group(request.GET['id']), activated=1)
    context = {'mygroups_list': GroupUsers.objects.filter(user_id=request.user.id, activated=1).order_by(
        '-group_id__createdate').exclude(group_id__user_id__id=request.user.id).order_by('-group_id__createdate')}
    return render(request, 'groups/join.html', context)


def unjoin(request):
    GroupUsers.objects.filter(user_id=request.user.id, group_id=Group(request.GET['id'])).delete()
    context = {
    'mygroups_list': GroupUsers.objects.filter(user_id=request.user.id).order_by('-group_id__createdate').exclude(
        group_id__user_id__id=request.user.id).order_by('-group_id__createdate')}
    return render(request, 'groups/join.html', context)


def add(request):
    context = {'mygroups_list': GroupUsers.objects.filter(user_id=request.user.id).exclude(
        group_id__user_id__id=request.user.id).order_by('-group_id__createdate')}
    return render(request, 'groups/join.html', context)


def invitation(request):
    context = {'mygroups_list': GroupUsers.objects.filter(user_id=request.user.id, activated=1).exclude(
        group_id__user_id__id=request.user.id).order_by('-group_id__createdate'),
               'nonactivated': GroupUsers.objects.filter(user_id=request.user.id, activated=0).exclude(
                   group_id__user_id__id=request.user.id).order_by('-group_id__createdate').count(),
               'nonactivated_grouplist': GroupUsers.objects.filter(user_id=request.user.id, activated=0).exclude(
                   group_id__user_id__id=request.user.id).order_by('-group_id__createdate'),
               'title': 'Группы, в которые Вас пригласили:'}
    return render(request, 'groups/invitation.html', context)


def activated(request):
    #j = GroupUsers.objects.get(user_id=request.user.id, group_id=Group(request.GET['id']), activated = 0)
    #j.user_id=request.user.id
    #j.group_id=Group(request.GET['id'])
    #j.activated = 1
    #j.save()
    GroupUsers.objects.filter(user_id=request.user.id, group_id=Group(request.GET['id']), activated=0).update(
        activated=1)
    context = {'mygroups_list': GroupUsers.objects.filter(user_id=request.user.id, activated=0).exclude(
        group_id__user_id__id=request.user.id).order_by('-group_id__createdate')}
    return render(request, 'groups/join.html', context)


@csrf_exempt
def fileupload(request):
    InitDir(request, 'temporary', 'groups')
    return HttpResponse(FileUpload(request, 'temporary', 'groups'))


@csrf_exempt
def filedelete(request):
    return HttpResponse(FileDelete(request, 'temporary', 'groups'))


def addpost(request):
    if request.POST:
        error = ""
        data = json.JSONDecoder().decode(request.POST['data'])
        spec_id = data['spec_id']
        type = data['type']
        service = data['service']
        title = data['title']
        description = data['description']
        object_id = data['object_id']
        service_id = 18
        if spec_id == '0':
            error += u'<p>Вы не выбрали специальность</p>'
        if type == '0':
            error += u'<p>Вы не выбрали тип материала</p>'
        if title == u'Введите заголовок':
            error += u'<p>Введите название</p>'
        if description == u'Введите текст':
            error += u'<p>Введите описание материала</p>'
        if error == "":
            m = Posts.objects.create(user_id=MyUser(id=request.user.id), spec_id=Specialities(id=spec_id), title=title,
                                     content=description, type=type, service_id=Posts.SERVICE_ID,
                                     createdate=timezone.now(), status=0, comment_cnt=0)
            service_id = PostLinks.objects.create(service_id=Posts.SERVICE_ID, type=type, post_id=m.id,
                                                  object_id=object_id)
            for i, val in sorted(data['photo'].iteritems()):
                basen = os.path.basename(val)
                fname = CreateFileDir(('temporary', 'post', request.user.login, basen))
                thumb = GetThumbName(fname)
                img = ExtractUrlFromPath(CopyFileOnly(fname, CreateFileDir(('post_images',))))
                tmb = ExtractUrlFromPath(CopyFileOnly(thumb, CreateFileDir(('post_images',))))
                if img and tmb:
                    pp = MaterialPhoto()
                    pp.picture = img
                    pp.thumb = tmb
                    pp.service_id = Posts.SERVICE_ID
                    pp.object_id = m.id
                    pp.save()
                else:
                    m.delete()
                    service_id.delete()
                    raise ValueError('ERROR: can not save photo')

            for j, val in sorted(data['video'].iteritems()):
                basen = os.path.basename(val)
                fname = CreateFileDir(('temporary', 'post', request.user.login, 'video', basen))
                vdo = ExtractUrlFromPath(CopyFileOnly(fname, CreateFileDir(('post_images',))))
                if vdo:
                    pv = MaterialVideo()
                    pv.preview = vdo
                    pv.data = '<iframe width="430" height="315" src="//www.youtube.com/embed/' + os.path.basename(
                        vdo) + '" frameborder="0" allowfullscreen></iframe>'
                    pv.service_id = Posts.SERVICE_ID
                    pv.object_id = m.id
                    pv.save()
                else:
                    m.delete()
                    service_id.delete()
                    raise ValueError('ERROR: can not save video basen=%s fname=%s vdo=%s' % (basen, fname, vdo))

            object_list = Posts.objects.filter(id=m.id)
            context = {'object_list': object_list}
            return render(request, 'posts/posts_ajax.html', context)
        else:
            context = {'error': error}
            return render(request, 'events/error.html', context)
    else:
        context = {'error': 'Ошибка передачи данных'}
        return render(request, 'events/error.html', context)
