# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import ListView

from events.models import Events
from medtus.models import Specialities, Statistics, MaterialPhoto, MaterialVideo, PostLinks, Like
from photos.models import PGalleries
from posts.models import Posts
from videos.models import Videos

# from account.models import CustomUser
from django.views import generic
from django.utils import timezone
import datetime
from account.models import MyUser
import os
import re
from django.conf import settings
from PIL import Image
import json
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.template import RequestContext, loader
from comments.models import Comments
from medtus.models import Visited
from fileshandle.views import OneFileUpload
from django.db.models import Q
from django.apps import apps
from datetime import datetime, timedelta
import random


from banners.models import Banner
from banners.models import BannerGroup
from banners.models import URL


# For render tag
from django.template import Template
from random import shuffle
from random import choice
import logging



TYPE_LIST = dict([
    (u'', u'Тип материала'),
    (u'/', ['1,2,88,99', u'Главная лента Врачи Вместе - профессиональная социальная '
                                  u'сеть для врачей, образовательный портал для врачей', '0', 'Y']),
    (u'/opinion/', ['4,5,9,12', u'Частное мненией врачей портала Врачи Вместе - профессиональная социальная '
                                  u'сеть для врачей, образовательный портал для врачей', '0', 'Y']),
    (u'/lecturers/', ['1,2,4,5,9,12,88,99', u'Лекторы', '0', 'Y']),
    (u'/news/', ['1', u'Новости', '0', 'Y']),
    (u'/articles/', ['2', u'Статьи', '0', 'Y']),
    (u'/consultations/', ['3', mark_safe(u'<b>Вебинары для врачей, трансляции медицинских конференций, '
                                         u'телемосты, трансляции из операционных</b>'), '0', 'N']),
    (u'/questions/', ['4', u'Вопрос коллегам', '0', 'Y']),
    (u'/opinions/', ['5', u'Частное мнение', '0', 'Y']),
    (u'/magazines/', ['6', u'Книги и журналы', '0', 'N']),
    (u'/tranings/', ['7', u'Тренинги', '0', 'N']),
    (u'/vacancies/', ['8', u'Вакансии врача, резюме врача. Размещение материалов '
                           u'бесплатное, бессрочное. Требуется регистрация."', '0', 'N']),
    (u'/preparations/', ['9', u'Обсуждение препарата', '0', 'Y']),
    (u'/doctor/', ['11', u'Доктор с Большой Буквы', '20', 'N']),
    (u'/practice/', ['11', u'Опросы и исследования', '14', 'N']),
    (u'/clinicals/', ['12', u'Клинический случай', '0', 'Y']),
    (u'/groupsposts/', ['15', u'Публикации в группе', '21', 'Y']),
    (u'/partners/', ['50', u'Партнёры', '50', 'N'])]
)




def Partners(request, id=104):
    partners = get_object_or_404(Posts, pk=id)
    return render(request, 'posts/partners.html', {'partners': partners})

