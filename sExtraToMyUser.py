#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, gc

# Start execution here!
if __name__ == '__main__':
    print 'Starting Rango population script...'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmedu.settings')
    from account.models import MyUser
    from medtus.models import Countries, Towns, Sextrafields
    
    sextra = Sextrafields.objects.filter(object_id__in=[i for i in range(76340,80000)])
    for s in sextra:
        try:
            u = s.object_id
        except MyUser.DoesNotExist:
            continue
        name = s.name
        value = s.value
        if u != None:
            if name == 'city':
                try:
                    town = Towns.objects.get(name=value)
                except Towns.DoesNotExist:
                    continue
                except Towns.MultipleObjectsReturned:
                    continue
                if town != None:
                    u.town = town
                    if town.country_id != None:
                        try:
                            country = Countries.objects.get(id=town.country_id)
                        except Countries.DoesNotExist:
                            continue
                        if country != None:
                            u.country = country
            if name=='phone':
                u.phone_number = value
            if name=='icq':
                u.ICQ_Skype = value
            if name=='experience':
                u.experience = value
            if name=='vuz':
                u.school = value
            if name=='diser_theme':
                u.dissertation = value
        try:
            u.save()
        except:
            continue
        gc.collect()
