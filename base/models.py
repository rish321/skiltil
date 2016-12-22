from __future__ import unicode_literals

from django.db import models

# Create your models here.

class BaseModel(models.Model):
        created_date = models.DateTimeField(auto_now_add=True)
        modified_date = models.DateTimeField(auto_now=True)

        class Meta:
                abstract = True
