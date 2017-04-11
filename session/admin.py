from django.contrib import admin

# Register your models here.
from django.contrib.admin import DateFieldListFilter

from .models import Session, Call

from django.core import urlresolvers
from django.utils.html import format_html
from base.admin import BaseAdmin

@admin.register(Call)
class CallAdmin(BaseAdmin):
    list_filter = [('start_time', DateFieldListFilter), ('end_time', DateFieldListFilter), 'belong_session', 'belong_session__session_number', 'belong_session__skill_match__skill__topic',
                   'belong_session__skill_match__skill', 'belong_session__skill_match__customer',
                   'belong_session__student', "follow_up"]
    list_display = ['start_time', 'end_time', 'belong_session', "follow_up"]
    search_fields = ['start_time', 'end_time', 'belong_session__skill_match__skill__topic__topic_name',
                     'belong_session__skill_match__skill__skill_name',
                     'belong_session__skill_match__customer__customer_name', 'belong_session__student__customer_name',
                     'belong_session__session_number']

    raw_id_fields = ["belong_session"]
    readonly_fields = ['call_duration']


def reverse_foreignkey_change_links(model, get_instances, description=None, get_link_html=None, empty_text='(None)'):
    if not description:
        description = model.__name__ + '(s)'

    def model_change_link_function(_, obj):
        instances = get_instances(obj)
        if instances.count() == 0:
            return empty_text
        output = ''
        links = []
        for instance in instances:
            change_url = urlresolvers.reverse('admin:%s_change' % model._meta.db_table, args=(instance.id,))
            links.append('<a href="%s">%s</a>' % (change_url, unicode(instance)))
        return format_html('<br> '.join(links))

    model_change_link_function.short_description = description
    model_change_link_function.allow_tags = True
    return model_change_link_function


@admin.register(Session)
class SessionAdmin(BaseAdmin):
    list_filter = ['session_number', 'skill_match__skill__topic', 'skill_match__skill', 'skill_match__customer',
                   'student', "student_pricing", "teacher_pricing", "follow_up"]
    list_display = ['order_id', 'skill_match', 'student', 'session_number', 'amount_to_teacher', 'balance_amount',
                    'start_time', "student_pricing", "teacher_pricing", "follow_up"]
    search_fields = ['order_id', 'skill_match__skill__topic__topic_name', 'skill_match__skill__skill_name',
                     'skill_match__customer__customer_name', 'student__customer_name', 'session_number']

    raw_id_fields = ["skill_match", "student", "student_pricing", "teacher_pricing"]
    readonly_fields = ['order_id', 'session_number', 'total_calls', 'calls_list', 'total_duration', 'minutes_duration',
                       'start_time', 'end_time', 'call_time_range', 'money_refund', 'amount_to_teacher',
                       'amount_from_student', 'balance_amount']

    calls_list = reverse_foreignkey_change_links(Call, lambda obj: Call.objects.filter(belong_session=obj))

# admin.site.register(Session)
# admin.site.register(Call)
