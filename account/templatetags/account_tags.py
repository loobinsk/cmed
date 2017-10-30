# -*- coding: utf-8 -*-
import httplib
import os
import random

import datetime
from PIL import Image
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db.models import Q

from account.models import MyUser, AllMsg
from circle.models import Dialog, Record, Circle
from cuter.cuter import resize_and_crop
from events.models import Events
from groups.models import GroupUsers
from medtus.models import Like, Visited
from posts.models import Posts
from settings.models import Settings
from videos.models import Videos
import re

size = settings.AVATAR_SIZE

register = template.Library()

prolog_day = u'<div class="content-block-right-popular-head">Самые популярные за день:</div>'
prolog_month = u'<div class="content-block-right-popular-head">Самые популярные за месяц:</div>'
epilog = u'<div class="content-block-right-popular-item-dots"></div>'
template = u'<div class="content-block-right-popular-item"><div class="content-block-right-popular-item-left"><div class="content-block-right-popular-item-left-photo-bg"><a href="{0}" target="_parent" title="На страницу автора"><div class="content-block-right-popular-item-left-photo" style="background-image:{1}"></div></a></div><div class="content-block-right-popular-item-left-rating"><div class="content-block-right-popular-item-left-rating-val" id="like_most_popular_{2}_{3}" title="Соглашусь!" onclick="SendLike(\'{4}\', \'{5}\', \'like_most_popular_{2}_{3}\');">+{7}</div></div></div><div class="content-block-right-popular-item-right"><p><a href="{8}" target="_parent" title="На страницу автора">{9}<br />{10} {11}</a><br /><i>{12}</i></p><a href="{13}" target="_blank" title="{14}">{15}</a> <span>{16}</span></div></div>'
down_line = '<div class="content-block-right-popular-item-line"></div>'

template_now_read = u'<div class="content-block-right-read-now-item"><a href="{0}" target="_blank" title="{1}">{2}</a><br /><p><a href="{3}" target="_parent" title="На страницу автора">{4}<br />{5} {6}</a></p>	{7}</div>'
template_now_read_down_line = '<div class="content-block-right-read-now-item-line"></div>'

@register.filter
def find_bool(string, args):
    if re.search(args, string).group(0):
        return True
    return False

@register.simple_tag
def get_all_users():
    return MyUser.objects.all().count()

@register.simple_tag
def get_all_users_fake():
    return 110298+(MyUser.objects.all().count()-72110)


@register.simple_tag
def get_all_from_my_town(user_id):
    try:
        user = MyUser.objects.get(id=user_id)
        return MyUser.objects.filter(town__id=user.town.id).count()
    except:
        return 0


@register.simple_tag
def get_all_with_my_spec(user_id):
    try:
        user = MyUser.objects.get(id=user_id)
        spec = user.spec_id
        return MyUser.objects.filter(spec_id__id=spec.id).count()
    except:
        return 0


@register.simple_tag
def most_visited():
    visited = Visited.objects.all().order_by('-lastview')[0:3]
    # debug = []
    out = ''
    for v in visited:
        try:
            obj = v.content_object
            user = obj.user_id
            if out:
                out = out + template_now_read_down_line
            out = out + template_now_read.format(obj.get_absolute_url(), obj.title, obj.title,
                                                 reverse('lichnie2', args=(user.id,)), user.lastname, user.firstname,
                                                 user.surname, user.spec_id.title)
        except:
            pass
    return out


def get_object(ID, service_id=0):
    try:
        if service_id == 10:
            return Videos.objects.get(id=ID)
        if service_id == 18:
            return Posts.objects.get(id=ID)
        if service_id == 6:
            return Events.objects.get(id=ID)
    except:
        pass
    try:
        return Videos.objects.get(id=ID)
    except:
        pass
    try:
        return Posts.objects.get(id=ID)
    except:
        pass
    try:
        return Events.objects.get(id=ID)
    except:
        pass
    return None


