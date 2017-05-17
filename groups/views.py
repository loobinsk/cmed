# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from groups.models import Group, GroupUsers, GroupTypes
from medtus.models import PostLinks
from posts.models import Posts

# from account.models import MyUser
from django.utils import timezone
from django.db import IntegrityError
from fileshandle.views import FileUpload, FileDelete, InitDir, CopyFileOnly, CreateFileDir, GetThumbName, \
    ExtractUrlFromPath, FileUploadTo
from django.http import HttpResponse
from medtus.models import Specialities, MaterialPhoto, MaterialVideo

from account.models import MyUser
import os
from django.views.decorators.csrf import csrf_exempt
import json

from django.conf import settings


class GroupsList(ListView):
    paginate_by = '15'

    def get_queryset(self):
        if self.request.is_ajax():
            self.template_name = 'groups/groups_ajax.html'
        else:
            self.template_name = 'groups/groups.html'

        query = Group.objects.extra(select={'post_count': "SELECT COUNT(*) FROM PostLinks pl JOIN Posts p ON p.id = pl.post_id where pl.object_id = Groups.id AND `pl`.`type`='15'"})
        query = query.extra(order_by=['-post_count'])

        spec_id = self.request.GET.get('spec_id')
        if spec_id:
            query = query.filter(spec_id__id__in=spec_id.split(','))
        where = self.request.GET.get('where')
        if where:
            if where != u'Найти группу':
                query = query.filter(title__icontains=where.strip())
            else:
                query = query.exclude(user_id__id=self.request.user.id)
        return query

    def get_context_data(self, **kwargs):
        context = super(GroupsList, self).get_context_data(**kwargs)
        context['mygroupscreate_list'] = Group.objects.filter(user_id__id=self.request.user.id).order_by('-createdate')
        context['mygroups_list'] = GroupUsers.objects.filter(user_id=self.request.user.id, activated=1).exclude(
            group_id__user_id__id=self.request.user.id).order_by('-group_id__createdate')
        grs = GroupUsers.objects.filter(user_id=self.request.user.id, activated=1).values('group_id')
        arr = []
        for gr in grs:
            arr.append(gr['group_id'])
        context['array_mygroups_list'] = arr
        context['title'] = 'Группы, в которых вы состоите:'
        context['path'] = self.request.path

        context['nonactivated'] = GroupUsers.objects.filter(user_id=self.request.user.id, activated=0).exclude(
            group_id__user_id__id=self.request.user.id).order_by('-group_id__createdate').count()
        # GroupUsers.objects.filter(user_id=self.request.user.id, activated=0).count()

        context['nonactivated_grouplist'] = []
        for gu in GroupUsers.objects.filter(user_id=self.request.user.id, activated=0):
            try:
                context['nonactivated_grouplist'].append(gu.group_id)
            except Group.DoesNotExist:
                pass

        context['spec'] = Specialities.objects.all()
        context['gp'] = GroupTypes.objects.all()
        context['where'] = self.request.GET.get('where')
        return context


class DetailViewGroup(DetailView):
    model = Group
    search = ''

    def get_context_data(self, **kwargs):

        if self.request.is_ajax():
            self.template_name = 'posts/posts_ajax.html'
        else:
            self.template_name = 'groups/detailgroup.html'

        context = super(DetailViewGroup, self).get_context_data(**kwargs)
        postslinks = list(set([f.post_id for f in PostLinks.objects.filter(type=15, object_id=self.object.id)]))
        search = self.request.GET.get('search')
        if postslinks:

            if search and search != u'Что ищем?':
                query = Q(content__icontains=search) | Q(title__icontains=search)
            else:
                query = Q()

            query = Posts.objects.filter(Q(id__in=postslinks) & query)

            spec_id = self.request.GET.get('spec_id')
            if spec_id:
                query = query.filter(spec_id__id__in=spec_id.split(','))

            context['object_list'] = query.order_by('-createdate')
        else:
            context['object_list'] = []
        context['path'] = self.request.path
        context['is_no_my_group'] = True
        context['show_filter'] = False
        context['show_search'] = False
        context['search'] = search
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


class ParticipantsList(ListView):
    paginate_by = '500'
    model = Group
    template_name = 'groups/participants.html'
    context_object_name = 'members'

    def get_queryset(self):
        query = Group.objects.get(id=self.kwargs['pk']).members
        return query
    def get_context_data(self, **kwargs):
        context = super(ParticipantsList, self).get_context_data(**kwargs)
        obj = Group.objects.get(id=self.kwargs['pk'])
        context['title'] = obj.title
        context['count_users'] = obj.count_users
        return context

@csrf_exempt
def avatarupload(request, sizex=0, sizey=0, groupid=0):
    # result = FileUpload(request, 'temporary', 'groups', sizex=sizex, sizey=sizey)
    result = FileUploadTo(request, ['temporary', 'post', request.user.login], int(sizex), int(sizey))
    resultjson = json.loads(result)

    img = ExtractUrlFromPath(
        CopyFileOnly(os.path.join(settings.MEDIA_ROOT, resultjson['file']), CreateFileDir(('group_images',))))

    group = Group.objects.get(pk=int(groupid))
    group.image = img
    group.save()
    return HttpResponse(json.JSONEncoder().encode(resultjson))


def join(request):
    try:
        j = GroupUsers.objects.create(user_id=request.user.id, group_id=Group(request.GET['id']), activated=1)
    except IntegrityError:
        pass
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
        if not request.user.is_staff:
            description = "<br />".join(description.split("\n"))
        object_id = data['object_id']
        service_id = 18
        if (spec_id == '0'):
            error = error + u'<p>Вы не выбрали специальность</p>'
        if (type == '0'):
            error = error + u'<p>Вы не выбрали тип материала</p>'
        if (title == u'Введите заголовок'):
            error = error + u'<p>Введите название</p>'
        if (description == u'Введите текст'):
            error = error + u'<p>Введите описание материала</p>'
        if (error == ""):
            # try:
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

            # try:
            for i, val in sorted(data['video'].iteritems()):
                basen = os.path.basename(val)
                fname = CreateFileDir(('temporary', 'post', request.user.login, 'video', basen))
                cpo = CopyFileOnly(fname, CreateFileDir(('post_images',)), no_random=True)
                vdo = ExtractUrlFromPath(cpo)
                if vdo:
                    pv = MaterialVideo()
                    pv.preview = vdo
                    pv.data = '<iframe width="430" height="315" src="//www.youtube.com/embed/' + \
                              os.path.splitext(os.path.basename(fname))[
                                  0] + '" frameborder="0" allowfullscreen></iframe>'
                    pv.service_id = Posts.SERVICE_ID
                    pv.object_id = m.id
                    pv.save()
                else:
                    m.delete()
                    service_id.delete()
                    raise ValueError('ERROR: can not save video basen=%s fname=%s vdo=%s' % (basen, fname, vdo))
            # except:
            #    return HttpResponse(u'can not create PostVideo')
            # m = Videos.objects.create(user_id=MyUser(id=request.user.id), spec_id=Specialities(id=spec_id), title=title, description=description, format=type, createdate=timezone.now() , status=1, comment_cnt=0, image=url, code='<iframe width="430" height="315" src="//www.youtube.com/embed/' + url1 + '" frameborder="0" allowfullscreen></iframe>')

            object_list = Posts.objects.filter(id=m.id)
            context = {'object_list': object_list}
            return render(request, 'posts/posts_ajax.html', context)
        else:
            context = {'error': error}
            return render(request, 'events/error.html', context)
    else:
        context = {'error': 'Ошибка передачи данных'}
        return render(request, 'events/error.html', context)
