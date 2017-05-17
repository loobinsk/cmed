# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.exceptions import PermissionDenied
from django.template.response import SimpleTemplateResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect

from comments.models import Comments
from mce_filebrowser.admin import MCEFilebrowserAdmin
from django import forms
from account.models import MyUser
from account.mixins import StaffPermissionMixin


class CommentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        if 'user_id' in self.initial:
            self.fields['user_id'].queryset = MyUser.objects.filter(pk=self.initial['user_id'])
        else:
            self.fields['user_id'].queryset = MyUser.objects.filter(pk=self.initial['user_id'])


class CommentsAdmin(StaffPermissionMixin, MCEFilebrowserAdmin):
    # list_display = ('id', 'title', 'content', 'createdate')
    list_display = ('id', 'link', 'content', 'createdate',
                    'user_id', 'user_lname', 'user_fname',
                    'user_surname', 'user_town', 'user_country',
                    'user_spec_id', 'user_graduate')

    def user_fname(self, obj):
        return obj.user_id.firstname

    def user_lname(self, obj):
        return obj.user_id.lastname

    def user_surname(self, obj):
        return obj.user_id.surname

    def user_town(self, obj):
        if hasattr(obj.user_id, 'town'):
            return obj.user_id.town
        else:
            return ""

    def user_country(self, obj):
        if hasattr(obj.user_id, 'country'):
            return obj.user_id.country
        else:
            return ""

    def user_spec_id(self, obj):
        if hasattr(obj.user_id, 'spec_id'):
            return obj.user_id.spec_id
        else:
            return ""

    def user_graduate(self, obj):
        if hasattr(obj.user_id, 'graduate'):
            return obj.user_id.graduate
        else:
            return ""

    def link(self, obj):
        if hasattr(obj, 'link'):
            return mark_safe("<a href='{0}'>Пост</a>".format(obj.link))
        else:
            return ""

    search_fields = ('title', 'content')
    list_filter = ('createdate', )
    form = CommentsForm

    def get_actions(self, request):
        actions = self.actions if hasattr(self, 'actions') else []
        actions.append('csv_export')
        # actions.append('truncate')
        return super(CommentsAdmin, self).get_actions(request)

    def changelist_view(self, request, extra_context=None):
        from django.contrib.admin import helpers
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        if selected or request.POST.get('action', False) not in (u'csv_export', ):
            return super(CommentsAdmin, self).changelist_view(request, extra_context)

        from django.contrib.admin.views.main import ERROR_FLAG

        if not self.has_change_permission(request, None):
            raise PermissionDenied

        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)

        actions = self.get_actions(request)
        if actions:
            list_display = ['action_checkbox'] + list(list_display)

        ChangeList = self.get_changelist(request)
        try:
            cl = ChangeList(request, self.model, list_display,
                list_display_links, list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related,
                self.list_per_page, self.list_max_show_all, self.list_editable,
                self)
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET.keys():
                return SimpleTemplateResponse('admin/invalid_setup.html', {
                    'title': _('Database error'),
                })
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

        response = self.csv_export(request, qs=cl.get_queryset(request))

        return response

    def csv_export(self, request, qs=None, *args, **kwargs):
        from account.admin import MyUserAdmin
        user_admin = MyUserAdmin(MyUser, self.admin_site)
        users = []
        for comment in qs:
            if comment.user_id not in users:
                users.append(comment.user_id)

        return user_admin.export_list(request, users)

    def save_model(self, request, obj, form, change):
        obj.safe = True
        obj.save()

    csv_export.short_description = \
        'Exported selected %(verbose_name_plural)s as CSV'


class CommentsAdminLink():

    def comments_link(self, obj):
        from django.core.urlresolvers import reverse
        url = reverse('admin:comments_comments_changelist')
        model = obj._meta.model
        count = len(Comments.objects.filter(object_id=obj.id, service_id=model.SERVICE_ID))
        return u"<a target='_blank' href='{0}?object_id={1}&service_id={2}'>{3} шт.</a>".format(url,
                                                                                                    obj.id,
                                                                                                    model.SERVICE_ID,
                                                                                                    count)
    comments_link.allow_tags = True
    comments_link.short_description = "Комментарии"


admin.site.register(Comments, CommentsAdmin)
