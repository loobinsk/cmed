# -*- coding: utf-8 -*-

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from settings.views import send_email
from django.conf import settings
from django.core.mail import send_mail
from .models import Feedback
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
    msg=render_to_string('emails/feedback_email.html', context)
    if message.pk:
        try:
            send_mail(u"Новое сообщение обратной связи", msg, 'feedback@vrvm.ru', ['artexmail@gmail.com'], fail_silently=True)
            dajax.alert(u'Спасибо! Сообщение отправлено. Мы обязательно ответим Вам.')
            dajax.script("$('#message').click();")
        except:
            dajax.alert(u'Что-то пошло не так при отправке. Попробуйте позже.')

    else:
        dajax.alert('Что-то пошло не так. Попробуйте позже.')

    return dajax.json()
