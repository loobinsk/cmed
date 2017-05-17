# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import PGalleries, PGPhotos
from comments.admin import CommentsAdminLink
from account.mixins import StaffPermissionMixin
# Register your models here.


class PGPhotosAdmin(admin.TabularInline):
    model = PGPhotos
    exclude = ('user', 'createdate', 'updatedate', 'comment_cnt', 'rating', 'votes')
    extra = 3

    def __str__(self):
        return self.id




class PGalleriesAdmin(StaffPermissionMixin, admin.ModelAdmin, CommentsAdminLink):
    list_display = ('id', 'comments_link', 'title', 'createdate', 'status')

    inlines = (PGPhotosAdmin,)

    exclude = ('user', )


    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(new_object)
        return super(PGalleriesAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super(PGalleriesAdmin, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):
        for photo in obj.pgphotos_set.all():
            photo.user = obj.user
            photo.save()

        return obj


admin.site.register(PGalleries, PGalleriesAdmin)