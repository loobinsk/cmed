# -*- coding: utf-8 -*-
import json

from datetime import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from account.models import MyUser, AdditionalImage, Category, Aword
from medtus.models import Specialities, Countries, Towns
from library.models import Graduate, Title
from posts.models import Posts
from groups.models import Group, GroupUsers
from fileshandle.views import FileUploadTo, FileDelete



# Create your views here.

# @login_required
# @csrf_exempt
# def resavepass(request):
#    user = authenticate(username=request.user.email, password=request.POST['oldpassword'])
#    result = 'None'
#    if user is not None:
#        result = 'True'
#    else:
#        result = 'False'
#    return HttpResponse( json.JSONEncoder().encode({'result': result}) )

def geterror(message):
    return HttpResponse(json.JSONEncoder().encode({'result': False, 'message': message}))


# @login_required
# def lichnie2(request, userid=None):
#    context = RequestContext(request)
#    if userid is None:
#        user = request.user
#        is_owner = True
#    else:
#        try:
#            user = MyUser.objects.get(id=userid)
#            is_owner = False
#            if user is None:
#                return HttpResponse('user id=%s is not founded' % userid)
#        except MyUser.DoesNotExist:
#            return HttpResponse('user id=%s is not founded' % userid)
#    if len(user.images) > 2:
#        howmany = len(user.images) - 2
#    else:
#        howmany = 0
#    return render_to_response(
#            'lichnie/lichnie2.html',
#            {
#				'is_owner': is_owner,
#                'User': user,
#                'firstline_images': user.images[0:2],
#                'nextline_images': user.images[2:1000],
#                'howmany': howmany,
#                'object_list': Posts.objects.filter(status = 0, user_id__id = user.id).order_by('-createdate'),
#                'groups': Group.objects.filter(user_id__id=request.user.id).order_by('-createdate')
#            },
#            context)

class Profile(ListView):
    paginate_by = '5'
    # allow_empty = False
    def get_queryset(self, **kwargs):
        if self.request.is_ajax():
            self.template_name = 'posts/posts_ajax.html'
        else:
            self.template_name = 'lichnie/lichnie2.html'
        if not self.kwargs:
            user = self.request.user
            return Posts.objects.filter(status=0, user_id__id=user.id).order_by('-createdate')
        else:
            try:
                user = MyUser.objects.get(id=self.kwargs['userid'])
                is_owner = False
                return Posts.objects.filter(status=0, user_id__id=user.id).order_by('-createdate')
            except MyUser.DoesNotExist:
                return Posts.objects.filter(status=0, user_id__id=self.kwargs['userid']).order_by('-createdate')

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        is_owner = True

        if not self.kwargs:
            user = self.request.user
            context['is_owner'] = True
        else:
            try:
                user = MyUser.objects.get(id=self.kwargs['userid'])
                is_owner = False
                if user.id == self.request.user.id:
                    context['is_owner'] = True
                    context['is_id'] = 1111
                    is_owner = True
            except MyUser.DoesNotExist:
                raise Http404

        if len(user.images) > 2:
            context['howmany'] = len(user.images) - 2
        else:
            context['howmany'] = 0
        context['User'] = user
        if is_owner:
            offset = 2
        else:
            offset = 3
        context['firstline_images'] = user.images[0:offset]
        context['nextline_images'] = user.images[offset:1000]

        # Groups of current user. In this groups you CAN invite
        try:
            # been created by mine
            groups = [gr for gr in Group.objects.filter(user_id_id=self.request.user.id).order_by('-createdate')]
        except:
            groups = []

        try:
            # i'm friendship this groups
            member = [gr.group_id for gr in
                      GroupUsers.objects.filter(user_id=self.request.user.id, activated=1).order_by(
                          '-group_id__createdate')]
        except:
            member = []
        groups = groups + member

        # Groups of target User
        try:
            guest_groups = [gr for gr in Group.objects.filter(user_id_id=user.id).order_by('-createdate')]
        except:
            guest_groups = []

        try:
            guest_member = [gr.group_id for gr in GroupUsers.objects.filter(user_id=user.id)]
        except:
            guest_member = []

        guest_groups_id = [g.id for g in guest_groups + guest_member]
        context['Groups'] = list(set([g for g in groups if g.id not in guest_groups_id]))
        return context


