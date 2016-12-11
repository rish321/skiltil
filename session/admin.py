from django.contrib import admin

# Register your models here.

from .models import Session, Call

admin.site.register(Session)
admin.site.register(Call)