@register.simple_tag
def most_popular_events(period):
    events = ''
    today = datetime.date.today()
    Prolog = {'MONTH': prolog_month, 'DAY': prolog_day}

    if period == 'MONTH':
        last_month = today - datetime.timedelta(days=30)
        qs = Like.objects.filter(createdate__gte=last_month)
    else:
        qs = Like.objects.filter(createdate__gte=today)  # TODO test

    qs = qs.values('service_id', 'material_id').annotate(count=Count('service_id')).order_by('-count')[:4]

    for item in qs:
        obj = get_object(
            item['material_id'],
            item['service_id'],
        )

        if not obj:
            continue

        if events:
            events += down_line

        try:
            user = obj.user_id  # TODO select related
            try:
                spec_title = user.spec_id.title
            except:
                spec_title = ''

            events += template.format(
                reverse('lichnie2', args=(user.id,)),
                "url({0}), url({1})".format(get_avatar_preview_sizexy(user.id, 77, 77), user.avatar),
                period,
                obj.id, obj.id, item['service_id'], obj.id,
                obj.statistics and len(obj.statistics.likes.split()) or 0,
                reverse('lichnie2', args=(user.id,)),
                user.lastname, user.firstname, user.surname, spec_title,
                obj.get_absolute_url(),
                obj.title,
                obj.title,
                obj.createdate
            )
        except MyUser.DoesNotExist:
            pass

    if events:
        events = Prolog[period] + events + epilog
    return events


@register.filter
def printnull(string):
    if string == 0:
        return ''
    else:
        return string


invite = u'<a href="{0}"><div class="info-block"><span class="title">{1}</span><span class="info {2}">{3}</span></div></a>'


@register.simple_tag
def IInvitedThem(user):
    s = ''
    count = Circle.objects.filter(Q(parent=user) & Q(activated=False)).count()
    # count = Circle.objects.filter(Q(parent=user)).count()
    if count == 0:
        return ''
    elif count >= 1 and count < 5:
        s = u'%s врача' % count
    else:
        s = u'%s врачей' % count
    return invite.format(reverse('mycircle'), u'Вы пригласили в свой круг ', 'active',
                         s) + '<div class="content-block-top-separator"></div>'


@register.simple_tag
def IveBeenInvited(user):
    s = ''
    count = Circle.objects.filter(Q(friend=user) & Q(activated=False)).count()
    # count = Circle.objects.filter(Q(friend=user)).count()
    if count == 0:
        return ''
    elif count == 1:
        s = u'1 врач'
    elif count > 1 and count < 5:
        s = u'%s врача' % count
    else:
        s = u'%s врачей' % count
    return invite.format(reverse('mycircle'), u'Вас добавили в свой круг ', '', s)


@register.simple_tag
def newinvite(user):
    count = Circle.objects.filter(Q(friend=user) & Q(activated=False)).count()
    if count != 0:
        return "<span>%s</span>" % count
    else:
        return ''

@register.simple_tag
def AdmUnreaded_one(user_id):
    msgs = AllMsg.objects.get(user=user_id, type=0)
    if msgs.unreaded:
        return u'<a href="/circle/dialog/admin"><p class="groups-area holder description link01" style="float:left;width:10px;' \
               u'color:#fff;border-radius:3px;background-color:#e1523d;padding-top:2px;padding-left:5px;padding-right:5px;padding-bottom:2px;width:70px;">Новых: {0}</p></a>'.format(msgs.unreaded)
    else:
        return '<a href="/circle/dialog/admin"><p class="groups-area holder description link01" style="float:left;width:10px;' \
               'color:#fff;border-radius:3px;background-color:#e1523d;padding-top:2px;padding-left:5px;padding-right:5px;padding-bottom:2px;width:70px;">Сообщения</p></a>'


