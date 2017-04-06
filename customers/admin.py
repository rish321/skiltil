from django.contrib import admin

# Register your models here.

from .models import SkillMatch, Customer

@admin.register(SkillMatch)
class SkillMatchAdmin(admin.ModelAdmin):
	raw_id_fields = ["skill", "customer"]
	list_filter = ["skill__topic", "skill", "customer", "verified", "visible", "teacher_rating", "teacher_rating_count"]
	list_display = ["skill", "customer", "classes_given", "verified", "visible", "teacher_rating", "teacher_rating_count"]
	search_fields = ["skill__topic__topic_name", "skill__skill_name", "customer__customer_name"]
	readonly_fields = ["classes_given", "teacher_rating", "teacher_rating_count"]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	raw_id_fields = ["social"]
	list_display = ["customer_code", "social", "customer_name", "email", "skype_id", "gmail_id", "paytm_id", "phone_number", "no_subjects", "wallet_amount", "classes_taken", "classes_given", "student_rating", "student_rating_count", "teacher_rating", "teacher_rating_count"]
	search_fields = ["customer_code", "customer_name", "email", "skype_id", "gmail_id", "paytm_id", "phone_number"]
	readonly_fields = ["customer_code", "social", "no_subjects", "wallet_amount", "classes_taken", "classes_given", "student_rating", "student_rating_count", "teacher_rating", "teacher_rating_count"]
	list_filter = ["student_rating", "student_rating_count", "teacher_rating", "teacher_rating_count"]

#admin.site.register(SkillMatch)
#admin.site.register(Customer)
