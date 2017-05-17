from django.contrib import admin
from lecturers.models import Lecturer, LecturerLink


class LecturerLinkInline(admin.TabularInline):
    model = LecturerLink
    extra = 1


class LecturerAdmin(admin.ModelAdmin):
    inlines = [LecturerLinkInline]


admin.site.register(Lecturer, LecturerAdmin)