@register.simple_tag
def NmoUnreaded_one(user_id):
    msgs = AllMsg.objects.get(user=user_id, type=1)
    if msgs.unreaded:
        return u'<a href="/circle/dialog/nmo"><p class="groups-area holder description link01" style="float:left;width:10px;' \
               u'color:#fff;border-radius:3px;background-color:#e1523d;padding-top:2px;padding-left:5px;padding-right:5px;padding-bottom:2px;width:70px;">Новых: {0}</p></a>'.format(msgs.unreaded)
    else:
        return '<a href="/circle/dialog/nmo"><p class="groups-area holder description link01" style="float:left;width:10px;' \
               'color:#fff;border-radius:3px;background-color:#e1523d;padding-top:2px;padding-left:5px;padding-right:5px;padding-bottom:2px;width:70px;">Сообщения</p></a>'



@register.simple_tag
def Unreaded_one(account_id, dialog_id, auth):
    count = 0
    t = u'<a href="{0}"><p class="groups-area holder description link01" style="float:left;width:10px;color:#fff;border-radius:3px;background-color:#e1523d;padding-top:2px;padding-left:5px;padding-right:5px;padding-bottom:2px;width:70px;">Новых: {1}</p></a>'
    D = Dialog.objects.get(id=dialog_id)
    try:
        if D.authA.id == account_id:
            opponent = D.authB.id
        else:
            opponent = D.authA.id

        count = Record.objects.filter(Q(auth=opponent) & Q(viewed__lt='2006-01-01') & Q(dialog=D)).count()
        if count:
            return t.format(reverse('dialog', args=(auth,)), count)
        return '<a href="{0}"><p class="groups-area holder description link01" style="float:left;width:10px;color:#fff;border-radius:3px;background-color:#e1523d;padding-top:2px;padding-left:5px;padding-right:5px;padding-bottom:2px;width:70px;">Сообщения</p></a>'.format(
            reverse('dialog', args=(auth,)))
    except:
        return 0


@register.simple_tag
def Unreaded(account_id):
    sql = """
    SELECT COUNT(*) as count
    FROM
    (select d.id from
        `circle_dialog` d
    join circle_record R1 ON R1.auth_id = d.authB_id and d.id = R1.dialog_id
    WHERE d.`authA_id` = '{account_id}' and d.authB_id != '{account_id}' and R1.viewed < R1.createdate
    UNION
    select d.id from
        `circle_dialog` d
    join circle_record R2 ON R2.auth_id = d.authA_id and d.id = R2.dialog_id
    WHERE d.`authB_id` = '{account_id}' and d.authA_id != '{account_id}' and R2.viewed < R2.createdate
    ) as tmp
    """.format(account_id=account_id)
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    countmsgs=int(row[0])
    msg=''
    try:
        msg=AllMsg.objects.get(user=account_id, type=0)
    except:
        pass
    if msg != '':
        countmsgs+=int(msg.unreaded)
    if countmsgs == 0:
        return ''
    else:
        return "<span>%s</span>" % countmsgs

@register.simple_tag
def UnreadedNmo(account_id):
    countmsgs=0
    msg=''
    try:
        msg=AllMsg.objects.get(user=account_id, type=1)
    except:
        pass
    if msg != '':
        countmsgs=int(msg.unreaded)
    if countmsgs == 0:
        return ''
    else:
        return "<span>%s</span>" % countmsgs

@register.filter
def allmsgs_index(List, i):
    return List[int(i)]

@register.filter
def allmsgs_cut(string):
    msgs=re.split("\|",string)
    text=list()
    for msg in msgs:
        if msg!='':
           text.append(msg)
    return text

@register.filter
def allmsgsdate_cut(string):
    msgs=re.split("\|",string)
    date=list()
    for msg in msgs:
        if msg!='':
            date.append(datetime.datetime.strptime(msg, "%Y-%m-%d %H:%M:%S.%f+00:00"))
    return date


@register.filter
def IfNone(string):
    if string == '' or string == None or string == 'None' or string == 0 or string == '0' or string == '32' or string == u'нет' or string == u'Нет категории':
        return u"Нет"
    else:
        return u"%s" % string


@register.filter
def IsData(string):
    if string == '' or string == None or string == 'None' or string == 0 or string == '0' or string == '32' or string == u'нет' or string == u'Нет категории' or string == u'Нет':
        return False
    else:
        return True


