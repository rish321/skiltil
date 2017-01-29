from django.contrib import admin

# Register your models here.

from .models import Session, Call


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_filter = ['belong_session', 'belong_session__session_number', 'belong_session__skill_match__skill__topic',
                   'belong_session__skill_match__skill', 'belong_session__skill_match__customer',
                   'belong_session__student']
    list_display = ['start_time', 'end_time', 'belong_session']
    search_fields = ['start_time', 'end_time', 'belong_session__skill_match__skill__topic__topic_name',
                     'belong_session__skill_match__skill__skill_name',
                     'belong_session__skill_match__customer__customer_name', 'belong_session__student__customer_name',
                     'belong_session__session_number']

    raw_id_fields = ["belong_session"]
    readonly_fields = ['call_duration']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_filter = ['session_number', 'skill_match__skill__topic', 'skill_match__skill', 'skill_match__customer',
                   'student']
    list_display = ['order_id', 'skill_match', 'student', 'session_number', 'amount_to_teacher', 'balance_amount',
                    'start_time', ]
    search_fields = ['order_id', 'skill_match__skill__topic__topic_name', 'skill_match__skill__skill_name',
                     'skill_match__customer__customer_name', 'student__customer_name', 'session_number']

    raw_id_fields = ["skill_match", "student"]
    readonly_fields = ['order_id', 'session_number', 'total_calls', 'total_duration', 'minutes_duration', 'start_time',
                       'end_time',
                       'call_time_range', 'money_refund', 'amount_to_teacher', 'amount_from_student', 'balance_amount']

# admin.site.register(Session)
# admin.site.register(Call)