def Main(request):
    paginate_by = 10
    search = ''
    if 'search' in request.GET:
        search = request.GET['search'].strip()

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1

    object_list = []
    post_format = request.GET.get('format')
    spec_id = request.GET.get('spec_id')

    q = Q(status=0)
    queryconf = Posts.objects.filter(Q(begindate__gte = datetime.now().date())).order_by('createdate')
    queryconf = queryconf.filter(type__in='3')[:8]
    if search != u'Что ищем?' and search != '':
        q = (Q(content__icontains=search) | Q(title__icontains=search))
        query = Posts.objects.filter(q).order_by('-createdate')
        if not post_format:
            post_format = TYPE_LIST[request.path][0]

        query = query.filter(type__in=post_format.split(','))
        query = query.filter(begindate__lte = datetime.now())
        


        if spec_id:
            query = query.filter(spec_id__id__in=spec_id.split(','))

        if TYPE_LIST[request.path][2] != '0':
            postslinks = PostLinks.objects.filter(service_id=TYPE_LIST[request.path][2])
            query = query.filter(id__in=list(set([f.post_id for f in postslinks])))


        for o in query:
            object_list.append({'object': o, 'template': 'posts'})
    else:
        q = Q(status=0)
        query = Posts.objects.filter(q).order_by('-createdate')
        if not post_format:
            post_format = TYPE_LIST[request.path][0]

        query = query.filter(type__in=post_format.split(','))
        query = query.filter(Q(begindate__lte = datetime.now()) | Q(begindate__isnull=True))

        if spec_id:
            query = query.filter(spec_id__id__in=spec_id.split(','))

        if TYPE_LIST[request.path][2] != '0':
            postslinks = PostLinks.objects.filter(service_id=TYPE_LIST[request.path][2])
            query = query.filter(id__in=list(set([f.post_id for f in postslinks])))


        for o in query:
            object_list.append({'object': o, 'template': 'posts'})
        # adding group posts to list
        group_posts = Posts.objects.filter(public_main=True)

        for o in group_posts:
            object_list.append({'object': o, 'template': 'posts'})

        # если формат не задан или формат 99 (видео формат), то показываем видео в списке
        if not post_format or '99' in post_format.split(','):
            q = Q(show_medtus=1, status=1, public_main=True)
            if search != u'Что ищем?' and search != '':
                q = q & (Q(title__icontains=search) | Q(description__icontains=search))
            query = Videos.objects.filter(q).order_by('-createdate')
            if spec_id:
                query = query.filter(spec_id__id__in=spec_id.split(','))
            for o in query:
                object_list.append({'object': o, 'template': 'videos'})

        # если формат не задан или формат 88 (Мероприятия формат), то показываем Мероприятия в списке
        if not post_format or '88' in post_format.split(','):
            q = Q(public_main=True)
            if search != u'Что ищем?' and search != '':
                q = q & (Q(content__icontains=search) | Q(title__icontains=search))
            query = Events.objects.filter(q).order_by('-createdate')
            if spec_id:
                query = query.filter(spec_id__id__in=spec_id.split(','))
            for o in query:
                object_list.append({'object': o, 'template': 'events'})

        # если формат не задан, то показываем галерею в списке
        if not request.GET.get('format', None) and not spec_id:
            q = Q(status=1, public_main=True)
            if search != u'Что ищем?' and search != '':
                q = q & (Q(title__icontains=search) | Q(description__icontains=search))
            query = PGalleries.objects.filter(q).order_by('-createdate')
            if spec_id:
                query = query.filter(spec_id__id__in=spec_id.split(','))
            for o in query:
                object_list.append({'object': o, 'template': 'photos'})

    # trying to sort result by createdate
    try:
        object_list.sort(key=lambda x: x['object'].createdate, reverse=True)
    except:
        pass
    p = Paginator(object_list, paginate_by)
    


    queryvid = Videos.objects.filter(show_medtus=1, status=1).order_by('-id')[:8]
    context = RequestContext(request)
    context['object_list'] = p.page(page)
    context['videos_list'] = queryvid
    context['conf_list'] = queryconf
    context['request'] = request



     # Начало баннеры
    try:
        page_url = context['request'].path_info
        
        group = BannerGroup.objects.get(slug='right_side')
        context['my'] = False
        good_urls = []

        for url in URL.objects.filter(public=True):
            
            if url.regex:
                url_re = re.compile(url.url)
                
                if url_re.findall(page_url):

                    good_urls.append(url)                  
            elif page_url == url.url:
                good_urls.append(url)

        banners_all = Banner.objects.filter(public=True, group=group, urls__in=good_urls)

        banners = [banner for banner in banners_all if banner.often == 10]

        banners_ids = [x for y in [[banner.id] * banner.often for banner in banners_all if banner.often < 10] for x in y]
        if(banners_ids):
            shuffle(banners_ids);
            banner_id = choice(banners_ids)
            banners.append([el for el in banners_all if el.id == banner_id][0])
    except:
        banners = False
        group = False
    if (banners and group):
        context['banners1'] = banners
        context['group1'] = group
        # Конец баннеры


        
    if request.is_ajax():
        template = 'posts/main_ajax.html'
        context['page'] = page
    else:
        template = 'posts/main.html'
        title = TYPE_LIST[request.path][1]
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['title'] = title
        context['path'] = request.path
        context['page'] = page
        context['search'] = search
        context['the_path'] = request.path
        context['isfilter'] = TYPE_LIST[request.path][3]
    return render(request,template,context.flatten())

