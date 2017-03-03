from __future__ import unicode_literals

from django.db import models

from base.models import BaseModel
from datetime import timedelta

# Create your models here.

class PriceModelQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        super(PriceModelQuerySet, self).delete(*args, **kwargs)

class PriceModel(BaseModel):
    objects = PriceModelQuerySet.as_manager()
    name = models.CharField(default="", max_length=50)
    fixed_price = models.IntegerField(default=0)
    fixed_price_time_end = models.DurationField(default=timedelta)
    red_cost_factor = models.FloatField(default=0)
    red_cost_time_end = models.DurationField(default=timedelta)
    cost_factor = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def calculateAmount(self, timeDuration, seconds=True):
        if seconds:
            timeSeconds = timeDuration.total_seconds()
            return (self.cost_factor * timeSeconds) / 60
        else:
            timeSeconds = timeDuration.total_seconds()
            minutes = timeSeconds / 60
            timeSeconds = timeSeconds % 60
            if timeSeconds > 0:
                minutes += 1
            fixedCost = 0
            redCost = 0
            noRedCost = 0
            if minutes > 0:
                fixedCost = self.fixed_price
                if self.red_cost_factor > 0 or self.cost_factor > 0:
                    minutes -= self.fixed_price_time_end.total_seconds()/60 #.getminutes
                    if minutes > 0:
                        redCost = int(minutes) * self.red_cost_factor
                        if self.cost_factor > 0:
                            minutes -= self.red_cost_time_end.total_seconds()/60 #.getminutes
                            if minutes > 0:
                                noRedCost = int(minutes) * (self.cost_factor - self.red_cost_factor)
            cost = fixedCost + redCost + noRedCost
            return cost