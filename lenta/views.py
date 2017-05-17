import logging
import os
import urllib
import cStringIO
import json
import string
import random
from urlparse import urlparse

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, Template
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

from account.models import MyUser
from library.models import Spec, Topic
from library.models import Topic, Spec
from post.models import Post, PostPhoto, PostVideo
from fileshandle.views import FileUpload, FileUploadTo, FileDelete, FileDeleteEx


size = 128, 128
logger = logging.getLogger(__name__)

# Create your views here.

@login_required
def mainpage(request):
    context = RequestContext(request)
    dirname = request.user.login
    postroot = os.path.join(os.path.join(settings.MEDIA_ROOT, 'temporary'), 'post');
    if os.path.exists(os.path.join(postroot, dirname)):
        try:
            for root, dirs, files in os.walk(os.path.join(postroot, dirname), topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        except:
            return HttpResponse('can not delete dir!!!')
    else:
        try:
            os.mkdir(os.path.join(postroot, dirname))
        except:
            return HttpResponse('can not create dir!!!')
    return render_to_response(
        'lenta/main.html',
        {'request': request,
         'spec': Spec.objects.all(),
         'topic': Topic.objects.all()},
        context)

def handle_uploaded_file(f, path):
    logger.log(logging.DEBUG, u'{0}/{1}'.format(path, f.name))
    try:
        with open(u'{0}/{1}'.format(path, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    except:
        return False


@csrf_exempt
def fileupload(request, sizex=0, sizey=0):
    if not request.user.is_authenticated():
        return HttpResponse(json.JSONEncoder().encode({'success': False}))
    return HttpResponse(FileUploadTo(request, ['temporary', 'post', request.user.login], int(sizex), int(sizey)))


@csrf_exempt
def filedelete(request):
    return HttpResponse(FileDeleteEx(request))


def do_URL(url):
    parsed_path = urlparse(url)
    try:
        params = dict([p.split('=') for p in parsed_path[4].split('&')])
    except:
        params = {}
    return params


@csrf_exempt
def videoupload(request):
    if request.method == 'POST':
        if 'video' in request.POST:
            address = ''
            try:
                urllib.urlopen(request.POST['video'])
                address = do_URL(request.POST['video'])
                if 'v' not in address:
                    return HttpResponse(
                        json.JSONEncoder().encode({'message': 'can not get video info', 'result': False}))
                address = address['v']
            except:
                address = request.POST['video']
            URL = "http://img.youtube.com/vi/{0}/0.jpg".format(address)
            INFO_URL = "http://youtube.com/get_video_info?video_id={0}".format(address)
            try:
                resource = urllib.urlopen(INFO_URL)
                content = resource.read()
                content = '{ ' + content.replace("=", " : ").replace('&', ' , ') + ' }'
                content = json.loads(content.replace(" ", "\""))
                title = urllib.unquote('"{0}"'.format(content.get('title', ''))).decode('utf8')
            except:
                return HttpResponse(
                    json.JSONEncoder().encode({'message': 'can not get video info %s' % address, 'result': False}))
            path = os.path.join(
                os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, 'temporary'), 'post'), request.user.login),
                'video')

            if not os.path.exists(path):
                os.makedirs(path)

            outputfile = os.path.join(path, u'{0}.jpg'.format(address))
            try:
                resource = urllib.urlopen(URL)
                output = open(outputfile, "wb+")
                output.write(resource.read())
                output.close()
                output_url = os.path.join(os.path.join(
                    os.path.join(os.path.join(os.path.join(settings.MEDIA_URL, 'temporary'), 'post'),
                                 request.user.login), 'video'), u'{0}.jpg'.format(address))
                return HttpResponse(json.JSONEncoder().encode(
                    {'furl': output_url, 'title': title[0:20], 'path': outputfile, 'file': output_url, 'result': True}))
            except Exception as e:
                logger.exception('can not upload video: %s' % e)
                return HttpResponse(json.JSONEncoder().encode(
                    {'message': u'can not upload video from {0}'.format(URL), 'result': False}))
        else:
            return HttpResponse(json.JSONEncoder().encode({'message': 'no video in POST', 'result': False}))
    else:
        return HttpResponse(json.JSONEncoder().encode({'message': 'no POST in request', 'result': False}))


