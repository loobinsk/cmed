# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from settings.views import dictfetchall
from lecturers.models import Lecturer


class Command(BaseCommand):
    help = u'Импортирует лекторов из таблицы lectors'

    def handle(self, *args, **options):
        sql = """
select l.about_lector, l.short_desc, u.firstname, u.lastname, u.surname, u.avatar
from lectors l
join account_myuser u on l.person_id = u.id;
        """
        cursor = connection.cursor()
        cursor.execute(sql)
        lectors = dictfetchall(cursor)
        imported = not_imported = 0
        for l in lectors:
            surname = l['lastname']
            firstname = l['firstname']
            secondname = l['surname']
            avatar = l['avatar']
            short_desc = l['short_desc']
            content = l['about_lector']
            if not Lecturer.objects.filter(surname=surname, firstname=firstname, secondname=secondname, image=avatar)\
                    .exists():
                Lecturer.objects.create(surname=surname,
                                        firstname=firstname,
                                        secondname=secondname,
                                        image=avatar,
                                        short_desc=short_desc,
                                        content=content)
                imported += 1
            else:
                not_imported += 1
        print(u'Импортировано: %s, не импортировано: %s' % (imported, not_imported))