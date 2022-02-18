from django.contrib import admin

from groups.models import Group
import os
from django.conf import settings
#from mce_filebrowser.admin import MCEFilebrowserAdmin

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'members_count', 'posts_count', 'createdate')

    def members_count(self, obj):
        return obj.calcCountUsers()


    def posts_count(self, obj):
        return obj.calcCountPosts()

    def save_model(self, request, obj, form, change):
        obj.save()

        if request.FILES.get('image'):
            file_path = obj.image.name
            obj.image = os.path.join(settings.MEDIA_URL, file_path)
            obj.save()



admin.site.register(Group, GroupAdmin)
