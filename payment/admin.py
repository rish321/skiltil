from django.contrib import admin

# Register your models here.
from .models import Payment, Payout

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	raw_id_fields = ["customer"]
	list_filter = ["customer"]
	list_display = ["customer", "amount", "time"]
	search_fields = ["customer__customer_name"]

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
	raw_id_fields = ["customer"]
	list_filter = ["customer"]
	list_display = ["customer", "amount", "time"]
	search_fields = ["customer__customer_name"]


#admin.site.register(Payment)
#admin.site.register(Payout)
