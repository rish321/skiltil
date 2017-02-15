#from __future__ import unicode_literals

#from django.db import models

# Create your models here.
from django.db import models
#from proj.models import Skill
from session.models import Session
from payment.models import Payment, Payout
from django.utils.encoding import python_2_unicode_compatible
from base.models import BaseModel

GENDEROPTIONS = (
	('f', 'Female'),
	('m', 'Male'),
    ('o', 'Other'),
	('d', 'Decline to State'),
)

class Customer(BaseModel):
	customer_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200, blank=True)
	phone_number = models.CharField(max_length=200, blank=True)
	gender = models.CharField(max_length=1, choices=GENDEROPTIONS, default='d')
	image = models.CharField(max_length=200, blank = True)
	skype_id = models.CharField(max_length=200, blank = True)
	gmail_id = models.CharField(max_length=200, blank = True)
	paytm_id = models.CharField(max_length=200, blank = True)
	customer_code = models.CharField(max_length=200, default="")
	no_subjects = models.IntegerField(default=0)
	wallet_amount = models.FloatField(default=0)
	classes_taken = models.IntegerField(default=0)
	classes_given = models.IntegerField(default=0)
	def __str__(self):
                return self.customer_name
	def generate_code(self, customer_name):
		val = BaseModel.findVal(customer_name)
		if Customer.objects.filter(customer_code=val).count() != 0:
			x = 2
			while True:
				val = "{0}{1}".format(val, x)
				if Customer.objects.filter(customer_code=val).count() == 0:
					break
				x += 1
				if x > 10000000:
					raise Exception("Name is super popular!")
		return ''.join(e for e in val if e.isalnum())
	def save(self, *args, **kwargs):
		if len(self.customer_code) == 0:
			self.customer_code = self.generate_code(self.customer_name)
		self.wallet_amount = 0
		sessions = Session.objects.filter(student = self)
		for session in sessions:
			self.wallet_amount -= session.balance_amount
		self.classes_taken = len(sessions)
		self.classes_given = 0
		skillMatches = SkillMatch.objects.filter(customer = self)
		self.no_subjects = len(skillMatches)
		for skillMatch in skillMatches:
			self.classes_given += skillMatch.classes_given
			teacherSessions = Session.objects.filter(skill_match = skillMatch)
			for session in teacherSessions:
	                        self.wallet_amount += session.amount_to_teacher
		payments = Payment.objects.filter(customer = self)
		for payment in payments:
			self.wallet_amount += payment.amount
		payouts = Payout.objects.filter(customer = self)
		for payout in payouts:
			self.wallet_amount -= payout.amount
		super(Customer, self).save(*args, **kwargs)
		
class SkillMatchQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        super(SkillMatchQuerySet, self).delete(*args, **kwargs)


class SkillMatch(BaseModel):
	objects = SkillMatchQuerySet.as_manager()
	skill = models.ForeignKey("proj.Skill", default=None)
	customer = models.ForeignKey(Customer, default=None)
	details = models.TextField(default="", blank = True)
	classes_given = models.IntegerField(default=0)
	def __str__(self):
                return self.skill.skill_name + " - " + self.customer.customer_name
	def save(self, *args, **kwargs):
        	sessions = Session.objects.filter(skill_match = self)
		self.classes_given = len(sessions)
		super(SkillMatch, self).save(*args, **kwargs)
		self.skill.save(*args, **kwargs)
		self.customer.save(*args, **kwargs)
	def delete(self, *args, **kwargs):
		skill = self.skill
		customer = self.customer
		super(SkillMatch, self).delete(*args, **kwargs)
		skill.save(*args, **kwargs)
		customer.save(*args, **kwargs)