"""a:1:{i:0;s:21:"врач-уролог";}"""


@register.filter
def normalize(string):
    if string == None or string == "None" or string == "none":
        return ""
    try:
        r = string.split('{')
    except:
        return string
    if len(r) == 1:
        return string
    return r[1].split('"')[1]


@register.simple_tag
def get_avatar_fname(account_id):
    user = MyUser.objects.get(id=account_id)

    if user.avatar.name.find("media") != -1:
        return user.avatar.name
    else:
        return u'/media/' + user.avatar.name


@register.simple_tag
def get_preview_sizexy(fnameurl, sizex, sizey):
    if fnameurl == "":
        return u'/media/old/249_399/mt.png'

    fnameurl = str(fnameurl)
    fname = os.path.basename(fnameurl)
    dirname = os.path.basename(os.path.dirname(fnameurl))
    thumb = 'thumb_{0}_{1}_{2}'.format(sizex, sizey, fname)
    path = os.path.join(settings.MEDIA_ROOT, dirname)
    infile = os.path.join(path, fname)
    outfile = os.path.join(path, thumb)
    if (os.path.isfile(outfile)):
        return u'/media/{0}/{1}'.format(dirname, thumb)
    try:
        resize_and_crop(infile, outfile, [sizex, sizey], 'middle')
        return u'/media/{0}/{1}'.format(dirname, thumb)
    except:
        return fnameurl


@register.simple_tag
def get_image_url(fnameurl):
    fnameurl = str(fnameurl)
    fname = os.path.basename(fnameurl)
    dirname = os.path.basename(os.path.dirname(fnameurl))

    return u'/media/{0}/{1}'.format(dirname, fname)


@register.simple_tag
def get_preview_calculate(fnameurl):
    fnameurl = str(fnameurl)
    fname = os.path.basename(fnameurl)
    dirname = os.path.basename(os.path.dirname(fnameurl))
    path = os.path.join(settings.MEDIA_ROOT, dirname)
    infile = os.path.join(path, fname)
    try:
        img = Image.open(infile)
    except:
        return fnameurl

    sizex = 0
    sizey = 0
    (width, height) = img.size
    k = float(width) / float(height)
    if k > 1:
        sizey = int(430 / k)
    else:
        sizey = int(223 / k)
    if k > 1:
        sizex = 430
    else:
        sizex = 223
    thumb = 'thumb_{0}_{1}_{2}'.format(sizex, sizey, fname)
    outfile = os.path.join(path, thumb)
    if (os.path.isfile(outfile)):
        return u'/media/{0}/{1}'.format(dirname, thumb)
    try:
        resize_and_crop(infile, outfile, [sizex, sizey], 'middle')
        return u'/media/{0}/{1}'.format(dirname, thumb)
    except:
        return fnameurl


@register.simple_tag
def get_avatar_preview_sizexy(account_id, sizex, sizey):
    try:
        user = MyUser.objects.get(id=account_id)
    except:
        return 'none'
    fname = os.path.basename(user.avatar.name)
    thumb = u'thumb_{0}_{1}_{2}'.format(sizex, sizey, fname)
    path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
    infile = os.path.join(path, fname)
    outfile = os.path.join(path, thumb)
    if (os.path.isfile(outfile)):
        return u'/media/profile_images/{0}'.format(thumb)
    try:
        resize_and_crop(infile, outfile, [sizex, sizey], 'middle')
        return u'/media/profile_images/{0}'.format(thumb)
    except:
        return u'/media/profile_images/{0}'.format(fname)


@register.simple_tag
def get_avatar_preview_sizexy_hax(avatar_name, sizex, sizey):
    if avatar_name is None:
        return 'none'
    fname = os.path.basename(avatar_name)
    thumb = 'thumb_{0}_{1}_{2}'.format(sizex, sizey, fname)
    path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
    infile = os.path.join(path, fname)
    outfile = os.path.join(path, thumb)
    if (os.path.isfile(outfile)):
        return u'/media/profile_images/{0}'.format(thumb)
    try:
        resize_and_crop(infile, outfile, [sizex, sizey], 'middle')
        return u'/media/profile_images/{0}'.format(thumb)
    except:
        return u'/media/profile_images/{0}'.format(fname)