@csrf_exempt
def videodelete(request):
    logger.log(logging.DEBUG, request)
    if request.method == 'POST':
        if 'video' in request.POST:
            try:
                os.remove(request.POST['video'])
                return HttpResponse('OK')
            except:
                return HttpResponse('error delete video!!!')
        else:
            return HttpResponse('no video in POST')
    else:
        return HttpResponse('no POST in request')


@csrf_exempt
def savepost(request):
    # logger.log(logging.DEBUG, request)
    media = dict()
    media['photo'] = {}
    media['video'] = {}
    if request.method == 'POST':
        if 'data' in request.POST:
            try:
                data = json.JSONDecoder().decode(request.POST['data'])
            except:
                return HttpResponse('data is not JSON')
            logger.log(logging.DEBUG, data)
            try:
                for key, val in data['photo'].iteritems():
                    src = os.path.join(
                        os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, 'temporary'), 'post'),
                                     request.user.login), val)
                    dstname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                    dst = os.path.join(os.path.join(settings.MEDIA_ROOT, 'post_images'), dstname)
                    src_thumb = os.path.join(
                        os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, 'temporary'), 'post'),
                                     request.user.login), u'thumb_{0}'.format(val))
                    dst_thumb = os.path.join(os.path.join(settings.MEDIA_ROOT, 'post_images'),
                                             u'thumb_{0}'.format(dstname))
                    im = Image.open(src)
                    im.save(dst, "JPEG")
                    im = Image.open(src_thumb)
                    im.save(dst_thumb, "JPEG")
                    media['photo'][key] = {}
                    media['photo'][key]['photo'] = dst
                    media['photo'][key]['thumb'] = dst_thumb

                for key, val in data['video'].iteritems():
                    src = os.path.join(os.path.join(
                        os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, 'temporary'), 'post'),
                                     request.user.login), 'video'), val)
                    dstname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                    dst = os.path.join(os.path.join(settings.MEDIA_ROOT, 'post_images'), dstname)
                    im = Image.open(src)
                    im.save(dst, "JPEG")
                    media['video'][key] = {}
                    media['video'][key]['video'] = dst
            except:
                return HttpResponse(u'can not save files')
            try:
                media['topic'] = data['topic']
                media['content'] = data['content']
                media['spec'] = data['spec']
                media['title'] = data['title']
            except:
                return HttpResponse(u'can not save fields')
            try:
                post = Post()
                topic = Topic.objects.filter(name=media['topic'])
                if not topic:
                    return HttpResponse(u'have no topic {0}'.format(media['topic']))
                post.topic = topic[0]
                post.content = media['content']
                post.title = media['title']
                spec = Spec.objects.filter(name=media['spec'])
                if not spec:
                    return HttpResponse(u'have no spec {0}'.format(media['spec']))
                post.spec = spec[0]
                user = MyUser.objects.filter(login=request.user.login)
                if not user:
                    return HttpResponse(u'have no user {0}'.format(request.user.login))
                post.publisher = user[0]
                post.save()
            except:
                return HttpResponse(u'can not create Post')
            try:
                for key, val in media['photo'].iteritems():
                    pp = PostPhoto()
                    url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['photo']))
                    pp.picture = url
                    url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['thumb']))
                    pp.thumb = url
                    pp.post = post
                    pp.save()
                    logger.log(logging.DEBUG, val['photo'])
            except:
                return HttpResponse(u'can not create PostPhoto')
            try:
                for key, val in media['video'].iteritems():
                    pv = PostVideo()
                    url = os.path.join(os.path.join(settings.MEDIA_URL, 'post_images'), os.path.basename(val['video']))
                    pv.preview = url
                    pv.data = os.path.basename(val['video'])
                    pv.post = post
                    pv.save()
            except:
                return HttpResponse(u'can not create PostVideo')
            logger.log(logging.DEBUG, media)
            return HttpResponse('ok')
        else:
            return HttpResponse('no data in POST')
    else:
        return HttpResponse('no POST in request')
