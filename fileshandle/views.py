import os
import json
import string
import random
import sys
import errno

from django.conf import settings
from PIL import Image
from wand.image import Image as WandImage

from cuter.cuter import resize_and_crop, is_image_animated


size = 128, 128


def handle_uploaded_file(f, path):
    try:
        with open(u'{0}/{1}'.format(path, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    except:
        return False

def handle_uploaded_file_ex(f, path):
    try:
        fileName, fileExtension = os.path.splitext(f.name.encode("ascii"))
    except:
        fileName, fileExtension = os.path.splitext(f.name)
    fname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    fname = fname + fileExtension
    try:
        with open(u'{0}/{1}'.format(path, fname), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return os.path.basename(fname)
    except:
        try:
            im = Image.open(f.name)
            isanimated = is_image_animated(im)
            new_path = u'{0}/{1}'.format(path, fname)
            if isanimated:
                with WandImage(filename=f.name) as img:
                    f = open(new_path, 'w')
                    img.save(file=f)
            else:
                im.save(new_path)
            return fname
        except:
            return ''


def InitDir(request, dirname, subdirname):
    directory = request.user.login
    root = os.path.join(os.path.join(settings.MEDIA_ROOT, dirname), subdirname);
    if os.path.exists(os.path.join(root, directory)):
        try:
            for root, dirs, files in os.walk(os.path.join(root, directory), topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        except:
            return {'result': False, 'message': 'can not delete dir!!!'}
    else:
        try:
            os.mkdir(os.path.join(root, directory))
        except:
            return {'result': False, 'message': 'can not create dir!!!'}
    return {'result': True}


def FileUpload(request, dirname, subdirname, sizex=0, sizey=0):
    if request.method == 'POST':
        if 'file' in request.FILES:
            path = os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, dirname), subdirname),
                                request.user.login)
            if handle_uploaded_file(request.FILES['file'], path):
                try:
                    infile = request.FILES['file'].name
                    outfile = os.path.join(path, u'thumb_{0}'.format(infile))
                    im = Image.open(u'{0}/{1}'.format(path, infile))
                    if sizex != 0 and sizey != 0:
                        im.thumbnail(sizex, sizey)
                    else:
                        im.thumbnail(size)
                    im.save(outfile)
                    output_url = os.path.join(
                        os.path.join(os.path.join(os.path.join(settings.MEDIA_URL, dirname), subdirname),
                                     request.user.login), u'thumb_{0}'.format(infile))
                    return json.JSONEncoder().encode({'url': output_url, 'file': infile, 'result': True})
                except IOError:
                    return json.JSONEncoder().encode(
                        {'message': u'cannot create thumbnail for {0}'.format(infile), 'result': False})
            else:
                return json.JSONEncoder().encode(
                    {'message': 'cannot upload file {0} - {1}'.format(request.FILES['file'], path), 'result': False})
        else:
            return json.JSONEncoder().encode({'message': 'no file in request', 'result': False})
    else:
        return json.JSONEncoder().encode({'message': 'no POST request', 'result': False})


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def OneFileUpload(f, dirname, sizex=0, sizey=0):
    ext = {'.JPG': '.JPEG'}
    savepath = ''
    path = os.path.join(settings.MEDIA_ROOT, '')
    url = os.path.join(settings.MEDIA_URL, '')
    for d in dirname:
        savepath = os.path.join(savepath, d)
        path = os.path.join(path, d)
        url = os.path.join(url, d)
    try:
        make_sure_path_exists(path)
    except:
        return json.JSONEncoder().encode({'message': u'cannot create dir {0}'.format(path), 'result': False})

    infile = handle_uploaded_file_ex(f, path)
    if infile != '':
        try:
            try:
                fileName, fileExtension = os.path.splitext(f.name.encode("ascii"))
            except:
                fileName, fileExtension = os.path.splitext(f.name)
            if string.upper(fileExtension) in ext:
                fileExtension = ext[string.upper(fileExtension)]
            outfile = os.path.join(path, u'thumb_{0}'.format(infile))
            if sizex != 0 and sizey != 0:
                resize_and_crop(u'{0}/{1}'.format(path, infile), outfile, (sizex, sizey))
            else:
                resize_and_crop(u'{0}/{1}'.format(path, infile), outfile, size)
            output_url = os.path.join(url, u'thumb_{0}'.format(infile))
            return json.JSONEncoder().encode(
                {'url': output_url, 'file': os.path.join(savepath, infile), 'result': True})
        except IOError:
            return json.JSONEncoder().encode(
                {'message': u'cannot create thumbnail for {0}'.format(infile), 'result': False})
    else:
        return json.JSONEncoder().encode(
            {'message': u'cannot upload file {0} - {1}'.format(f.name, path), 'result': False})


def FileUploadTo(request, dirname, sizex=0, sizey=0):
    if request.method == 'POST':
        if 'file' in request.FILES:
            return OneFileUpload(request.FILES['file'], dirname, sizex, sizey)
        else:
            return json.JSONEncoder().encode({'message': 'no file in request', 'result': False})
    else:
        return json.JSONEncoder().encode({'message': 'no POST request', 'result': False})


def FileDelete(request, dirname, subdirname):
    if request.method == 'POST':
        fname = os.path.basename(request.POST['file']).split('_')[1]
        original = os.path.join(
            os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, dirname), subdirname), request.user.login),
            fname)
        thumb = os.path.join(
            os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, dirname), subdirname), request.user.login),
            u'thumb_{0}'.format(fname))
        try:
            os.remove(original)
            os.remove(thumb)
        except:
            return json.JSONEncoder().encode({'message': 'error delete!!!', 'result': False})
        return json.JSONEncoder().encode({'message': 'OK', 'result': True})
    else:
        return json.JSONEncoder().encode({'message': 'no POST in request', 'result': False})


