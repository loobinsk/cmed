    #!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, gc

# Start execution here!
if __name__ == '__main__':
    print 'Starting Rango population script...'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmedu.settings')
    from account.models import MyUser
    from medtus.models import Countries, Towns, Oextrafields, Sextrafields
    
    oextra = Oextrafields.objects.filter(object_id__in=[i for i in range(73740,80000)])
    for o in oextra:
        try:
            u = o.object_id
        except MyUser.DoesNotExist:
            continue
        name = o.name
        value = o.value
        if u != None:
            if name=='job_comp':
                u.organization = value
            if name=='job_title':
                u.job = value
            if name=='job_site':
                u.site = value
        try:
            u.save()
        except:
            continue
        gc.collect()
