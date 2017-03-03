from django.contrib import admin

from .models import PriceModel
# Register your models here.

@admin.register(PriceModel)
class PriceModelAdmin(admin.ModelAdmin):
	list_display = ['name', 'fixed_price', 'fixed_price_time_end', 'red_cost_factor', 'red_cost_time_end', 'cost_factor']
	search_fields = ['name']