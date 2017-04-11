from django.contrib import admin

# Register your models here.
from django.contrib.admin import DateFieldListFilter

from customers.models import Customer
from .models import Payment, Payout, Transfer
from base.admin import BaseAdmin

@admin.register(Payment)
class PaymentAdmin(BaseAdmin):
	raw_id_fields = ["customer"]
	list_filter = [("time", DateFieldListFilter), "customer", "mode"]
	list_display = ["customer", "amount", "time", "mode", "transaction_id"]
	search_fields = ["customer__customer_name"]

@admin.register(Payout)
class PayoutAdmin(BaseAdmin):
	raw_id_fields = ["customer"]
	list_filter = [("time", DateFieldListFilter), "customer", "mode"]
	list_display = ["customer", "amount", "time", "mode", "transaction_id"]
	search_fields = ["customer__customer_name"]

@admin.register(Transfer)
class TransferAdmin(BaseAdmin):
	raw_id_fields = ["customer", "customer_to_transfer"]
	list_filter = [("time", DateFieldListFilter), "customer", "customer_to_transfer"]
	list_display = ["transaction_id", "customer", "amount", "customer_to_transfer", "transaction_id", "time"]
	search_fields = ["customer__customer_name", "customer_to_transfer__customer_name"]
	readonly_fields = ["transaction_id"]

	#existing_amount = getExistingAmount(lambda obj: obj.customer.wallet_amount)


#admin.site.register(Payment)
#admin.site.register(Payout)
