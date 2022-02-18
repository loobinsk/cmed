# -*- coding: utf-8 -*-
# from dajax.core import Dajax
# from dajaxice.decorators import dajaxice_register
from django.contrib.auth import authenticate
import string, random
from django.core.mail import send_mail
from django.conf import settings
import sys
import re
from groups.models import GroupUsers
from django.http import HttpResponseRedirect, HttpResponse

def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# @dajaxice_register
# def InviteIntoGroup(request, userid, groupids):
#     dajax = Dajax()
#     itog = map(long, re.compile('\d+').findall(groupids))
#     user_groups = [x.group_id_id for x in GroupUsers.objects.filter(user_id=userid)]
#     try:
#         for i in itog:
#             if i not in user_groups:
#                 GroupUsers.objects.create(user_id=userid, group_id_id=i, activated=0, invite=request.user)
#     except:
#         dajax.alert("Ошибка!!! %s" % sys.exc_info()[0])
#         return dajax.json()
#     dajax.alert("Приглашение отправлено")
#     return dajax.json()


def changepass(request):

    oldpassword=request.POST.get('oldpassword')
    password=request.POST.get('password')
    confirmpassword=request.POST.get('confirmpassword')

    user = authenticate(username=request.user.email, password=oldpassword)

    result = 'None'
    if user is not None:
        if password == '' or confirmpassword == '':
            result = u'Пароль не может быть пустым!!!'
        else:

            if password != confirmpassword:
                result = u'Введенные пароли не совпадают!!!'
            else:
                import re
                p = re.compile(ur'[a-z\d]+', re.UNICODE | re.IGNORECASE)
                if re.search(p, password):
                    try:
                        user.set_password(password.encode('utf-8'))
                        user.save()
                        from settings.views import send_email
                        send_email(request, user.email, 'passchange_email', u'Ваш пароль изменен',
                           profile=user, password=password.encode('utf-8'))

                        result = u'Пароль успешно изменен'
                    except:
                        result = 'Unknowed exception! Please write to support.'
                else:
                    result = u'В пароле доступны только символы A-Z и 0-9'
    else:
        result = u"Старый пароль указан неверно"

    return HttpResponse(result)

# @dajaxice_register
# def GiveMeNewPassword(request, email):
#     dajax = Dajax()
#     newpassword = id_generator(6)
#     if email != '':
#         try:
#             user = request.user
#             user.set_password(newpassword)
#             user.save()
#             send_mail('Subject here', 'Here is password {0}.'.format(newpassword), settings.ADMIN_EMAIL, [email], fail_silently=False)
#             message = 'Password have been sent to your email.'
#         except:
#             message = 'Unknowed error! Password have no been sent. Please write to admin!'
#     else:
#         message = 'Email have not to be NULL.'
#     dajax.script(u'ViewMessage("%s");' % message)
#     return dajax.json()
#
# @dajaxice_register
# def InviteCollegue(request, emails, message):
#     dajax = Dajax()
#     try:
#         send_mail(u'Приглашение на Врачи Вместе', message, settings.ADMIN_EMAIL, emails.split(','), fail_silently=False)
#         dajax.alert(u'Приглашение отправлено!')
#     except:
#         dajax.alert(u'При отправке произошла ошибка - проверьте правильность emails')
#     return dajax.json()
#
#
# @dajaxice_register
# def deleteImage(request, image_id):
#     dajax = Dajax()
#     from account.models import AdditionalImage
#     try:
#         image = AdditionalImage.objects.get(pk=image_id)
#         dajax.remove('#user_image_{0}'.format(image.id))
#         image.delete()
#     except AdditionalImage.DoesNotExist:
#         dajax.alert(u"Изображение не найдено.")
#
#     return dajax.json()