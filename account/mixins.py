# -- coding: utf-8 --
__author__ = 'PekopT'

from django.contrib import admin
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.exceptions import PermissionDenied
from django.template.response import SimpleTemplateResponse
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect


class CSVTruncateAdmin(admin.ModelAdmin):
    """
    Adds a CSV export action to an admin view.
    """

    # This is the maximum number of records that will be written.
    # Exporting massive numbers of records should be done asynchronously.
    csv_record_limit = 1000

    extra_csv_fields = ()

    maps = {
        'user_id': 'user',
        'user_fname': 'user__firstname',
        'user_lname': 'user__lastname',
        'user_surname': 'user__surname',
        'user_spec_id': 'user__spec_id',
        'user_graduate': 'user__graduate',
        'user_town': 'user__town',
        'user_country': 'user__country',
        'post_title': 'post__title',
        'timer': 'time'
    }

    def changelist_view(self, request, extra_context=None):
        from django.contrib.admin import helpers
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        if selected or request.POST.get('action', False) not in (u'csv_export', u'truncate'):
            return super(CSVTruncateAdmin, self).changelist_view(request, extra_context)

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

        return self.csv_export(request, qs=cl.get_queryset(request))

    def get_actions(self, request):
        actions = self.actions if hasattr(self, 'actions') else []
        actions.append('csv_export')
        actions.append('truncate')
        actions = super(CSVTruncateAdmin, self).get_actions(request)
        return actions

    def get_extra_csv_fields(self, request):
        return self.extra_csv_fields

    def truncate(self, request, qs=None):
        qs.delete()

    def export_list(self, request, objects):
        import csv
        from django.http import HttpResponse
        from django.template.defaultfilters import slugify

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' \
                                          % slugify(self.model.__name__)
        headers = list(self.list_display) + list(self.get_extra_csv_fields(request))
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.DictWriter(response, headers, delimiter=";")

        # Write header.
        header_data = {}

        for name in headers:
            keyName = name

            if name in self.maps.keys():
                name = self.maps[name]
            if hasattr(self, name) \
                    and hasattr(getattr(self, name), 'short_description'):
                header_data[keyName] = getattr(
                    getattr(self, name), 'short_description')
            else:
                field_data = name.split('__')
                if len(field_data) > 1:
                    for_model = self.model._meta.get_field_by_name(field_data[0])
                    field = for_model[0].rel.to._meta.get_field_by_name(field_data[1])
                else:
                    field = self.model._meta.get_field_by_name(field_data[0])

                if field and field[0].verbose_name:
                    header_data[keyName] = field[0].verbose_name
                else:
                    header_data[keyName] = name

                if type(header_data[keyName]) == unicode:
                    header_data[keyName] = header_data[keyName].encode('utf-8')

            header_data[keyName] = header_data[keyName].title()

        writer.writerow(header_data)


        # Write records.
        for r in objects:
            data = {}
            for name in header_data.iterkeys():
                if hasattr(self, name):
                    data[name] = getattr(self, name)
                    if callable(getattr(self, name)):
                        data[name] = data[name](r)
                elif hasattr(r, name):
                    data[name] = getattr(r, name)

                if data.get(name) and type(data[name]) not in (str, unicode):
                    data[name] = unicode(data[name])

            data = dict((k, v.encode('utf-8')) for k, v in data.iteritems() if v)
            writer.writerow(data)
        return response

    def csv_export(self, request, qs=None, *args, **kwargs):
        return self.export_list(request, qs[:self.csv_record_limit])

    csv_export.short_description = \
        'Exported selected %(verbose_name_plural)s as CSV'


class StaffPermissionMixin(object):
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff