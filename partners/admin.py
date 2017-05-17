from django.contrib import admin

# Register your models here.

from .models import Partner, Rubric

class PartnerAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'url', 'rubric',)
    list_display = ('id', 'name', 'image', 'url', 'rubric',)

class RubricAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name',)

admin.site.register(Partner, PartnerAdmin)
admin.site.register(Rubric, RubricAdmin)
