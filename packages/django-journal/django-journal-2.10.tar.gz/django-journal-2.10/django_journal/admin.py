from string import Formatter

import django.contrib.admin as admin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import force_text
from django.utils.html import escape, format_html, mark_safe
from django.utils.translation import ugettext_lazy as _

from .actions import export_as_csv
from .models import Journal, ObjectData, StringData, Tag


class ModelAdminFormatter(Formatter):
    def __init__(self, model_admin=None, filter_link=True, object_link=True):
        self.filter_link = filter_link
        self.object_link = object_link
        self.model_admin = model_admin
        super().__init__()

    def build_object_link(self, value):
        content_type = ContentType.objects.get_for_model(value.__class__)
        url = '{}:{}_{}_change'.format(
            self.model_admin.admin_site.name, content_type.app_label, content_type.model
        )
        try:
            url = reverse(url, args=(value.pk,))
        except NoReverseMatch:
            return ''
        return f'<a href="{escape(url)}" class="external-link"></a>'

    def format_field(self, value, format_spec):
        if isinstance(value, models.Model):
            res = ''
            if self.filter_link:
                content_type = ContentType.objects.get_for_model(value.__class__)
                res = '<a href="?objectdata__content_type={}&objectdata__object_id={}">{}</a>'.format(
                    content_type.id, value.pk, escape(force_text(value))
                )
            else:
                res = escape(force_text(value))
            if self.object_link:
                res += self.build_object_link(value)
            return res
        return escape(super().format_field(value, format_spec))


class ObjectDataInlineAdmin(admin.TabularInline):
    model = ObjectData
    fields = ('tag', 'content_type', 'content_object')
    readonly_fields = fields
    extra = 0
    max_num = 0


class StringDataInlineAdmin(admin.TabularInline):
    model = StringData
    fields = ('tag', 'content')
    readonly_fields = fields
    extra = 0
    max_num = 0


class JournalAdmin(admin.ModelAdmin):
    list_display = ('time', '_tag', 'user', 'ip', 'message_for_list')
    list_filter = ('tag',)
    fields = ('time', 'tag', 'user', 'ip', 'message_for_change')
    readonly_fields = fields
    inlines = (
        ObjectDataInlineAdmin,
        StringDataInlineAdmin,
    )
    date_hierarchy = 'time'
    search_fields = ('message', 'tag__name', 'time')
    actions = [export_as_csv]

    class Media:
        css = {
            'all': ('journal/css/journal.css',),
        }

    def queryset(self, request):
        '''Get as much data as possible using the fewest requests possible.'''
        qs = super().queryset(request)
        qs = qs.select_related('tag', 'template').prefetch_related(
            'objectdata_set__content_type',
            'stringdata_set',
            'objectdata_set__tag',
            'stringdata_set__tag',
            'objectdata_set__content_object',
        )
        return qs

    def lookup_allowed(self, key, *args, **kwargs):
        return True

    def _tag(self, entry):
        name = entry.tag.name.replace('-', '\u2011')
        res = format_html('<a href="?tag__id__exact={0}">{1}</a>', escape(entry.tag.id), escape(name))
        return res

    _tag.short_description = _('tag')

    def ip(self, entry):
        '''Search and return any associated stringdata whose tag is "ip"'''
        for stringdata in entry.stringdata_set.all():
            if stringdata.tag.name == 'ip':
                return format_html(
                    '<a href="?stringdata__tag__id={tag_id}&' 'stringdata__content={ip}">{ip}</a>',
                    tag_id=stringdata.tag.id,
                    ip=stringdata.content,
                )
        return _('None')

    ip.short_description = _('IP')

    def user(self, entry):
        '''Search and return any associated objectdata whose tag is "user"'''
        for objectdata in entry.objectdata_set.all():
            if objectdata.tag.name == 'user':
                return format_html(self.object_filter_link(objectdata) + self.object_link(objectdata))
        return _('None')

    user.short_description = _('User')

    def object_filter_link(self, objectdata):
        if objectdata.content_object is not None:
            caption = force_text(objectdata.content_object)
        else:
            caption = _('<deleted {content_type} {object_id}>').format(
                content_type=objectdata.content_type, object_id=objectdata.object_id
            )
        return '<a href="?objectdata__content_type={}&objectdata__object_id={}">{}</a>'.format(
            objectdata.content_type_id, objectdata.object_id, escape(caption)
        )

    def object_link(self, obj_data):
        if obj_data.content_object is None:
            return ''
        url = '{}:{}_{}_change'.format(
            self.admin_site.name, obj_data.content_type.app_label, obj_data.content_type.model
        )
        try:
            url = reverse(url, args=(obj_data.object_id,))
        except NoReverseMatch:
            return ''
        return f'<a href="{url}" class="external-link"></a>'

    def message_for_change(self, entry):
        ctx = entry.message_context()
        formatter = ModelAdminFormatter(model_admin=self, filter_link=False)
        message = formatter.format(escape(entry.template.content), **ctx)
        return format_html('<span>{}</span>', mark_safe(message))

    message_for_change.short_description = _('Message')

    def message_for_list(self, entry):
        ctx = entry.message_context()
        formatter = ModelAdminFormatter(model_admin=self)
        message = formatter.format(entry.template.content, **ctx)
        return format_html('<span>{}</span>', mark_safe(message))

    message_for_list.short_description = _('Message')
    message_for_list.admin_order_field = 'message'


admin.site.register(Journal, JournalAdmin)
admin.site.register(Tag)
