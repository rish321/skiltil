#from __future__ import unicode_literals

#from django.db import models

# Create your models here.
from django.db import models
from proj.models import Skill
from django.utils.encoding import python_2_unicode_compatible

class Customer(models.Model):
	customer_name = models.CharField(max_length=200)
	skype_id = models.CharField(max_length=200, blank = True)
	gmail_id = models.CharField(max_length=200, blank = True)
	paytm_id = models.CharField(max_length=200, blank = True)
	wallet_amount = models.FloatField(default=0)
	classes_taken = models.IntegerField(default=0)
	classes_given = models.IntegerField(default=0)
	def __str__(self):
                return self.customer_name

class SkillMatch(models.Model):
	skill = models.ForeignKey(Skill, default=None)
	customer = models.ForeignKey(Customer, default=None)
	classes_given = models.IntegerField(default=0)
	def __str__(self):
                return self.skill.skill_name + " - " + self.customer.customer_name
	def save(self, *args, **kwargs):
                self.skill.no_teachers += 1
                super(Skill, self.skill).save(*args, **kwargs)
                super(SkillMatch, self).save(*args, **kwargs)
