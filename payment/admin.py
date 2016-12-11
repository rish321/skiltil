from django.contrib import admin

# Register your models here.
from .models import Payment, Payout

admin.site.register(Payment)
admin.site.register(Payout)
