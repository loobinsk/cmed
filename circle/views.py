# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.template.loader import render_to_string

from account.models import MyUser, AllMsg
from groups.models import Group
from medtus.models import Countries, Towns, PostLinks, Specialities
from circle.models import Dialog, Record, Circle
from events.models import Events
from photos.models import PGalleries
from posts.models import Posts
from videos.models import Videos
from records.models import Records
from medtus.models import Like

import re

def get_object(ID, service_id=0):
    try:
        if service_id == 10:
            return {'o': Videos.objects.filter(id=ID).order_by('-createdate'), 'n': 'object_list',
                    't': 'videos/videos_ajax.html'}  #
        if service_id == 18:
            return {'o': Posts.objects.filter(id=ID).order_by('-createdate'), 'n': 'object_list',
                    't': 'posts/posts_ajax.html'}  #
        if service_id == 6:
            return {'o': Events.objects.filter(id=ID).order_by('-createdate'), 'n': 'object_list',
                    't': 'events/events_ajax.html'}  #
        if service_id == 11:
            return {'o': PGalleries.objects.filter(id=ID).order_by('-createdate'), 'n': 'object_list',
                    't': 'photos/photo_ajax.html'}  #
        if service_id == 23:
            return {'o': Records.objects.filter(id=ID).order_by('-createdate'), 'n': 'object_list',
                    't': 'records/records_ajax.html'}
    except:
        pass


def interesting(request):
    likes = Like.objects.filter(user__id=request.user.id).order_by('-createdate')
    el = {}
    out = ''
    for l in likes:
        e = get_object(l.material_id, l.service_id)
        if e is not None and e['o'].count() != 0 and not (l.material_id in el):
            group_id = PostLinks.objects.filter(post_id=l.material_id, service_id=l.service_id)
            group = ''
            if group_id.exists():
                group = Group.objects.get(pk=group_id[0].object_id)
            out = out + render_to_string(e['t'], {e['n']: e['o'], 'user': request.user, 'circle': True, 'group': group})
            el[l.material_id] = e

    if request.is_ajax():
        template = 'circle/interesting_ajax.html'
    else:
        template = 'circle/interesting.html'

    return render(request, template, {'out': out})


def get_user_owner(_self):
    if not _self.kwargs:
        user = _self.request.user
        is_owner = True
    else:
        try:
            user = MyUser.objects.get(id=_self.kwargs['userid'])
            is_owner = False
            if user is None:
                return {'result': False, 'response': HttpResponse('user id=%s is not founded' % userid)}
        except MyUser.DoesNotExist:
            return {'result': False, 'response': HttpResponse('user id=%s is not founded' % userid)}
    return {'result': True, 'user': user, 'is_owner': is_owner}


class MyCircleView(generic.ListView):
    template_name = 'circle/MyCircle.html'
    model = Circle
    context_object_name = 'mycircle'

    def get_queryset(self, **kwargs):
        return Circle.objects.filter(Q(parent=self.request.user) | Q(friend=self.request.user)).exclude(activated=0)

    def get_context_data(self, **kwargs):
        context = super(MyCircleView, self).get_context_data(**kwargs)
        if not self.kwargs:
            user = self.request.user
            context['is_owner'] = True
        else:
            try:
                user = MyUser.objects.get(id=self.kwargs['userid'])
                context['is_owner'] = False
                if user is None:
                    return HttpResponse('user id=%s is not founded' % self.kwargs['userid'])
            except MyUser.DoesNotExist:
                return HttpResponse('user id=%s is not founded' % self.kwargs['userid'])
        context['User'] = user
        context['invite'] = Circle.objects.filter(Q(parent=user) & Q(activated=False))
        context['invited'] = Circle.objects.filter(Q(friend=user) & Q(activated=False))
        context['circle'] = []
        context['is_id'] = self.request.user.id
        for value in Circle.objects.filter(Q(parent=user.id) | Q(friend=user.id)).exclude(activated=0):
            # .exclude(friend=self.request.user):
            try:
                if value.parent == user:
                    u = value.friend
                else:
                    u = value.parent
                if context['circle'].count(u) == 0:
                    context['circle'].append(u)
            except MyUser.DoesNotExist:
                pass
        return context


