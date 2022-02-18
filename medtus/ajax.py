# -*- coding: utf-8 -*-


#from settings.views import send_email
from django.conf import settings
from django.core.mail import send_mail
from .models import Feedback, PrivateContentPageUsers, ContentPage
from django.template.loader import render_to_string
import json
from django.http import HttpResponse

def feedback(request):

    topic=request.GET.get('topic')
    name=request.GET.get('name')
    position=request.GET.get('position')
    contact=request.GET.get('contact')
    text=request.GET.get('text')
    result='None'
    if not topic or not name or not contact or not text or not position:
        result="Необходимо заполнить все поля!"
        return HttpResponse(result)

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
            result='Спасибо! Сообщение отправлено. Мы обязательно ответим Вам.'
            #dajax.script("$('#message').click();")
        except:
            result=u'Что-то пошло не так при отправке. Попробуйте позже.'

    else:
        result='Что-то пошло не так. Попробуйте позже.'

    return HttpResponse(result)


def getAccess(request):

    full_name=request.GET.get('full_name')
    city=request.GET.get('city')
    speciality=request.GET.get('speciality')
    email=request.GET.get('email')
    page=request.GET.get('page')
    phone=request.GET.get('phone')

    if not full_name or not city or not speciality or not page:
        result="Необходимо заполнить все поля!"
        return HttpResponse(result)

    content_page = ContentPage.objects.get(pk=int(page))


    if not email:            
        email = ''
    
    if not phone:
        phone = ''

    message = PrivateContentPageUsers(full_name=full_name, email=email, city=city, speciality=speciality, page=content_page, phone=phone)    

    message.save()
    
    if message.pk:
        try:            
            result=u'Спасибо! Ваши данные отправлены. Нажмите Ок и получите доступ.'
            #dajax.script("$('#contactForm').remove();")
            #dajax.script("$('html').css('overflow-y','unset');")
        except:
            result=u'Что-то пошло не так при отправке. Попробуйте позже.'

    else:
        result='Что-то пошло не так. Попробуйте позже.'

    return HttpResponse(result)
