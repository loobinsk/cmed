# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
import os
import json
import re

from django.db.models import Count
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.utils import timezone

from quiz.models import Quiz
from account.forms import RegisterStep1Form, RegisterStep2Form, RegisterStep3Form
from .models import MyUser, AdditionalImage, AllMsg
from medtus.models import Specialities, Towns, Countries
from cuter.cuter import resize_and_crop
from fileshandle.views import FileUploadTo

size = settings.AVATAR_SIZE
logger = logging.getLogger(__name__)

step2_form = ""


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainpage'))


def user_login(request):
    context = RequestContext(request)
    error = ''
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
        except (MultipleObjectsReturned, UnicodeEncodeError):
            user = None
        if user is not None:
            # Need to delete password restore tokens if user logined in with default password
            from models import PassToken
            token = PassToken.objects.filter(user=user)
            if token.exists():
                for t in token:
                    t.delete()
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                if request.META.get('HTTP_REFERER', False) and 'account/login' not in request.META.get('HTTP_REFERER'):
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Medtus account is disabled.")

        else:
            # Bad login details were provided. So we can't log the user in.
            error = u'<span class="inform-error">Логин или пароль ошибочны!  ' \
                    u'<br>попробуйте ввести пароли еще раз.</span>'
    return render_to_response(
        'account/login.html',
        {'error': error},
        context)


def password_forgot(request, **kwargs):
    context = RequestContext(request)
    error = ''
    if request.method == 'POST':
        email = request.POST['email']
        user = MyUser.objects.filter(email=email)
        if user.exists():
            if user.first().is_active:
                from models import PassToken
                import string
                import random
                token_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                                       for _ in range(24))
                token = PassToken.objects.get_or_create(user=user.first())[0]
                token.token = token_string
                token.save()

                from settings.views import send_email
                send_email(request, email, 'forgot_email', u'Восстановление пароля на vrvm.ru', token=token.token)

                return render_to_response(
                    'account/forgot.html',
                    {
                        'error': error,
                        'sent': True
                    },
                    context
                )
            else:
                error = u'Аккаунт не активен'
        else:
            error = u'Аккаунта с такой почтой у нас нет.'

        return render_to_response(
            'account/forgot.html',
            {'error': error},
            context
        )
    else:
        return render_to_response(
            'account/forgot.html',
            {'error': error},
            context
        )


def password_change(request, **kwargs):
    from models import PassToken
    from datetime import timedelta
    from django.utils import timezone
    from django.core.urlresolvers import reverse

    context = RequestContext(request)
    params = {'error': '', 'token': kwargs.get('token', ''), 'show_form': True}
    token = PassToken.objects.filter(token=kwargs.get('token'))
    fift_min_ago = timezone.now() - timedelta(minutes=120)

    if token.exists():
        if token.first().time > fift_min_ago:
            if request.method == 'POST':
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                if password1 != password2:
                    params['error'] = u'Пароли должны совпадать'
                else:
                    import re
                    p = re.compile(ur'[a-z\d]+', re.UNICODE | re.IGNORECASE)
                    if re.search(p, password1):
                        user = token.first().user
                        user.set_password(password1.encode('utf-8'))
                        user.save()

                        from settings.views import send_email
                        send_email(request, user.email, 'passchange_email', u'Ваш пароль изменен',
                           profile=user, password=password1.encode('utf-8'))

                        token.first().delete()
                        params['error'] = u'Пароль успешно изменен <a href="{url}">Войти</a>'.format(url=reverse('login'))
                        params['show_form'] = False
                    else:
                        params['error'] = u'В пароле доступны только символы A-Z и 0-9'
        else:
            params['error'] = u'Ссылка не действительна. Запросите ссылку еще раз'
            params['show_form'] = False
            token.first().delete()
    else:
        params['show_form'] = False
        params['error'] = u'Ссылка не действительна. <a href="{url}">Запросите ссылку еще раз</a>'.format(url=reverse('forgot'))

    return render_to_response(
        'account/change.html',
        params,
        context
    )


