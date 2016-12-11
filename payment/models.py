from __future__ import unicode_literals

from django.db import models
from customers.models import Customer
from django.utils import timezone

# Create your models here.

class Payment(models.Model):
        customer = models.ForeignKey(Customer, default=None)
        amount = models.FloatField(default=0)
        time = models.DateTimeField(default=timezone.now)
        def __str__(self):
                return self.customer.customer_name + " - " + str(self.amount) + " - " + str(self.time)
	def save(self, *args, **kwargs):
                self.customer.wallet_amount += self.amount
                super(Customer, self.customer).save(*args, **kwargs)
                super(Payment, self).save(*args, **kwargs)


class Payout(models.Model):
        customer = models.ForeignKey(Customer, default=None)
        amount = models.FloatField(default=0)
        time = models.DateTimeField(default=timezone.now)
        def __str__(self):
                return self.customer.customer_name + " - " + str(self.amount) + " - " + str(self.time)
	def save(self, *args, **kwargs):
                self.customer.wallet_amount -= self.amount
                super(Customer, self.customer).save(*args, **kwargs)
                super(Payout, self).save(*args, **kwargs)
