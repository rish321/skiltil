from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives
from django.db import models
# from customers.models import Customer
from django.template.loader import render_to_string
from django.utils import timezone
from base.models import BaseModel


# Create your models here.

PAYMENTMODECHOICES = (
    ("paytm", "Paytm"),
    ("account", "Account Transfer"),
    ("cash", "Cash"),
    ("other", "Others"),
    ("skiltil-transfer", "Skiltil Internal Transfer"),
)

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
    mode = models.CharField(max_length=20, choices=PAYMENTMODECHOICES, default="paytm")
    transaction_id = models.CharField(max_length=50, default="", blank=True)
    def __str__(self):
        return self.customer.customer_name + " - " + str(self.amount) + " - " + str(self.time)

    def save(self, *args, **kwargs):
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
    mode = models.CharField(max_length=20, choices=PAYMENTMODECHOICES, default="paytm")
    transaction_id = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return self.customer.customer_name + " - " + str(self.amount) + " - " + str(self.time)

    def save(self, *args, **kwargs):
        super(Payout, self).save(*args, **kwargs)
        self.customer.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        customer = self.customer
        super(Payout, self).delete(*args, **kwargs)
        customer.save(*args, **kwargs)


class TransferQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        super(TransferQuerySet, self).delete(*args, **kwargs)


class Transfer(BaseModel):
    objects = TransferQuerySet.as_manager()
    customer = models.ForeignKey("customers.Customer", related_name="paying_customer", default=None)
    amount = models.FloatField(default=0)
    customer_to_transfer = models.ForeignKey("customers.Customer", related_name="customer_to_transfer", default=None)
    time = models.DateTimeField(default=timezone.now)
    mode = "Skiltil Transfer"
    transaction_id = models.CharField(max_length=50, default="", blank=True)

    def generateTransactionId(self):
        skilTransVal="SkilTrans"
        x = 1
        val = "{0}{1}".format(skilTransVal, x)
        if Transfer.objects.filter(transaction_id=val).count() != 0:
            while True:
                x += 1
                val = "{0}{1}".format(skilTransVal, x)
                if Transfer.objects.filter(transaction_id=val).count() == 0:
                    break
        return ''.join(e for e in val if e.isalnum())


    def __str__(self):
        return self.customer.customer_name + " - " + str(self.amount) + " - " + self.customer_to_transfer.customer_name + " - " + str(self.time)

    def save(self, *args, **kwargs):
        self.transaction_id = self.generateTransactionId()
        super(Transfer, self).save(*args, **kwargs)
        self.customer.save(*args, **kwargs)
        self.customer_to_transfer.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        customer = self.customer
        super(Transfer, self).delete(*args, **kwargs)
        customer.save(*args, **kwargs)