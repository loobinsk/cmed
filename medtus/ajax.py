# -*- coding: utf-8 -*-
__author__ = 'PekopT'

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register


@dajaxice_register
def feedback(request, topic, name, position, contact, text):
    dajax = Dajax()

    if not topic or not name or not contact or not text or not position:
        dajax.alert("Необходимо заполнить все поля!")
        return dajax.json()

    from models import Feedback
    message = Feedback(topic=topic, name=name, text=text, contact=contact, position=position)
    message.save()

    if message.pk:
        from settings.views import send_email
        from account.models import MyUser
        to = [u.email for u in MyUser.objects.filter(is_admin=True, is_active=True)]
        for email in to:
            send_email(request, email, 'feedback_email', u"Новое сообщение обратной связи", message=message)
        dajax.script("$('#message').click();")
        dajax.alert('Спасибо! Сообщение отправлено. Мы обязательно ответим Вам.')
    else:
        dajax.alert('Что-то пошло не так. Попробуйте позже.')

    return dajax.json()
