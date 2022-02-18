# -*- coding: utf-8 -*-
from account.models import MyUser
from circle.models import Circle, Dialog, Record
from django.core.urlresolvers import reverse
import sys
from django.db.models import Q
from django.http import HttpResponse


def confirmmycircle(request):
    result='None'
    parentid=request.GET.get('parentid')
    try:
        C = Circle.objects.get(Q(friend=request.user) & Q(parent_id=parentid))
        C.activated = True
        C.save()
        selector_id = '#invited_%s' % parentid
        selector_confirm = '#confirmbutton_%s' % parentid
        selector_new = "#groups-area-new"
        selector_old = "#groups-area-old"
        result=u'Пользователь добавлен в ваш круг!'
        #dajax.remove(selector_confirm)
        #dajax.script(u'$("%s").appendTo("%s");' % (selector_id, selector_old))
        #dajax.script(u'$("%s > .links > .delete-group").html("Удалить из круга");' % selector_id)
    except:
        result=u'Unhandling error - %s' % sys.exc_info()[0]
    return HttpResponse(result)


def removedialog(request):
    result='None'
    dialogid=request.GET.get('dialogid')
    #dajax.remove('#dialog_%s' % dialogid)
    D = Dialog.objects.get(id__exact=dialogid)
    if(D.authA == request.user.id):
        D.auth_b_deleted = 1
    else:
        D.auth_a_deleted = 1
    D.save()
    # R = Record.objects.filter(dialog=D).delete()
    # D.delete();
    return HttpResponse(result)


def removefrommycircle(request):
    friend=request.GET.get('friend')
    Parent = MyUser.objects.get(id=request.user.id)
    Friend = MyUser.objects.get(id=friend)
    Circle.objects.filter((Q(parent_id=Parent.id) & Q(friend_id=Friend.id)) | Q(friend_id=Parent.id) & Q(parent_id=Friend.id)).delete()

    result=u'Готово!'
    return HttpResponse(result)


def inviteintomycircle(request):
    avatar=request.GET.get('avatar')
    parent=request.GET.get('parent')
    friend=request.GET.get('friend')
    if parent == friend:
        result=u'Невозможно добавить в круг самого себя!!!'
        return HttpResponse(result)
    Parent = MyUser.objects.get(id=parent)
    Friend = MyUser.objects.get(id=friend)
    html = u'<div class="holder" id="invite_%s">\
					<div class="content-block-center-item-head-photo-bg">\
						<a target="_parent" href="#">\
						<div class="content-block-center-item-head-photo" style="background-image:url(%s), url(%s)"></div>\
						</a>\
					</div>\
					<div class="description">\
						<h3><a href="%s">%s %s %s</a> <em>%s</em></h3>\
						<div class="link-holder">\
							<a href="%s" class="link-write">написать личное сообщение</a>\
						</div>\
					</div>\
					<div class="links">\
						<a class="delete-group" style="cursor:pointer;" onclick="Dajaxice.circle.removefrommycircle(Dajax.process, {\'friend\':\'%s\', \'ID\':\'invite_%s\'})">Удалить</a>\
					</div>\
				</div>'
    out = ''
    C = Circle.objects.filter( (Q(parent_id=parent) & Q(friend_id=friend)) | (Q(friend_id=parent) & Q(parent_id=friend)) )
    if C.count() is 0:
        C = Circle()
        C.parent = Parent
        C.friend = Friend
        C.save()
        out = html % (friend, avatar, Friend.avatar, reverse('lichnie2', kwargs={'userid':friend}), Friend.lastname, Friend.firstname, Friend.surname, Friend.spec_id, reverse('dialog', kwargs={'authBid':friend}), friend, friend)
        result=u'Приглашение в ваш круг отправлено!'
    else:
        result=u'Возможно, пользователь уже в вашем круге?!!'
    #dajax.prepend('.groups-area', 'innerHTML', u'%s' % out)
    return HttpResponse(result)
