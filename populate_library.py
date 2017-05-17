#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

#class Graduate(models.Model):
#    name = models.CharField(max_length=128, unique=True)
#
#class Title(models.Model):
#    name = models.CharField(max_length=128, unique=True)
#
#class School(models.Model):
#    name = models.CharField(max_length=128, unique=True)
#
#class Country(models.Model):
#    name = models.CharField(max_length=128, unique=True)
#
#class Town(models.Model):
#    country = models.ForeignKey(Country)
#    name = models.CharField(max_length=128, unique=True)

spec = [ u'Авиационная и космическая медицина', u'Акушерка', u'Аллерголог', u'Анестезиолог', u'Бактериолог', u'Вирусолог', u'Врач востановительной медицины', u'Врач коммунальной гигиены', u'Врач лабораторной диагностики', u'Врач общей гигиены', u'Врач общей практики', u'Врач скорой помощи', u'Врач ультразвуковой диагностики', u'Врач функциональной диагностики', u'Врач-трансфузиолог', u'Гастроэнтеролог', u'Гематолог', u'Генетик', u'Гепатолог', u'Геронтолог', u'Гинеколог', u'Дезинфектолог', u'Дерматовенеролог', u'Детский инфеционист', u'Детский кардиолог', u'Детский невролог', u'Детский онколог', u'Детский ортопед', u'Детский психиатр', u'Детский хирург', u'Диабетолог', u'Диетолог', u'Иммунолог', u'Инфекционист', u'Кардиолог', u'Кардиохирург', u'Клиническая микология', u'Клинический психолог', u'Клинический фармаколог', u'Колопроктолог', u'Косметолог', u'Лабораторная микология', u'Лечебная физкультура и спортивная медицина', u'Маммолог', u'Мануальный терапевт', u'Медбрат', u'Медицинский лабораторный техник', u'Медсестра', u'Нарколог', u'Невролог', u'Нейрохирург', u'Неонатолог', u'Нефролог', u'Онколог', u'Организатор здравоохранения', u'Ортодонт', u'Остеопат', u'Оториноларинголог', u'Офтальмолог', u'Паразитолог', u'Патологоанатом', u'Патофизиолог', u'Педиатр', u'Пластический хирург', u'Провизор', u'Профпатолог', u'Психиатр', u'Психотерапевт', u'Пульмонолог', u'Радиолог', u'Реабилитолог', u'Ревматолог', u'Рентгенолог', u'Рефлексотерапевт', u'Санитарный врач', u'Сексолог', u'Стоматолог', u'Студент', u'Судебно-медицинский эксперт ', u'Судмедэксперт', u'Судовой врач', u'Терапевт', u'Токсиколог', u'Торакальный хирург', u'Травматолог', u'Трансплантолог', u'Трансфузиолог', u'Уролог', u'Фармацевт', u'Фельдшер', u'Физиолог', u'Физиотерапевт', u'Флеболог', u'Фтизиатр', u'Хирург', u'Челюстно-лицевой хирург', u'Эмбриолог', u'Эндокринолог', u'Эндоскопист', u'Эпидемиолог' ]

topic = [ u'Новость', u'Научная статья', u'Клинический случай', u'Вопрос коллегам', u'Частное мнение', u'Обсуждение препарата', u'Анонс мероприятия', u'Видеоматериалы', u'Мероприятия' ]

def populate():
    add_title(u'нет')
    add_title(u'Доцент')
    add_title(u'Профессор')
    add_title(u'Член-корреспондент РАН')
    add_title(u'Действительный член (академик) РАН')
    add_title(u'Член-корреспондент РАМН')
    add_title(u'Действительный член (академик) РАМН')
    add_title(u'Член-корреспондент РАСХН')
    add_title(u'Действительный член (академик) РАСХН')
    add_title(u'Член-корреспондент РАО')
    add_title(u'Действительный член (академик) РАО')
    add_title(u'Член-корреспондент РАХ')
    add_title(u'Действительный член (академик) РАХ')
    add_title(u'Член-корреспондент РААСН')
    add_title(u'Действительный член (академик) РААСН')
    add_title(u'Член-корреспондент РАЕН')
    add_title(u'Действительный член (академик) РАЕН')
    
    add_school(u'МЭИ')
    add_school(u'УрГУПС')
    add_school(u'МГУ')

    country=u'Россия'
    c = add_country(country)
    add_town(country=c, town=u'Москва')
    add_town(country=c, town=u'Санкт-Петербург')
    country=u'Ангола'
    c = add_country(country)
    add_town(country=c, town=u'Столица Анголы')
    add_town(country=c, town=u'Деревня Анголы')
    country=u'Иран'
    c = add_country(country)
    add_town(country=c, town=u'Кувейт')
    add_town(country=c, town=u'Дамаск')
    for s in spec:
        add_spec(s)
    for t in topic:
        add_topic(t)
    
def add_topic(top):
    t = Topic.objects.get_or_create(name=top)[0]
    return t    

def add_spec(speciality):
    s = Spec.objects.get_or_create(name=speciality)[0]
    return s
        
def add_graduate(graduate):
    g = Graduate.objects.get_or_create(name=graduate)[0]
    return g

def add_title(title):
    t = Title.objects.get_or_create(name=title)[0]
    return t

def add_school(school):
    s = School.objects.get_or_create(name=school)[0]
    return s

def add_country(country):
    c = Country.objects.get_or_create(name=country)[0]
    return c

def add_town(country, town):
    t = country.town_set.create( name=town )
    return t

# Start execution here!
if __name__ == '__main__':
    print 'Starting Rango population script...'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmedu.settings')
    from library.models import Graduate, Title, School, Country, Town, Spec, Topic
    populate()
