from django.contrib import admin

# Register your models here.

from .models import SkillMatch, Customer

admin.site.register(SkillMatch)

#@admin.register(Customer)
#class CustomerAdmin(admin.CustomerAdmin):
#	model = Customer
#	list_display = ['customer_name', 'skype_id', 'gmail_id', 'wallet_amount']
#        search_fields = ['customer_name']
#	#pass
admin.site.register(Customer)