@login_required
@csrf_exempt
def saveprofile(request):
    need_fields = ['lastname', 'firstname', 'surname', 'sex', 'birthday', 'spec_id', 'experience', 'addspeciality',
                   'addexperience', 'graduate', 'dissertation', 'title', 'addtitle', 'category', 'awords',
                   'organization', 'job', 'site', 'school', 'graduate_year', 'faculty', 'cathedra', 'country', 'town',
                   'phone_number', 'phone_visible', 'email', 'email_visible', 'ICQ_Skype', 'social']
    required_fields = ['email', 'firstname', 'lastname', 'spec_id', 'town', 'country']
    user = MyUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        if request.POST['lastname'] == '' or request.POST['firstname'] == '' or request.POST['surname'] == '':
            return HttpResponse(
                u"Firstname - {0}, surname - {1}, lastname - {2} can't be NULL!!!".format(request.POST['firstname'],
                                                                                          request.POST['lastname'],
                                                                                          request.POST['surname']))
        user.lastname = request.POST['lastname']
        user.firstname = request.POST['firstname']
        user.surname = request.POST['surname']
        if 'sex' in request.POST:
            user.sex = request.POST['sex']
        birthday = request.POST['birthday'].split('/')
        #print(birthday)
        try:
            d1 = datetime.strptime('{0} {1} {2}'.format(birthday[0], birthday[1], birthday[2]), "%d %m %Y")
            user.birthday = d1.strftime("%Y-%m-%d")
        except:
            return geterror(u'В дате рождения ошибка!!!')
        try:
            user.spec_id = Specialities.objects.get(id=request.POST['spec_id'])
        except Specialities.DoesNotExist:
            return geterror(u'Не определена специальность!!!')
        user.experience = request.POST['experience']
        try:
            user.addspeciality = Specialities.objects.get(id=request.POST['addspeciality'])
        except Specialities.DoesNotExist:
            user.addspeciality = None
        user.addexperience = request.POST['addexperience']

        if request.POST['graduate'] != '0':
            try:
                gr = Graduate.objects.get(pk=request.POST['graduate'])
                user.graduate = gr
            except Graduate.DoesNotExist:
                user.graduate = None

        user.dissertation = request.POST['dissertation']
        user.title = request.POST['title']
        user.addtitle = request.POST['addtitle']
        try:
            user.category = Category.objects.get(id=request.POST['category'])
        except:
            user.category = Category.objects.all()[:1].get()
        Aword.objects.filter(user=request.user).delete()
        awords = request.POST.getlist('awords[]')
        for value in awords:
            if value != "":
                aword = Aword(name=value, user=request.user)
                aword.save()
        user.organization = request.POST['organization']
        user.job = request.POST['job']
        user.site = request.POST['site']
        user.school = request.POST['school']
        user.graduate_year = request.POST['graduate_year']
        user.faculty = request.POST['faculty']
        user.cathedra = request.POST['cathedra']
        try:
            user.town = Towns.objects.get(id=request.POST['town'])
        except Towns.DoesNotExist:
            return geterror(u"Город не определен!!!")
        try:
            user.country = Countries.objects.get(id=request.POST['country'])
        except Countries.DoesNotExist:
            return geterror(u"Страна не определена!!!")
        user.phone_number = request.POST['phone_number']
        if 'phone_visible' in request.POST:
            user.phone_visible = 'no_visible'
        else:
            user.phone_visible = 'visible'

        if 'email_visible' in request.POST:
            user.email_visible = 'no_visible'
        else:
            user.email_visible = 'visible'
        user.ICQ_Skype = request.POST['ICQ_Skype']
        user.social = request.POST['social']
        user.save()
        return HttpResponse(json.JSONEncoder().encode({'result': True}))
    else:
        return geterror(u"Ошибка в данных!!!")


@login_required
def lichnie1(request):
    context = RequestContext(request)
    user = request.user
    try:
        birthday = user.birthday.strftime("%d%m%Y")
    except:
        d1 = datetime.strptime('01 01 1970', "%d %m %Y")
        user.birthday = d1.strftime("%Y-%m-%d")
        user.save()
        birthday = '01011970'

    if not user.country:
        user.country = Countries.objects.get(pk=1)
        user.save()

    return render(request, 'lichnie/lichnie1.html',{
            'birthday': user.birthday,
            'spec_list': Specialities.objects.all().order_by('name'),
            'addspeciality_list': Specialities.objects.all(),
            'graduate_list': Graduate.objects.all(),
            'title_list': Title.objects.all(),
            'country_list': Countries.objects.all(),
            'town_list': Towns.objects.filter(country_id=user.country.id).order_by('order', 'name'),
            'csrf_token_value': get_token(request),
            'category_list': Category.objects.all(),
        },context.flatten())


@csrf_exempt
def fileupload(request, sizex=0, sizey=0):
    result = FileUploadTo(request, ['user_image', ], int(sizex), int(sizey))
    resultjson = json.loads(result)
    if resultjson['result'] == False:
        return HttpResponse(result)
    Additional_Image = AdditionalImage()
    Additional_Image.image = resultjson['file']
    Additional_Image.user_id = request.user.id
    Additional_Image.save()
    if len(request.user.images) > 2:
        resultjson['howmany'] = len(request.user.images) - 2
    else:
        resultjson['howmany'] = 0
    return HttpResponse(json.JSONEncoder().encode(resultjson))


@csrf_exempt
def filedelete(request):
    return HttpResponse(FileDelete(request, 'user_image', ''))
