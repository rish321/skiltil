from django.contrib import admin

from .models import SkillTopic, Skill, CustomerRequest

# Register your models here.
admin.site.register(SkillTopic)
admin.site.register(Skill)
admin.site.register(CustomerRequest)