def GetListFilesIntoDir(request, dirname, subdirname):
    directory = request.user.login
    root = os.path.join(os.path.join(settings.MEDIA_ROOT, dirname), subdirname);
    if not os.path.exists(os.path.join(root, directory)):
        return 0
    return os.listdir(os.path.join(root, directory))


def CopyFiles(request, fileslist, srcdirname, srcsubdirname, dstdirname):
    ext = {'.JPG': '.JPEG'}
    files = []
    # try:
    for val in fileslist:
        try:
            fileName, fileExtension = os.path.splitext(val.encode("ascii"))
        except:
            fileName, fileExtension = os.path.splitext(val)
        if string.upper(fileExtension) in ext:
            fileExtension = ext[string.upper(fileExtension)]
        dstname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10)) + fileExtension
        src = os.path.join(os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, srcdirname), srcsubdirname),
                                        request.user.login), val)
        dst = os.path.join(os.path.join(settings.MEDIA_ROOT, dstdirname), dstname)
        im = Image.open(src)
        im.save(dst, fileExtension[1:])
        files.append(dst)
    return {'result': True, 'fileslist': files}
    # except:
    # return {'result': False, 'message': 'unknown error in CopyFiles'}#sys.exc_info()[0]}


def CopyFilesOnly(fileslist, dstdirname):
    ext = {'.JPG': '.JPEG'}
    files = []
    # try:
    for val in fileslist:
        try:
            fileName, fileExtension = os.path.splitext(val.encode("ascii"))
        except:
            fileName, fileExtension = os.path.splitext(val)
        if string.upper(fileExtension) in ext:
            fileExtension = ext[string.upper(fileExtension)]
        dstname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10)) + fileExtension
        dst = os.path.join(os.path.join(settings.MEDIA_ROOT, dstdirname), dstname)
        im = Image.open(val)
        im.save(dst, fileExtension[1:])
        files.append(dst)
    return {'result': True, 'fileslist': files}


def CopyFileOnly(onefile, dstdirname, **kwargs):
    ext = {'.JPG': '.JPEG'}
    files = []
    try:
        fileName, fileExtension = os.path.splitext(onefile.encode("ascii"))
    except:
        fileName, fileExtension = os.path.splitext(onefile)
    if string.upper(fileExtension) in ext:
        fileExtension = ext[string.upper(fileExtension)]

    try:
        if (not kwargs.get('no_random', False)):
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        else:
            name = fileName
        dstname = name + fileExtension
        dst = os.path.join(dstdirname, dstname)
        im = Image.open(onefile)
        isanimated = is_image_animated(im)
        if isanimated:
            with WandImage(filename=onefile) as img:
                f = open(dst, 'w')
                img.save(file=f)
        else:
            im.save(dst, fileExtension[1:])
        return dst
    except:
        return False


def CreateFileDir(namelist):
    result = settings.MEDIA_ROOT
    for name in namelist:
        result = os.path.join(result, name)
    return result


def GetThumbName(name):
    basename = os.path.basename(name)
    dirname = os.path.dirname(name)
    thumbname = u'thumb_%s' % basename
    return os.path.join(dirname, thumbname)


def ExtractUrlFromPath(path):
    try:
        p = path.split('media')[1]
        return u'/media%s' % p
    except:
        return False


def CreatePathFromUrl(furl):  # furl = /media/...
    try:
        return u'%s%s' % (os.path.dirname(settings.MEDIA_ROOT), furl.split('media')[1])
    except:
        return False


def ImageIsThumb(image):
    return len(image.split('thumb_')) > 1


def ThumbToImage(thumb):
    fdir = os.path.dirname(thumb)
    base = os.path.basename(thumb)
    media = os.path.dirname(settings.MEDIA_ROOT)
    try:
        fname = base.split('thumb_')[1]
        return u'%s%s/%s' % (media, fdir, fname)
    except:
        return False


def FileDeleteEx(request):
    if request.method == 'POST':
        furl = request.POST['file']
        if ImageIsThumb(furl):
            image = ThumbToImage(furl)
        else:
            image = CreatePathFromUrl(furl)
        if not image:
            return json.JSONEncoder().encode({'message': 'remove fail %s' % sys.exc_info()[0], 'result': False})
        thumb = GetThumbName(image)
        try:
            os.remove(image)
            os.remove(thumb)
        except Exception as e:
            return json.JSONEncoder().encode(
                {'message': "remove fail {0} furl={1} image={2}".format(e, image, image), 'result': False})
        return json.JSONEncoder().encode({'result': True})
    else:
        return json.JSONEncoder().encode({'message': 'POST fail', 'result': False})
