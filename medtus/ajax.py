# -*- coding: utf-8 -*-

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from settings.views import send_email
from django.conf import settings
from django.core.mail import send_mail
from .models import Feedback

@dajaxice_register
def feedback(request, topic, name, position, contact, text):
    dajax = Dajax()

    if not topic or not name or not contact or not text or not position:
        dajax.alert("Необходимо заполнить все поля!")
        return dajax.json()

    message = Feedback(topic=topic, name=name, text=text, contact=contact, position=position)
    message.save()

    if message.pk:
        try:
            send_mail(u"Новое сообщение обратной связи", message, 'feedback_email', settings.COORD_EMAIL, fail_silently=False)
            dajax.alert(u'Спасибо! Сообщение отправлено. Мы обязательно ответим Вам.')
        except:
            dajax.alert(u'При отправке произошла ошибка - проверьте правильность emails')

        dajax.script("$('#message').click();")
    else:
        dajax.alert('Что-то пошло не так. Попробуйте позже.')

    return dajax.json()