def agreement(request):
    import settings.models as s
    on = s.Settings.objects.all()[:1]
    content = ""
    if on.exists():
        content = on[0].agreement

    context = RequestContext(request)

    return render_to_response(
        'account/agreement.html',
        {'content': content},
        context)


def register1(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account.views.register4'))
    if request.method == 'POST':
        step1_form = RegisterStep1Form(data=request.POST)
        if step1_form.is_valid(request):
            return HttpResponseRedirect(reverse('account.views.register2'))
    else:
        step1_form = RegisterStep1Form()
    # Render the template depending on the context.
    return render_to_response(
        'account/register.html',
        {'register_form': step1_form.render(request), 'step1_active': 'active', 'step': 1},
        context)


def register2(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account.views.register4'))
    step2_form = RegisterStep2Form()
    if request.method == 'POST':
        step2_form = RegisterStep2Form(data=request.POST)
        if step2_form.is_valid(request):
            return HttpResponseRedirect(reverse('account.views.register3'))
    else:
        step2_form = RegisterStep2Form()
    # Render the template depending on the context.
    return render_to_response(
        'account/register.html',
        {'register_form': step2_form.render(request), 'step1_active': 'active', 'step2_active': 'active', 'step': 2},
        context)


def register3(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account.views.register4'))
    step3_form = RegisterStep3Form()
    if request.method == 'POST':
        step3_form = RegisterStep3Form(data=request.POST)
        if step3_form.is_valid(request):
            if MyUser.objects.filter(email=request.session['email']):
                email = request.session['email']
                request.session.clear()
                return HttpResponse("Login %s is already into database. <a href='%s'>Please re-enter login</a>" %
                                    (email, reverse('account.views.register1')))
            profile = MyUser()
            profile.email = request.session['email']
            profile.login = request.session['email']
            profile.surname = request.session['surname']
            profile.firstname = request.session['firstname']
            profile.lastname = request.session['lastname']

            try:
                profile.spec_id = Specialities.objects.get(id=request.session['spec_id'])
            except Specialities.DoesNotExist:
                profile.spec_id = None
            try:
                profile.town = Towns.objects.get(id=request.session['town'])
            except Towns.DoesNotExist:
                profile.town = None
            try:
                profile.country = Countries.objects.get(id=request.session['country'])
            except Countries.DoesNotExist:
                profile.country = None
            profile.avatar = request.session['avatar']
            profile.sex = request.session['sex']

            birthday = request.session['birthday'].split()
            if birthday:
                d1 = datetime.strptime('{0} {1} {2}'.format(birthday[0], birthday[1], birthday[2]), "%d %m %Y")
                profile.birthday = d1.strftime("%Y-%m-%d")


            profile.experience = request.session['experience']
            try:
                profile.addspeciality = Specialities.objects.get(id=request.session['addspeciality'])
            except Specialities.DoesNotExist:
                profile.addspeciality = None
            profile.addexperience = request.session['addexperience']
            from library.models import Graduate
            try:
                grad = Graduate.objects.get(pk=request.session['graduate'])
                profile.graduate = grad
            except Graduate.DoesNotExist:
                profile.graduate = None

            profile.dissertation = request.session['dissertation']
            profile.title = request.session['title']
            profile.addtitle = request.session['addtitle']

            try:
                from account.models import Category
                cat = Category.objects.get(pk=request.session['category'])
                profile.category = cat
            except Category.DoesNotExist:
                profile.category = None

            profile.awords = None
            profile.organization = request.session['organization']
            profile.job = request.session['job']
            profile.site = request.session['site']
            if not request.session['school'] and request.session['no_found_school']:
                from library.models import School
                new_school, smth = School.objects.get_or_create(name=request.session['no_found_school'])
                profile.school = new_school.name
            else:
                profile.school = request.session['school']
            profile.graduate_year = request.session['graduate_year']
            profile.faculty = request.session['faculty']
            profile.cathedra = request.session['cathedra']
            profile.phone_number = request.session['phone_number']
            profile.phone_visible = request.session['phone_visible']
            profile.ICQ_Skype = request.session['ICQ_Skype']
            profile.social = request.session['social']
            profile.set_password(request.session["password"])
            profile.save()

            try:
                from account.models import Aword
                awrd, created = Aword.objects.get_or_create(name=request.session['awords'], user=profile)
                profile.awords = awrd
                profile.save()
            except Aword.DoesNotExist:
                pass

            from settings.views import send_email
            send_email(request, profile.email, 'register_email', u'Регистрация на сайте',
                       profile=profile, password=request.session["password"])

            user = authenticate(username=request.session['email'], password=request.session["password"])
            if user is not None:
                login(request, user)

            request.session['registered'] = 'TRUE'
            return HttpResponseRedirect(reverse('account.views.register4'))
    else:
        step3_form = RegisterStep3Form()
    # Render the template depending on the context.

    return render_to_response(
        'account/register.html',
        {'register_form': step3_form.render(request), 'step1_active': 'active', 'step2_active': 'active',
         'step3_active': 'active', 'step': 3},
        context)


def register4(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    content = u'<div class="title-holder"><h3>Спасибо за уделённое нам время!</h3></div><div class="link-frame">' \
              u'<a href="{0}">перейти на «ленту публикаций»</a></div>'.format(reverse('mainpage'))
    # Render the template depending on the context.
    return render_to_response(
        'account/register.html',
        {'register_form': content, 'step1_active': 'active', 'step2_active': 'active', 'step3_active': 'active',
         'step4_active': 'active', 'step': 4},
        context)


def handle_uploaded_file(f, path):
    try:
        with open(os.path.join(path, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    except:
        return False


def allmsg(request, **kwargs):
    if re.search("[?].*", request.POST.get('url')):
        xxx = re.search("[?].*", request.POST.get('url')).group(0)
        xx=re.sub("[?]","",xxx)
        yyy = re.sub("__.*?=","=", xx)
        zz = re.split("&",yyy)
        d = dict()
        for z in zz:
            d[re.split("=",z)[0]]=re.split("=",z)[1]
        users = MyUser.objects.filter(**(d))
    else:
        users = MyUser.objects.all()
    message=request.POST.get('allmsg')
    file_content=''
    file_content=u'Сообщение:\n'+message+u'\nВремя отправки: '+str(timezone.now())+u'\nСообщение отправлено пользователям: \n'
    for i,user in enumerate(users):
        file_content+=str(i+1)+u'. '+str(user)+u'\n'
        msg, created = AllMsg.objects.get_or_create(user=user, type=0)
        msg.unreaded=int(msg.unreaded)+1
        msg.msgs=msg.msgs+message+'|'
        msg.datetime=str(msg.datetime)+str(timezone.now())+'|'
        msg.type=0
        msg.save()
    # f = open(os.path.join(settings.STATIC_ROOT,
    #                       'sending.log'), 'w+')
    # f.write(file_content.encode("utf-8"))
    # f.close()
    htmsg="отправлено"
    return render(request, 'circle/MassDialog.html',{'xurl':  users,'msg':htmsg})

def allmsgcodes(request, **kwargs):
    if re.search("[?].*", request.POST.get('url')):
        xxx = re.search("[?].*", request.POST.get('url')).group(0)
        xx=re.sub("[?]","",xxx)
        yyy = re.sub("__.*?=","=", xx)
        zz = re.split("&",yyy)
        d = dict()
        for z in zz:
            d[re.split("=",z)[0]]=re.split("=",z)[1]

        if not d['post'] and d['score']!="pass":
            htmsg="не отправлено, ошибка в фильтре: "+str(request.POST.get('url'))
            return render(request, 'circle/MassDialog.html',{'msg':htmsg})
        passm=75
        try:
            q=Quiz.objects.get(post=int(d['post']))
            passm=q.pass_mark
        except:
            htmsg="не отправлено, ошибка в фильтре: "+str(d)
            return render(request, 'circle/MassDialog.html',{'msg':htmsg})
        users=MyUser.objects.filter(progress__overallscore__gte=passm, progress__test_id__post=d['post'])
    else:
        htmsg="не отправлено, ошибка в фильтре: "+str(request.POST.get('url'))
        return render(request, 'circle/MassDialog.html',{'msg':htmsg})
    message=request.POST.get('allmsg')
    codes=''
    file_content=''
    if request.POST.get('codes'):
        codes=request.POST.get('codes')
        codes=re.split("\r\n",codes)

    if codes=='':
        htmsg="не отправлено, ошибка в кодах"
        return render(request, 'circle/MassDialog.html',{'msg':htmsg})
    if len(codes)<len(users):
        htmsg="не отправлено, недостаточно кодов: "+str(len(codes))+" < "+str(len(users))
        return render(request, 'circle/MassDialog.html',{'msg':htmsg})
    file_content=u'Сообщение:\n'+message+u'\nВремя отправки:'+str(timezone.now())+u'\nСообщение с кодами отправлено пользователям: \n'
    for i,user in enumerate(users):
        file_content+=str(i+1)+u'. '+str(user).decode("utf-8")+u' код:'+codes[i]+u'\n'
        msg, created = AllMsg.objects.get_or_create(user=user, type=1)
        msg.unreaded=int(msg.unreaded)+1
        msg.msgs=msg.msgs+message+u'<br><b>КОД: </b>'+codes[i]+'|'
        msg.datetime=str(msg.datetime)+str(timezone.now())+'|'
        msg.type=1
        msg.save()
    f = open(os.path.join(settings.STATIC_ROOT,
                          'sending.log'), 'w+')
    f.write(file_content.encode("utf-8"))
    f.close()

    htmsg="отправлено"
    return render(request, 'circle/MassDialog.html',{'xurl':  users,'msg':htmsg})


@csrf_exempt
def avatarupload(request, sizex=0, sizey=0):
    result = FileUploadTo(request, ['profile_images', ], int(sizex), int(sizey))
    resultjson = json.loads(result)
    if resultjson['result'] == False:
        return HttpResponse(result)
    user = MyUser.objects.get(id=request.user.id)
    user.avatar = resultjson['file']
    user.save()
    if len(request.user.images) > 2:
        resultjson['howmany'] = len(request.user.images) - 2
    else:
        resultjson['howmany'] = 0
    return HttpResponse(json.JSONEncoder().encode(resultjson))


@csrf_exempt
def addimageupload(request, sizex, sizey):
    if request.method == 'POST':
        if 'file' in request.FILES:
            path = os.path.join(settings.MEDIA_ROOT, 'user_image')
            if handle_uploaded_file(request.FILES['file'], path):
                infile = request.FILES['file'].name
                outfile = 'thumb_{0}_{1}_{2}'.format(sizex, sizey, request.FILES['file'].name)
                input_url = os.path.join(os.path.join('/media', 'user_image'), infile)
                output_url = os.path.join(os.path.join('/media', 'user_image'), outfile)
                if not os.path.isfile(os.path.join(path, outfile)):
                    try:
                        resize_and_crop(os.path.join(path, infile), os.path.join(path, outfile),
                                        [int(sizex), int(sizey)], 'middle')
                    except IOError:
                        return HttpResponse(u'cannot create thumbnail for {0}'.format(infile))
                Additional_Image = AdditionalImage()
                Additional_Image.image = input_url
                Additional_Image.user_id = request.user.id
                Additional_Image.save()
                return HttpResponse(json.JSONEncoder().encode({'url': output_url, 'file': outfile}))
        else:
            return HttpResponse("cannot upload file")
    else:
        return HttpResponse("no POST request")


def admin_statistic(request):
    context = {}
    from account.models import MyUser

    context['by_city'] = MyUser.objects.values('town__name').annotate(count=Count('id')).order_by('-count')
    context['by_spec'] = MyUser.objects.values('spec_id__name').annotate(count=Count('id')).order_by('-count')
    return render(request, 'admin/stat.html', {'context': context})