@register.simple_tag
def get_avatar_preview(account_id):
    user = MyUser.objects.get(id=account_id)
    fname = os.path.basename(user.avatar.name)
    thumb = 'thumb_{0}'.format(fname)
    path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
    if (os.path.isfile(os.path.join(path, thumb))):
        return u'/media/profile_images/{0}'.format(thumb)
    else:
        if (handle_uploaded_file(fname)):
            return u'/media/profile_images/{0}'.format(thumb)
        else:
            return u'/media/profile_images/{0}'.format(fname)


def handle_uploaded_file(fname):
    try:
        path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
        outfile = os.path.join(path, u'thumb_{0}'.format(fname))
        im = Image.open(os.path.join(path, fname))
        im.thumbnail(size)
        im.save(outfile, "JPEG")
        return True
    except:
        return False


@register.assignment_tag
def nows():
    query = Events.objects.filter(type_id__in=[1, 2, 3, 5, 6]).extra(
        where=["NOW() BETWEEN `start` AND `end`"])
    if query.exists():
        index = random.randint(0, query.count() - 1)
        if query:
            return query[index]
        else:
            return None
    else:
        return None


@register.assignment_tag
def afters():
    query = Events.objects.filter(type_id__in=[1, 2, 3, 5, 6]).extra(where=[
        "DATE(`start`)>DATE(NOW()) AND DATE(`start`)<=DATE_ADD(NOW(), INTERVAL 90 DAY)"])
    if query.exists():
        index = random.randint(0, query.count() - 1)
        if query:
            return query[index]
        else:
            return None
    else:
        return None


@register.simple_tag
def online():
    on = Settings.objects.all()[:1]
    if on.exists() and on[0].online:
        if on[0].translation:
            from django.core.urlresolvers import reverse
            url = reverse('detailtranslation', kwargs={'pk': on[0].translation.pk})
            return u'<div class="left-block-content-links-item-count" style="top: 2px;right: -7px;"><a href="{url}"><span style="background-color:#e1523d;font-size: 13px;">Прямой эфир!</span></a></div>'.format(
                url=url)
        else:
            return u'<div class="left-block-content-links-item-count" style="top: 2px;right: -7px;"><span style="background-color:#e1523d;font-size: 13px;">Прямой эфир!</span></div>'
    else:
        return u''

@register.simple_tag
def online2():
    on = Settings.objects.all()[:1]
    if on.exists() and on[0].online:
        if on[0].translation:
            from django.core.urlresolvers import reverse
            url = reverse('detailtranslation', kwargs={'pk': on[0].translation.pk})
            return u'<div id="center-block-online"><a href="{url}" ><div class="online-arrows"><img src="/static/images/strelki.png"/></div>' \
                   u'<div class="online-arrows"><span>Внимание! Идет прямой эфир!</span></div><div class="online-arrows"><img src="/static/images/strelki2.png"/></div></a></div>'.format(url=url)
        else:
            return u'<div id="center-block-online"><div class="online-arrows"><img src="/static/images/strelki.png"/></div><a href="" >' \
                   u'<div class="online-arrows"><span>Внимание! Идет прямой эфир!</span></div></a><div class="online-arrows"><img src="/static/images/strelki2.png"/></div></div>'
    else:
        return u''