class AllDialogsView(generic.ListView):
    template_name = 'circle/AllDialogs.html'
    model = Dialog
    context_object_name = 'dialogsrecords'

    def get_context_data(self, **kwargs):
        from django.core.paginator import EmptyPage, PageNotAnInteger

        context = super(generic.ListView, self).get_context_data(**kwargs)

        objects = self.object_list
        # for o in self.object_list:
        #     try:
        #          # if o.authA and o.authB:
        #          objects.append(o)
        #     except MyUser.DoesNotExist:
        #         pass

        paginator = self.paginator_class(objects, 20)

        page = self.request.GET.get('page')
        try:
            dialogs = paginator.page(page)
        except PageNotAnInteger:
            dialogs = paginator.page(1)
        except EmptyPage:
            dialogs = paginator.page(paginator.num_pages)

        context['page_obj'] = dialogs


        msg=''
        try:
            msg=AllMsg.objects.get(user=self.request.user, type=0)
        except:
            pass
        if msg != '':
            context['all_msgs'] = msg

        return context


    def get_queryset(self, **kwargs):
        return self.get_dialogs()

    def get_dialogs(self):
        q1 = Q(authA=self.request.user, auth_a_deleted=0)

        q2 = Q(authB=self.request.user, auth_b_deleted=0)
        dialogs = Dialog.objects.filter(q1 | q2)

        return sorted(dialogs, key=lambda p: p.lastrecord.createdate if p.lastrecord else timezone.now(), reverse=True)


class NmoDialogsView(generic.ListView):
    template_name = 'circle/NmoDialogs.html'
    model = Dialog

    def get_context_data(self, **kwargs):
        from django.core.paginator import EmptyPage, PageNotAnInteger

        context = super(generic.ListView, self).get_context_data(**kwargs)

        objects = self.object_list
        # for o in self.object_list:
        #     try:
        #          # if o.authA and o.authB:
        #          objects.append(o)
        #     except MyUser.DoesNotExist:
        #         pass

        paginator = self.paginator_class(objects, 20)

        page = self.request.GET.get('page')
        try:
            dialogs = paginator.page(page)
        except PageNotAnInteger:
            dialogs = paginator.page(1)
        except EmptyPage:
            dialogs = paginator.page(paginator.num_pages)

        context['page_obj'] = dialogs


        msg=''
        try:
            msg=AllMsg.objects.get(user=self.request.user, type=1)
        except:
            pass
        if msg != '':
            context['all_msgs'] = msg

        return context




class AdminDialogView(generic.ListView):
    template_name = 'circle/AdminDialog.html'
    model = Record
    context_object_name = 'all_msgs'

    def get_queryset(self, **kwargs):
        msg=''
        try:
            msg=AllMsg.objects.get(user=self.request.user, type=0)
        except:
            pass
        if msg != '':
            msg.unreaded=0
            msg.save()
            return msg
        return ''


class NmoDialogView(generic.ListView):
    template_name = 'circle/NmoDialog.html'
    model = Record
    context_object_name = 'all_msgs'

    def get_queryset(self, **kwargs):
        msg=''
        try:
            msg=AllMsg.objects.get(user=self.request.user, type=1)
        except:
            pass
        if msg != '':
            msg.unreaded=0
            msg.save()
            return msg
        return ''


class DialogView(generic.ListView):
    template_name = 'circle/Dialog.html'
    model = Record
    context_object_name = 'dialogrecords'

    def get_queryset(self, **kwargs):
        authA = MyUser.objects.get(id=self.request.user.id)
        authB = MyUser.objects.get(id=self.kwargs['authBid'])
        return self.getrecords(authA, authB)

    def getrecords(self, authA, authB):
        D = self.getDialog(authA, authB)
        if D is None:
            return None
        else:
            for R in Record.objects.filter(dialog=D, auth=authB):
                R.viewed = datetime.now()
                R.save()
            return Record.objects.filter(dialog=D).order_by('createdate')

    def in_online(self, authB, request):
        if authB in request.online_now:
            return u'Сейчас в сети'
        else:
            return u'Сейчас не в сети'

    def getDialog(self, authA, authB):
        q1 = Q(authA_id=authA.id)
        q2 = Q(authB_id=authB.id)
        q11 = Q(authA_id=authB.id)
        q22 = Q(authB_id=authA.id)
        try:
            D = Dialog.objects.get(q1 & q2)
        except Dialog.DoesNotExist:
            D = None
        if D is None:
            try:
                D = Dialog.objects.get(q11 & q22)
            except Dialog.DoesNotExist:
                D = None
        return D


    def get_context_data(self, **kwargs):
        context = super(DialogView, self).get_context_data(**kwargs)
        authB = MyUser.objects.get(id=self.kwargs['authBid'])
        context['authBid'] = self.kwargs['authBid']
        context['authB'] = authB
        context['online_now'] = self.in_online(authB, self.request)
        return context

    def post(self, request, *args, **kwargs):
        authA = MyUser.objects.get(id=self.request.user.id)
        authB = MyUser.objects.get(id=self.request.POST['authBid'])
        D = self.getDialog(authA, authB)
        if D is None:
            D = Dialog()
            D.authA = authA
            D.authB = authB
            D.save()
        R = Record()
        R.value = self.request.POST['text']
        R.auth = self.request.user
        R.dialog = D
        d1 = datetime.strptime('01 01 1970', "%d %m %Y")
        R.viewed = d1.strftime("%Y-%m-%d")
        R.moderated = False
        R.save()
        return render(request, self.template_name,
                      {'authBid': authB.id, 'authB': authB, 'online_now': self.in_online(authB, self.request),
                       'dialogrecords': self.getrecords(authA, authB)})