def Opinion(request):
    paginate_by = 5
    search = ''
    if 'search' in request.GET:
        search = request.GET['search'].strip()

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1

    object_list = []
    post_format = request.GET.get('format')
    spec_id = request.GET.get('spec_id')
    if search != u'Что ищем?' and search != '':
        q = (Q(content__icontains=search) | Q(title__icontains=search))
        query = Posts.objects.filter(q).order_by('-createdate')
        if not post_format:
            post_format = TYPE_LIST[request.path][0]

        query = query.filter(type__in=post_format.split(','))


        if spec_id:
            query = query.filter(spec_id__id__in=spec_id.split(','))

        if TYPE_LIST[request.path][2] != '0':
            postslinks = PostLinks.objects.filter(service_id=TYPE_LIST[request.path][2])
            query = query.filter(id__in=list(set([f.post_id for f in postslinks])))
        
        for o in query:
            object_list.append({'object': o, 'template': 'posts'})
    else:
        q = Q(status=0)
        query = Posts.objects.filter(q).order_by('-createdate')
        if not post_format:
            post_format = TYPE_LIST[request.path][0]

        query = query.filter(type__in=post_format.split(','))


        if spec_id:
            query = query.filter(spec_id__id__in=spec_id.split(','))

        if TYPE_LIST[request.path][2] != '0':
            postslinks = PostLinks.objects.filter(service_id=TYPE_LIST[request.path][2])
            query = query.filter(id__in=list(set([f.post_id for f in postslinks])))


        for o in query:
            object_list.append({'object': o, 'template': 'posts'})
        # adding group posts to list
        # group_posts = Posts.objects.filter(public_main=True)

        # for o in group_posts:
        #     object_list.append({'object': o, 'template': 'posts'})

        # если формат не задан или формат 99 (видео формат), то показываем видео в списке
        if not post_format or '99' in post_format.split(','):
            q = Q(show_medtus=1, status=1, public_main=True)
            if search != u'Что ищем?' and search != '':
                q = q & (Q(title__icontains=search) | Q(description__icontains=search))
            query = Videos.objects.filter(q).order_by('-createdate')
            if spec_id:
                query = query.filter(spec_id__id__in=spec_id.split(','))
            for o in query:
                object_list.append({'object': o, 'template': 'videos'})

        # если формат не задан или формат 88 (Мероприятия формат), то показываем Мероприятия в списке
        if not post_format or '88' in post_format.split(','):
            q = Q(public_main=True)
            if search != u'Что ищем?' and search != '':
                q = q & (Q(content__icontains=search) | Q(title__icontains=search))
            query = Events.objects.filter(q).order_by('-createdate')
            if spec_id:
                query = query.filter(spec_id__id__in=spec_id.split(','))
            for o in query:
                object_list.append({'object': o, 'template': 'events'})

        # если формат не задан, то показываем галерею в списке
        if not request.GET.get('format', None) and not spec_id:
            q = Q(status=1, public_main=True)
            if search != u'Что ищем?' and search != '':
                q = q & (Q(title__icontains=search) | Q(description__icontains=search))
            query = PGalleries.objects.filter(q).order_by('-createdate')
            if spec_id:
                query = query.filter(spec_id__id__in=spec_id.split(','))
            for o in query:
                object_list.append({'object': o, 'template': 'photos'})

    # trying to sort result by createdate
    object_list.sort(key=lambda x: x['object'].createdate, reverse=True)
    p = Paginator(object_list, paginate_by)
    

    context = {
        'object_list': p.page(page),
        "request":request,
    }
    if request.is_ajax():
        template = loader.get_template('posts/main_ajax.html')
        context['page'] = page
    else:
        template = loader.get_template('posts/opinion.html')
        title = TYPE_LIST[request.path][1]
        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['title'] = title
        context['path'] = request.path
        context['page'] = page
        context['search'] = search
        context['the_path'] = request.path
        context['isfilter'] = TYPE_LIST[request.path][3]
    return HttpResponse(template.render(context))


