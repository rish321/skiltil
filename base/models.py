from __future__ import unicode_literals

from django.db import models


# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @staticmethod
    def findVal(name):
        splits = name.split()
        first_name = ""
        last_name = ""
        if len(splits) > 0:
            first_name = splits[0]
        if len(splits) > 1:
            last_name = splits[1]
        val = "{0}{1}".format(first_name, last_name).lower()
        return val
