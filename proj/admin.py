from django.contrib import admin

from .models import SkillTopic, Skill, CustomerRequest
from base.admin import BaseAdmin

# Register your models here.

#admin.site.register(Event)

@admin.register(SkillTopic)
class SkillTopicAdmin(BaseAdmin):
	raw_id_fields = ["parent_topic",]
	list_display = ['topic_code', 'topic_name', 'clicks', 'classes_given', "parent_topic",]
	list_filter = ["parent_topic",]
	search_fields = ['topic_code', 'topic_name', "parent_topic__topic_code", "parent_topic__topic_name"]
	readonly_fields = ['topic_code', 'clicks', 'classes_given']

@admin.register(Skill)
class SkillAdmin(BaseAdmin):
	raw_id_fields = ["topic", "student_pricing", "teacher_pricing",]
	list_filter = ["no_teachers", "topic", "exclusive", "visible", 'skill_rating_count', "student_pricing", "teacher_pricing"]
	list_display = ['skill_code', "skill_name", "topic", "clicks", "classes_given", "no_teachers", "exclusive", "visible", 'get_skill_rating', 'skill_rating_count', "student_pricing", "teacher_pricing"]
	search_fields = ['skill_code', "skill_name", "topic__topic_name"]
	readonly_fields = ['skill_code', 'clicks', 'classes_given', 'no_teachers', 'skill_rating', 'skill_rating_count']

#admin.site.register(SkillTopic)
#admin.site.register(Skill)
#admin.site.register(CustomerRequest)
@admin.register(CustomerRequest)
class CustomerRequestAdmin(BaseAdmin):
	list_filter = ["default_skill", "skill",]
	list_display = ['contact_name', "contact_phone", "contact_email", "default_skill", "skill", "preferred_communication_time",]
	search_fields = ['contact_name', "contact_phone", "contact_email", "default_skill", "skill",]
	readonly_fields = ['contact_name', "contact_phone", "contact_email", "default_skill", "skill", "preferred_communication_time", "content"]
