# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
import os
import json
import re
import sys

from django.db.models import Count
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.utils import timezone
from django.db.transaction import atomic

from quiz.models import Quiz
from account.forms import RegisterStep1Form, RegisterStep2Form, RegisterStep3Form
from .models import MyUser, AdditionalImage, AllMsg
from medtus.models import Specialities, Towns, Countries, Regions
from cuter.cuter import resize_and_crop
from fileshandle.views import FileUploadTo
from simplejson import dumps, loads

size = settings.AVATAR_SIZE
logger = logging.getLogger(__name__)
step2_form = ""


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainpage'))


def user_login(request):
    error=''
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        #print(password)
        try:
            user = authenticate(request, username=username, password=password)
            print(user)
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
            error = u'<span class="inform-error">?????????? ?????? ???????????? ????????????????!  ' \
                    u'<br>???????????????????? ???????????? ???? ?????? ??????.</span>'
    return render(request,
        'account/login.html',{'error': error})

@csrf_protect
def password_forgot(request, **kwargs):
    error = ''
    context = RequestContext(request)
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
                send_email(request, email, 'forgot_email', u'???????????????????????????? ???????????? ???? vrvm.ru', token=token.token)

                return render(request,
                    'account/forgot.html',
                    {
                        'error': error,
                        'sent': True
                    },
                    context.flatten()
                )
            else:
                error = u'?????????????? ???? ??????????????'
        else:
            error = u'???????????????? ?? ?????????? ???????????? ?? ?????? ??????.'

        return render(request,
            'account/forgot.html',
             { 'error': error},
                    context.flatten()
        )
    else:
        return render(request,
            'account/forgot.html',
                    context.flatten()
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
                    params['error'] = u'???????????? ???????????? ??????????????????'
                else:
                    import re
                    p = re.compile(ur'[a-z\d]+', re.UNICODE | re.IGNORECASE)
                    if re.search(p, password1):
                        user = token.first().user
                        user.set_password(password1.encode('utf-8'))
                        user.save()

                        from settings.views import send_email
                        send_email(request, user.email, 'passchange_email', u'?????? ???????????? ??????????????',
                           profile=user, password=password1.encode('utf-8'))

                        token.first().delete()
                        params['error'] = u'???????????? ?????????????? ?????????????? <a href="{url}">??????????</a>'.format(url=reverse('login'))
                        params['show_form'] = False
                    else:
                        params['error'] = u'?? ???????????? ???????????????? ???????????? ?????????????? A-Z ?? 0-9'
        else:
            params['error'] = u'???????????? ???? ??????????????????????????. ?????????????????? ???????????? ?????? ??????'
            params['show_form'] = False
            token.first().delete()
    else:
        params['show_form'] = False
        params['error'] = u'???????????? ???? ??????????????????????????. <a href="{url}">?????????????????? ???????????? ?????? ??????</a>'.format(url=reverse('forgot'))

    return render(request,
        'account/change.html',
        params,
	context.flatten()
    )


def agreement(request):
    import settings.models as s
    on = s.Settings.objects.all()[:1]
    content = ""
    if on.exists():
        content = on[0].agreement

    context = RequestContext(request)

    return render(request,
        'account/agreement.html',
        {'content': content}
        )


def register1(request):
    # Like before, get the request's context.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register4'))
    if request.method == 'POST':
        step1_form = RegisterStep1Form(data=request.POST)
        if step1_form.is_valid(request):
            return HttpResponseRedirect(reverse('register2'))
    else:
        step1_form = RegisterStep1Form()
    # Render the template depending on the context.
    return render(request,
        'account/register.html',
        {'register_form': step1_form.render(request), 'step1_active': 'active', 'step': 1}
        )


def register2(request):
    def build_html_select_form(objects, first_title=None, field_name=None):
        out = []
        out.append(u'<option value="0">{}</option>'.format(first_title))
        for object in objects:
            out.append(u'<option value="{0}">{1}</option>'.format(
                            object.id, getattr(object, field_name or 'name')))
        return out

    # Like before, get the request's context.
    if request.method == 'GET' and request.is_ajax():
        if request.GET.get('country', None):
            first_title = u'???????????????? ????????????'
            queryset = Regions.objects.filter(
                    country_id=request.GET.get('country')
                ).order_by('name')
            return HttpResponse(
                        build_html_select_form(queryset, first_title, 'title'))
        elif request.GET.get('region', None):
            # Get towns by region. After set country and region.
            first_title = u'???????????????? ??????????'
            queryset = Towns.objects.filter(
                    region_id=request.GET.get('region')
                ).order_by('name')
            return HttpResponse(build_html_select_form(queryset, first_title))
        else:
            return HttpResponse(u'<option value="0">---------</option>')

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register4'))

    step2_form = RegisterStep2Form()
    if request.method == 'POST':
        step2_form = RegisterStep2Form(data=request.POST)
        if step2_form.is_valid(request):
            return HttpResponseRedirect(reverse('register3'))
    else:
        step2_form = RegisterStep2Form()

    # Render the template depending on the context.
    return render(request,
        'account/register.html',
        {'register_form': step2_form.render(request), 'step1_active': 'active', 'step2_active': 'active', 'step': 2}
        )


def register3(request):
    # Like before, get the request's context.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register4'))
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
                profile.region = Regions.objects.get(id=request.session['region'])
            except Regions.DoesNotExist:
                profile.region = None
            try:
                profile.country = Countries.objects.get(id=request.session['country'])
            except Countries.DoesNotExist:
                profile.country = None
            profile.avatar = request.session['avatar']
            profile.sex = request.session['sex']

            birthday = request.session['birthday'].split('/')
            if birthday:
		if len(birthday) > 2:
                	d1 = datetime.strptime('{0} {1} {2}'.format(birthday[0], birthday[1], birthday[2]), "%d %m %Y")
		else:
			d1 = datetime(1970,1,1)
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
            send_email(request, profile.email, 'register_email', u'?????????????????????? ???? ??????????',
                       profile=profile, password=request.session["password"])

            user = authenticate(username=request.session['email'], password=request.session["password"])
            if user is not None:
                login(request, user)

            request.session['registered'] = 'TRUE'
            return HttpResponseRedirect(reverse('register4'))
    else:
        step3_form = RegisterStep3Form()
    # Render the template depending on the context.

    return render(request,
        'account/register.html',
        {'register_form': step3_form.render(request), 'step1_active': 'active', 'step2_active': 'active',
         'step3_active': 'active', 'step': 3}
        )


def register4(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    content = u'<div class="title-holder"><h3>?????????????? ???? ?????????????????? ?????? ??????????!</h3></div><div class="link-frame">' \
              u'<a href="{0}">?????????????? ???? ???????????? ??????????????????????</a></div>'.format(reverse('mainpage'))
    # Render the template depending on the context.
    return render(request,
        'account/register.html',
        {'register_form': content, 'step1_active': 'active', 'step2_active': 'active', 'step3_active': 'active',
         'step4_active': 'active', 'step': 4}
        )


def handle_uploaded_file(f, path):
    try:
        with open(os.path.join(path, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    except:
        return False


def logfiles():
    logpath="/var/www/vrachivmeste.ru/medtus.djangohost.name/static/"
    logfiles=[]
    onlyfiles = [f for f in os.listdir(logpath) if os.path.isfile(os.path.join(logpath, f))]
    for file in onlyfiles:
        if "sending" in file:
            logfiles.append(file)
    return logfiles

def allmsgs(request, **kwargs):
    return render(request, 'circle/MassDialog.html',{'log_files': logfiles()})

@atomic
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
        # users = MyUser.objects.all()
        users = MyUser.objects.filter(id__gte=100000)
    message=request.POST.get('allmsg')
    file_content=''
    file_content=u'??????????????????:\n'+message+u'\n?????????? ????????????????: '+str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))+u'\n?????????????????? ???????????????????? '+str(len(users))+u' ??????????????????????????: \n'
    reload(sys)
    sys.setdefaultencoding('utf-8')
    f = open(os.path.join(settings.STATIC_ROOT, 'sending-'+str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))+'.txt'), 'w+')
    i=0
    for user in users.iterator():
        msg, created = AllMsg.objects.get_or_create(user=user, type=0)
        msg.unreaded=int(msg.unreaded)+1
        msg.msgs=msg.msgs+message+'|'
        msg.datetime=str(msg.datetime)+str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))+'|'
        msg.type=0
        msg.save()
        try:
            user.spec_id.title
        except:
            spec=u'???? ????????????'
        else:
            spec=user.spec_id.title.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user.country.title
        except:
            country=u'???? ????????????'
        else:
            country=user.country.title.encode('UTF-8', 'ignore').decode('UTF-8')


        try:
            user.town.name
        except:
            town=u'???? ????????????'
        else:
            town=user.town.name.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user.firstname
        except:
            firstname=u'???? ????????????'
        else:
            firstname=user.firstname.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user.lastname
        except:
            lastname=u'???? ????????????'
        else:
            lastname=user.lastname.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user_login=user.login.encode('UTF-8', 'ignore').decode('UTF-8')
        except:
            user_login=u'???? ????????????'

        # file_content+=str(i+1)+u'. '+u'???? ????????????'+u', \n'#+firstname+u' '+\
        #               lastname+u', '+spec+u', '+town+u', '+\
        #               country+u' - ????????????????????\n'
        i+=1
        file_content=str(i)+u'. '+str(user.login.encode('ascii', 'ignore').decode('ascii'))+u', '+firstname+u' '+\
                      lastname+u', '+\
                      spec+u', '+town+u', '+\
                      country+\
                      u' - ????????????????????\n'
        f.write(file_content.encode("utf-16"))
    f.close()
    htmsg="???????????????????? "+str(len(users))+" ??????????????????????????"
    return render(request, 'circle/MassDialog.html',{'xurl':  users,'msg':htmsg, 'log_files': logfiles()})

