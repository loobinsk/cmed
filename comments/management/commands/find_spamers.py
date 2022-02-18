# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
import StringIO
import csv
from django.utils import timezone
from datetime import timedelta
from comments.models import Comments
from circle.models import Record
from settings.views import send_email
from settings.models import Settings


class Command(BaseCommand):
    help = u'Составляет отчеты об одинаковых личных сообщениях и комментариях'

    def from_private(self, set):
        domain = "www.vrachivmeste.ru"
        output = StringIO.StringIO()
        writer = csv.DictWriter(output, fieldnames=['id', 'link', 'cnt', 'message'])
        writer.writeheader()
        if set.spam_report_period > 0:
            records = Record.objects.filter(createdate__gte=timezone.now() - timedelta(days=set.spam_report_period))
        else:
            records = Record.objects.all()
        records = records.values('auth_id', 'value').annotate(cnt=Count('id')).filter(cnt__gt=1).order_by('-cnt')
        for r in records:
            url = 'https://' + domain + reverse('admin:account_myuser_change', args=(r['auth_id'],))
            writer.writerow({'id': r['auth_id'], 'message': r['value'].encode('utf-8'), 'cnt': r['cnt'], 'link': url})
        if records:
            return output.getvalue()
        else:
            return ''

    def from_comments(self, set):
        domain = "www.vrachivmeste.ru"
        output = StringIO.StringIO()
        writer = csv.DictWriter(output, fieldnames=['id', 'link', 'cnt', 'message'])
        writer.writeheader()
        if set.spam_report_period > 0:
            records = Comments.objects.filter(createdate__gte=timezone.now() - timedelta(days=set.spam_report_period))
        else:
            records = Comments.objects.all()
        records = records.values('user_id', 'content').annotate(cnt=Count('id')).filter(cnt__gt=1).order_by('-cnt')
        for r in records:
            url = 'https://' + domain + reverse('admin:account_myuser_change', args=(r['user_id'],))
            writer.writerow({'id': r['user_id'], 'message': r['content'].encode('utf-8'), 'cnt': r['cnt'], 'link': url})
        if records:
            return output.getvalue()
        else:
            return ''

    def handle(self, *args, **options):
        set = Settings.objects.first()
        if not set or not set.spam_report_email:
            print('Не настроен email')
            return
        email = EmailMessage(
            'Спамеры',
            'Отчеты об одинаковых личных сообщения и комментариях',
            to=[set.spam_report_email],
        )
        from_private = self.from_private(set)
        if from_private:
            email.attach('private.csv', from_private, 'text/csv')
        from_comments = self.from_comments(set)
        if from_comments:
            email.attach('comments.csv', from_comments, 'text/csv')
        if from_private or from_comments:
            email.send()