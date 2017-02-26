from django.contrib import admin

from .models import SkillTopic, Skill, CustomerRequest

# Register your models here.

@admin.register(SkillTopic)
class SkillTopicAdmin(admin.ModelAdmin):
	list_display = ['topic_code', 'topic_name', 'clicks', 'classes_given']
	search_fields = ['topic_code', 'topic_name']
	readonly_fields = ['topic_code', 'clicks', 'classes_given']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
	raw_id_fields = ["topic"]
	list_filter = ["no_teachers", "topic", "exclusive"]
	list_display = ['skill_code', "skill_name", "topic", "clicks", "classes_given", "no_teachers", "exclusive"]
	search_fields = ['skill_code', "skill_name", "topic__topic_name"]
	readonly_fields = ['skill_code', 'clicks', 'classes_given', 'no_teachers']

#admin.site.register(SkillTopic)
#admin.site.register(Skill)
admin.site.register(CustomerRequest)