class InviteView(generic.ListView):
    paginate_by = '5'
    template_name = 'circle/InviteIntoMyCircle.html'
    context_object_name = 'lookingfor'
    model = MyUser
    params = ['firstname', 'lastname', 'surname', 'country', 'town', 'school', 'job', 'birthday']

    def get_queryset(self):
        if self.request.is_ajax():
            self.template_name = 'circle/invite_ajax.html'
        else:
            self.template_name = 'circle/InviteIntoMyCircle.html'
        return MyUser.objects.filter(self.createquery(self.request.GET))

    def get_context_data(self, **kwargs):
        context = super(InviteView, self).get_context_data(**kwargs)
        for k in self.params:
            self.request.session[k] = ''
        context['session'] = self.request.session
        context['circle'] = self.getmycircle()
        context['specs'] = Specialities.objects.all().order_by('title')

        return context

    def getmycircle(self):
        circle = []
        for value in Circle.objects.filter(Q(parent=self.request.user.id) | Q(friend=self.request.user.id)).exclude(
                activated=0):
            try:
                if value.parent == self.request.user:
                    u = value.friend
                else:
                    u = value.parent
                if circle.count(u) == 0:
                    circle.append(u)
            except MyUser.DoesNotExist:
                pass
        return circle[0:3]

    def createquery(self, indata):
        try:
            Country = Countries.objects.get(title__iexact=indata['country'])
        except Countries.DoesNotExist:
            Country = None
        except MultiValueDictKeyError:
            return Q()
        try:
            Town = Towns.objects.filter(name__iexact=indata['town'])
        except Towns.DoesNotExist:
            Town = None
        try:
            Birthday = datetime.datetime.strptime(u'%s' % indata['birthday'], '%d-%m-%y').date()
        except:
            Birthday = None

        data = {'firstname': Q(firstname__icontains=indata['firstname'].strip()),
                'lastname': Q(lastname__icontains=indata['lastname'].strip()),
                'surname': Q(surname__icontains=indata['surname'].strip()), 'country': Q(country__title=Country),
                'town': Q(town__in=Town), 'school': Q(school=indata['school'].strip()),
                'job': Q(spec_id=indata['job'].strip()), 'birthday': Q(birthday=Birthday)}
        placeholders = [u'Имя', u'Фамилия', u'Отчество', u'Страна', u'Город', u'Место учебы', u'Место работы',
                        u'День рождения']
        dataIsNone = {'country': Country, 'town': Town}

        query = Q()
        for k, v in data.iteritems():
            if k in dataIsNone:
                if dataIsNone[k] is None:
                    continue
            if indata[k] != '' and not (indata[k] in placeholders):
                if query is None:
                    query = v
                else:
                    query = query & v
        return query & ~Q(id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        user_owner = get_user_owner(self)
        if not user_owner['result']:
            return user_owner['response']
        query = self.createquery(request.POST)
        users = MyUser.objects.filter(query)[0:5]
        count = MyUser.objects.filter(query).count()
        for k, v in request.POST.iteritems():
            self.request.session[k] = v

        if self.request.session.get('job'):
            self.request.session['job'] = int(self.request.session.get('job'))
        return render(request, self.template_name, {
            'lookingfor': users,
            'count': count,
            'circle': self.getmycircle(),
            'session': self.request.session,
            'specs': Specialities.objects.all().order_by('title')
        })