@atomic
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
            htmsg="???? ????????????????????, ???????????? ?? ??????????????, ???? pass: "+str(request.POST.get('url'))
            return render(request, 'circle/MassDialog.html',{'msg':htmsg})
        passm=75
        try:
            q=Quiz.objects.get(post=int(d['post']))
            passm=q.pass_mark

        except:
            htmsg="???? ????????????????????, ???????????? ?? ??????????????, ???? ?????????????? ???????????????? ????????: "+str(d)
            return render(request, 'circle/MassDialog.html',{'msg':htmsg})
        users=MyUser.objects.filter(progress__overallscore__gte=passm, progress__test_id__post=d['post'])
    else:
        htmsg="???? ????????????????????, ???????????? ?? ?????????????? (re.search): "+str(request.POST.get('url'))
        return render(request, 'circle/MassDialog.html',{'msg':htmsg})
    message=request.POST.get('allmsg')
    codes=''
    file_content=''
    if request.POST.get('codes'):
        codes=request.POST.get('codes')
        codes=re.split("\r\n",codes)

    if codes=='':
        htmsg="???? ????????????????????, ???????????? ?? ??????????"
        return render(request, 'circle/MassDialog.html',{'msg':htmsg})
    if len(codes)<len(users):
        htmsg="???? ????????????????????, ???????????????????????? ??????????: "+str(len(codes))+" < "+str(len(users))
        return render(request, 'circle/MassDialog.html',{'msg':htmsg})
    file_content=u'??????????????????:\n'+message+u'\n?????????? ????????????????:'+str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))+u'\n?????????????????? ?? ???????????? ?????? ???????????????????? '+str(len(users))+u' ??????????????????????????: \n'
    for i,user in enumerate(users):
        msg, created = AllMsg.objects.get_or_create(user=user, type=1)
        msg.unreaded=int(msg.unreaded)+1
        msg.msgs=msg.msgs+message+u'<br><b>??????: </b>'+codes[i]+'|'
        msg.datetime=str(msg.datetime)+str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))+'|'
        msg.type=1
        msg.save()

        try:
            user.spec_id.title
        except:
            spec=u'???? ????????????'
        else:
            spec=user.spec_id.title.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user.country.title
        except:
            country=u'???? ????????????'
        else:
            country=user.country.title.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user.town.name
        except:
            town=u'???? ????????????'
        else:
            town=user.town.name.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user.firstname
        except:
            firstname=u'???? ????????????'
        else:
            firstname=user.firstname.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user.lastname
        except:
            lastname=u'???? ????????????'
        else:
            lastname=user.lastname.encode('UTF-8', 'ignore').decode('UTF-8')

        try:
            user_login=user.login.encode('UTF-8', 'ignore').decode('UTF-8')
        except:
            user_login=u'???? ????????????'




        # file_content+=str(i+1)+u'. '+str(user.login.encode('ascii', 'ignore').decode('ascii'))+u', '+user.firstname.encode('UTF-8', 'ignore').decode('UTF-8')+u' '+\
        #               user.lastname.encode('UTF-8', 'ignore').decode('UTF-8')+u', '+\
        #               user.spec_id.name.encode('UTF-8', 'ignore').decode('UTF-8')+u', '+user.town.name.encode('UTF-8', 'ignore').decode('UTF-8')+u', '+\
        #               user.country.name.encode('UTF-8', 'ignore').decode('UTF-8')+\
        #               u' ??????:'+codes[i]+u' - ????????????????????\n'
        file_content+=str(i+1)+u'. '+str(user.login.encode('ascii', 'ignore').decode('ascii'))+u', '+firstname+u' '+\
                      lastname+u', '+\
                      spec+u', '+town+u', '+\
                      country+\
                      u' ??????:'+codes[i]+u' - ????????????????????\n'

    f = open(os.path.join(settings.STATIC_ROOT,
                          'sending-NMO.log-'+str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))+'.txt'), 'w+')
    f.write(file_content.encode("utf-16"))
    f.close()
    htmsg="???????????????????? "+str(len(users))+" ??????????????????????????"
    return render(request, 'circle/MassDialog.html',{'xurl':  users,'msg':htmsg, 'log_files': logfiles()})


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
