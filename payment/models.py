from __future__ import unicode_literals

from django.db import models
#from customers.models import Customer
from django.utils import timezone
from base.models import BaseModel

# Create your models here.

class PaymentQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        super(PaymentQuerySet, self).delete(*args, **kwargs)


class Payment(BaseModel):
	objects = PaymentQuerySet.as_manager()
        customer = models.ForeignKey("customers.Customer", default=None)
        amount = models.FloatField(default=0)
        time = models.DateTimeField(default=timezone.now)
        def __str__(self):
                return self.customer.customer_name + " - " + str(self.amount) + " - " + str(self.time)
	def save(self, *args, **kwargs):
                #self.customer.wallet_amount += self.amount
                #super(Customer, self.customer).save(*args, **kwargs)
                super(Payment, self).save(*args, **kwargs)
		self.customer.save(*args, **kwargs)
	def delete(self, *args, **kwargs):
		customer = self.customer
		super(Payment, self).delete(*args, **kwargs)
		customer.save(*args, **kwargs)

class PayoutQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        super(PayoutQuerySet, self).delete(*args, **kwargs)


class Payout(BaseModel):
	objects = PayoutQuerySet.as_manager()
        customer = models.ForeignKey("customers.Customer", default=None)
        amount = models.FloatField(default=0)
        time = models.DateTimeField(default=timezone.now)
        def __str__(self):
                return self.customer.customer_name + " - " + str(self.amount) + " - " + str(self.time)
	def save(self, *args, **kwargs):
                #self.customer.wallet_amount -= self.amount
                #super(Customer, self.customer).save(*args, **kwargs)
                super(Payout, self).save(*args, **kwargs)
		self.customer.save(*args, **kwargs)
	def delete(self, *args, **kwargs):
		customer = self.customer
		super(Payout, self).delete(*args, **kwargs)
		customer.save(*args, **kwargs)
