# -*- coding: utf-8 -*-

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
#from settings.views import send_email
from django.conf import settings
from django.core.mail import send_mail
from .models import Feedback, PrivateContentPageUsers, ContentPage
from django.template.loader import render_to_string
import json

@dajaxice_register
def feedback(request, topic, name, position, contact, text):
    dajax = Dajax()

    if not topic or not name or not contact or not text or not position:
        dajax.alert("Необходимо заполнить все поля!")
        return dajax.json()

    message = Feedback(topic=topic, name=name, text=text, contact=contact, position=position)
    message.save()
    context ={
    'topic': topic,
    'name': name,
    'text': text,
    'contact': contact,
    'position': position
    }
    msg=render_to_string('emails/new_feedback_email.html', context)
    if message.pk:
        try:
            send_mail(u"Новое сообщение обратной связи", msg, 'feedback@vrvm.ru', [settings.COORD_EMAIL], fail_silently=True)
            dajax.alert(u'Спасибо! Сообщение отправлено. Мы обязательно ответим Вам.')
            dajax.script("$('#message').click();")
        except:
            dajax.alert(u'Что-то пошло не так при отправке. Попробуйте позже.')

    else:
        dajax.alert('Что-то пошло не так. Попробуйте позже.')

    return dajax.json()

@dajaxice_register
def getAccess(request, full_name, city, speciality, email, page):
    dajax = Dajax()

    if not full_name or not city or not speciality or not page:
        dajax.alert("Необходимо заполнить все поля!")
        return dajax.json() 

    content_page = ContentPage.objects.get(pk=int(page))
    if not email:            
        message = PrivateContentPageUsers(full_name=full_name, email='', city=city, speciality=speciality, page=content_page)
    else:
        message = PrivateContentPageUsers(full_name=full_name, email=email, city=city, speciality=speciality, page=content_page)

    message.save()
    
    if message.pk:
        try:            
            dajax.alert(u'Спасибо! Ваши данные отправлены. Нажмите Ок и получите доступ.')
            dajax.script("$('#contactForm').remove();")
            dajax.script("$('html').css('overflow-y','unset');")
        except:
            dajax.alert(u'Что-то пошло не так при отправке. Попробуйте позже.')

    else:
        dajax.alert('Что-то пошло не так. Попробуйте позже.')

    return dajax.json()