@register.simple_tag(takes_context=True)
def count_new_events(context, model, service_id=None):
    count = 0
    request = context['request']

    if request.user.is_anonymous():
        return ''

    key = unicode(model)
    if service_id:
        key = key + unicode(service_id)

    key_event = key.lower()
    from account.models import EventAccess
    last_access = EventAccess.last_access(key_event, request.user)
    if not last_access:
        from django.utils import timezone
        last_access = timezone.localtime(timezone.now())

    Model = False

    if model == 'Events':
        from events.models import Events as Model
    if model == 'Videos':
        from videos.models import Videos as Model
    if model == 'PGalleries':
        from photos.models import PGalleries as Model
    if model == 'Posts' or model == 'PostLinks':
        from posts.models import Posts as Model
    if model == 'Records':
        from records.models import Records as Model
    if model == 'Rss':
        from rss.models import Posts as Model

    if Model:
        count = Model.objects.filter(createdate__gt=last_access)
    if service_id and model == 'Posts':
        count = count.filter(type=service_id)
    if service_id and model == 'Rss':
        count = count.filter(show=True)

    if model == 'PostLinks':
        from groups_posts.views import PostsList
        postlist = PostsList.get_postslinks(request)
        count = count.filter(id__in=postlist.keys())

    qnt = count.count()
    if qnt:
        return '<div class="left-block-content-links-item-count"><span>{0}</span></div>'.format(qnt)
    else:
        return ''


@register.simple_tag
def nonactivated(user_id):
    nonactivated = GroupUsers.objects.filter(user_id=user_id, activated=0).exclude(
        group_id__user_id__id=user_id).count()
    if nonactivated:
        return '<div class="left-block-content-links-item-count"><span>' + str(nonactivated) + '</span></div>'
    else:
        return ''


def exists(site, path):
    conn = httplib.HTTPConnection(site)
    conn.request('HEAD', path)
    response = conn.getresponse()
    conn.close()
    return response.status == 200


@register.simple_tag
def selectfrom(siteA, pathA, siteB, pathB):
    if exists(siteA, pathA):
        return u'%s%s' % (siteA, pathA)
    elif exists(siteB, pathB):
        return u'%s' % (pathB)
    return 'None'


@register.simple_tag
def selectfromEx(siteA, pathA, localpath):
    if exists(siteA, pathA):
        return u'http://%s%s' % (siteA, pathA)
    else:
        return u'%s' % (localpath)
    return 'None'


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def URL():
    return settings.SITE_URL


@register.filter
def get_send_invite_refuse_invite_refuse_invited(owner, item):
    invite = Circle.objects.filter(Q(parent=owner) & Q(friend=item) & Q(activated=False))
    invited = Circle.objects.filter(Q(parent=item) & Q(friend=owner) & Q(activated=False))
    if invite.count():
        return 'tpl_refuse_invite'
    elif invited.count():
        return 'tpl_refuse_invited'
    else:
        return 'tpl_send_invite'


@register.filter
def isUserIntoMyCircle(parent, friend):
    frend = Circle.objects.filter(
        ((Q(parent_id=parent) & Q(friend_id=friend)) | (Q(parent_id=friend) & Q(friend_id=parent))) & Q(activated=1))
    if frend.count():
        return 1
    else:
        return 0


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '00')


@register.assignment_tag
def users_by_spec():
    from account.models import MyUser
    return MyUser.objects.values('spec_id__name').annotate(count=Count('id')).order_by('-count')


@register.simple_tag
def count_online_users():
    from django.utils import timezone
    from datetime import timedelta
    time_threshold = timezone.localtime(timezone.now()) - timedelta(minutes=15)
    results = MyUser.objects.filter(lastaccess__gt=time_threshold).count()
    return results


@register.simple_tag
def count_materials():
    results = 0
    results += Videos.objects.count()
    results += Posts.objects.count()
    results += Events.objects.count()
    return results


@register.simple_tag(takes_context=True)
def last_access(context):
    request = context['request']
    from django.utils import timezone
    now = timezone.localtime(timezone.now())
    if request.user.is_authenticated():
        request.user.lastaccess = now
        request.user.save()

    return ''


@register.simple_tag
def morph_words(number, word1, word2, word3):
    try:
        if type(number) == str:
            number = int(number)
    except Exception:
        return word3

    if number > 19:
        number %= 10

    if number == 1:
        return word1
    elif 1 < number < 5:
        return word2
    else:
        return word3