class PostsList(ListView):
    paginate_by = '5'
    search = ''    

    def dispatch(self, request, *args, **kwargs):
        if self.request.path == '/posts/':
            return HttpResponseRedirect('/')
        else:
            return super(PostsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
        if self.search != u'Что ищем?' and self.search != '':
            query = Posts.objects.filter(Q(content__icontains=self.search) | Q(title__icontains=self.search))
            #query = Q(content__icontains=self.search) | Q(title__icontains=self.search)
        else:
            # query = Posts.objects.filter(Q(status=0)).order_by('-createdate')            
            if TYPE_LIST[self.request.path][0] == '3':
               query = Posts.objects.filter(Q(status=0)).order_by('createdate')
            else:
               query = Posts.objects.filter(Q(status=0)).order_by('-createdate')

        # Календарь       
        if TYPE_LIST[self.request.path][0] == '3' and 'date' in self.request.GET:
            try:
                start_date = datetime.strptime(self.request.GET['date'] + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(self.request.GET['date'] + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                query = Posts.objects.filter(begindate__gte = start_date, begindate__lte = end_date).order_by('createdate')
            except (ValueError, TypeError):
                raise Http404
                        


        if self.request.is_ajax():
            self.template_name = 'posts/posts_ajax.html'
        else:
            self.template_name = 'posts/posts.html'

        if TYPE_LIST[self.request.path][0] != '6' and 'archive' in self.request.GET:
            query = query.filter(archive=1)
        else:
            query = query.filter(archive=0)

        format = self.request.GET.get('format')
        if format:
            query = query.filter(type__in=format.split(','))
        else:
            query = query.filter(type__in=TYPE_LIST[self.request.path][0].split(','))
        spec_id = self.request.GET.get('spec_id')
        if spec_id:
            query = query.filter(spec_id__id__in=spec_id.split(','))
        if TYPE_LIST[self.request.path][2] != '0':
            postslinks = PostLinks.objects.filter(service_id=TYPE_LIST[self.request.path][2])
            query = query.filter(id__in=list(set([f.post_id for f in postslinks])))
        return query

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostsList, self).get_context_data(**kwargs)
        # Add in the publisher
        title = TYPE_LIST[self.request.path][1]
        page_id = TYPE_LIST[self.request.path][0]

        if not self.request.user.is_anonymous:
            from account.models import EventAccess
            EventAccess.update("posts" + page_id, self.request.user)

        context['specialities_list'] = Specialities.objects.all().order_by('name')
        context['title'] = title

        if self.request.GET.get('archive') == '':
            context['title'] = context['title'] + u'. Архив'

        if TYPE_LIST[self.request.path][0] == '3' and 'date' in self.request.GET:
            context['date_param'] = self.request.GET['date']
        else:
            context['date_param'] = ''

        context['path'] = self.request.path
        context['search'] = self.search
        context['id'] = page_id
        if page_id in ('3', '6', '8',):
            context['show_filter'] = False
            if page_id != '8':
                context['show_search'] = False
            else:
                context['show_search'] = True

        context['archive_url'] = self.request.path + '?archive=true'
        if page_id in ('3',) and self.request.GET.get('archive') == None:
            context['show_archive'] = True
        if page_id in ('8',) and self.request.GET.get('archive') == None:
            context['show_archive'] = True  

        return context


class DetailViewPost(generic.DetailView):
    model = Posts
    template_name = 'posts/detailpost.html'
    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailViewPost, self).get_context_data(**kwargs)
        # Add in the publisher
        if self.get_object().type == 15:
            from groups.models import Group
            groups_id = PostLinks.objects.filter(type=15, post_id=self.kwargs['pk']).values_list('object_id', flat=True)
            context['groups'] = Group.objects.filter(pk__in=groups_id)

        statistics = Statistics.objects.filter(material_id=self.kwargs['pk'], service_id=18)

        if 'text' in self.request.META['HTTP_ACCEPT']:
            if statistics:
                statistics[0].viewings = statistics[0].viewings + 1
                statistics[0].save()
                context['viewings'] = statistics[0].viewings
            else:
                Statistics.objects.create(material_id=self.kwargs['pk'], service_id=18, viewings=1)
                context['viewings'] = 1
        
        # logger = logging.getLogger(__name__)
        # logger.error('Load bof')
        # logger.error(context['viewings'])
        # logger.error('Load eof')
        Visited.record(self.get_object())
        return context


class DeletePost(generic.DeleteView):
    model = Posts
    template_name = 'posts/detailpost_delete.html'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.user_id.id == request.user.id or request.user.is_staff:
            return super(DeletePost, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotFound()

    def get_success_url(self):
        links = self.object.groups
        if len(links) > 0:
            link = links[0].object_id
            [x.delete() for x in links]
            return reverse('detailgroup', kwargs=dict(pk=link))


def like(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    user_id = str(request.user.id)
    try:
        Object_Id = int(request.GET.get('id'))
        Service_Id = int(request.GET.get('service_id'))
    except (ValueError, TypeError):
        raise Http404
    try:
        if request.GET['service_id'] == 9999:
            comment = Comments(id=request.GET['id'])
            Object_Id = comment.object_id
            Service_Id = comment.service_id
        Like.objects.get_or_create(material_id=Object_Id, service_id=Service_Id, user=request.user)
    except:
        pass
    statistics = Statistics.objects.filter(material_id=request.GET['id'], service_id=request.GET['service_id'])
    if statistics:
        likes = (statistics[0].likes).split(' ')
        if user_id in likes:
            likes.remove(user_id)
            Like.objects.filter(user__id=user_id, material_id=request.GET['id']).delete()
        else:
            likes.append(user_id)
        statistics[0].likes = ' '.join(likes)
        statistics[0].save()
    else:
        Statistics.objects.create(material_id=request.GET['id'], service_id=request.GET['service_id'], viewings=0,
                                  likes=user_id)
        statistics = Statistics.objects.filter(material_id=request.GET['id'], service_id=request.GET['service_id'])
    context = {'likes': statistics[0].likes}
    return render(request, 'posts/likes.html', context)


def addpost(request):
    if request.POST:
        error = ""
        spec_id = request.POST['data[spec_id]']
        type = request.POST['data[type]']
        title = request.POST['data[title]']
        description = request.POST['data[description]']
        
        try:
            begindate = request.POST['data[begindate]']
        except:
            begindate = ''

        if (begindate == ''):
            begindate = timezone.now()
        else:
            begindate = datetime.strptime(begindate, "%Y-%m-%d %H:%M:%S")
        if (spec_id == '0'):
            error = error + u'<p>Вы не выбрали специальность</p>'
        if (type == '0'):
            error = error + u'<p>Вы не выбрали тип материала</p>'
        if (title == u'Введите заголовок'):
            error = error + u'<p>Введите название</p>'
        if (re.sub(ur'<p>(Введите текст|&nbsp;| )*<\/p>', '', description).strip() == ''):
            error = error + u'<p>Введите описание материала</p>'
        if (error == ""):
            if (not request.user.is_staff):
                description = "<br/>".join(description.split("\n"))
            m = Posts.objects.create(user_id=MyUser(id=request.user.id), spec_id=Specialities(id=spec_id), title=title,
                                     content=description, type=type,
                                     createdate=timezone.now(), status=0, comment_cnt=0, begindate = begindate)

            # if type == u'11':
            #     service_id = PostLinks.objects.create(service_id=14, type=type, post_id=m.id,
            #                                           object_id=8)
            media = dict()
            media['photo'] = {}
            media['video'] = {}
            # try:
            index = 0
            while request.POST.get('data[photo][%s]' % index, False):
                val = request.POST['data[photo][%s]' % index]
                key = index
                index = index + 1
                src = os.path.join(settings.MEDIA_ROOT, val)
                result = OneFileUpload(file(src), ['post_images', ])
                resultjson = json.loads(result)
                if resultjson['result'] == False:
                    return HttpResponse("Error!!!:" + resultjson['message'])
                if resultjson['result'] == True:
                    media['photo'][key] = {}
                    media['photo'][key]['photo'] = resultjson['file']
                    media['photo'][key]['thumb'] = resultjson['url']
            index = 0
            while request.POST.get('data[video][%s]' % index, False):
                val = request.POST['data[video][%s]' % index]
                key = index
                index = index + 1
                src = settings.PUBLIC_HTML_ROOT + val
                dst = os.path.join(settings.MEDIA_ROOT, 'post_images', os.path.basename(val))
                im = Image.open(src)
                im.save(dst, "JPEG")
                media['video'][key] = {}
                media['video'][key]['video'] = dst
            # except:
            #    return HttpResponse(json.JSONEncoder().encode({'message': u'can not save files % s' % sys.exc_info()[0] , 'result': False}))
            # try:
            for key, val in sorted(media['photo'].iteritems()):
                pp = MaterialPhoto()
                url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['photo']))
                pp.picture = url
                url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['thumb']))
                pp.thumb = url
                pp.service_id = Posts.SERVICE_ID
                pp.object_id = m.id
                pp.save()
            # except:
            #    return HttpResponse(json.JSONEncoder().encode({'message': u'can not create PostPhoto' , 'result': False}))
            # try:
            for key, val in sorted(media['video'].iteritems()):
                pv = MaterialVideo()
                url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['video']))
                url1 = os.path.basename(val['video'])
                pv.preview = url
                video = val['video'].split(".")
                video.pop()
                pv.data = '<iframe width="430" height="315" src="//www.youtube.com/embed/' + os.path.basename(
                    ".".join(video)) + '" frameborder="0" allowfullscreen></iframe>'
                pv.service_id = Posts.SERVICE_ID
                pv.object_id = m.id
                pv.save()
            # except:
            #    return HttpResponse(json.JSONEncoder().encode({'message': u'can not create PostVideo' , 'result': False}))

            return HttpResponse(json.JSONEncoder().encode({'result': True}))
        else:
            return HttpResponse(json.JSONEncoder().encode({'message': error, 'result': False}))
    else:
        return HttpResponse(json.JSONEncoder().encode({'message': 'error POST query!', 'result': False}))


def rmpost(request):
    if request.method != 'POST':
        raise Http404
    post_id = request.POST.get('post_id')
    post_type = request.POST.get('type')
    if post_type == 'photo':
        model_type = apps.get_model('photos', 'PGalleries')
    elif post_type == 'video':
        model_type = apps.get_model('videos', 'Videos')
    else:
        model_type = apps.get_model('posts', 'Posts')
    post = get_object_or_404(model_type, pk=post_id)
    time_left = (timezone.now() - post.createdate).seconds < getattr(settings, 'POST_DELETION_TIME', 30) * 60

    if post_type == 'photo' and post.user != request.user \
            or post_type != 'photo' and post.user_id != request.user \
            or not time_left:
        return HttpResponse('error')
    post.delete()
    return HttpResponse('OK')
