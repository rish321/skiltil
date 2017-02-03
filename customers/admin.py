from django.contrib import admin

# Register your models here.

from .models import SkillMatch, Customer

@admin.register(SkillMatch)
class SkillMatchAdmin(admin.ModelAdmin):
	raw_id_fields = ["skill", "customer"]
	list_filter = ["skill__topic", "skill", "customer"]
	list_display = ["skill", "customer", "classes_given"]
	search_fields = ["skill__topic__topic_name", "skill__skill_name", "customer__customer_name"]
	readonly_fields = ["classes_given"]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ["user_name", "customer_name", "skype_id", "gmail_id", "paytm_id", "phone_number", "no_subjects", "wallet_amount", "classes_taken", "classes_given"]
	search_fields = ["user_name", "customer_name", "skype_id", "gmail_id", "paytm_id", "phone_number"]
	readonly_fields = ["user_name", "no_subjects", "wallet_amount", "classes_taken", "classes_given"]

#admin.site.register(SkillMatch)
#admin.site.register(Customer)
