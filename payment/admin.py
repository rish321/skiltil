from django.contrib import admin

# Register your models here.
from customers.models import Customer
from .models import Payment, Payout, Transfer

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

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
	raw_id_fields = ["customer", "customer_to_transfer"]
	list_filter = ["customer", "customer_to_transfer"]
	list_display = ["transaction_id", "customer", "amount", "customer_to_transfer", "time"]
	search_fields = ["customer__customer_name", "customer_to_transfer__customer_name"]
	readonly_fields = ["transaction_id"]

	#existing_amount = getExistingAmount(lambda obj: obj.customer.wallet_amount)


#admin.site.register(Payment)
#admin.site.register(Payout)
