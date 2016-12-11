from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from proj.models import Skill
from proj.models import SkillTopic
from customers.models import SkillMatch
from customers.models import Customer
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import python_2_unicode_compatible
from datetime import timedelta
from datetime import datetime
from operator import attrgetter
from django.utils import timezone
#from djangotoolbox.fields import ListField

CALLOPTIONS = (
    (0, 'OnGoing'),
    (1, 'Finished'),
    (2, 'Unfinished'),
)


class Session(models.Model):
	skill_match = models.ForeignKey(SkillMatch, default=None)
	student = models.ForeignKey(Customer, default=None)
	status = models.IntegerField(choices=CALLOPTIONS)
	time_refund = models.DurationField(default=timedelta)
	follow_up = models.BooleanField()
	total_calls = models.IntegerField(default=0)
	total_duration = models.DurationField(default=timedelta)
	minutes_duration = models.IntegerField(default=0)
	start_time = models.DateTimeField(default=timezone.now)
	end_time = models.DateTimeField(default=timezone.now().replace(year=1970, month=1, day=1, hour=0, minute=0, second=0))
	call_time_range = models.DurationField(default=timedelta)
	money_refund = models.FloatField(default=0)
	amount_to_teacher = models.FloatField(default=0)
	amount_from_student = models.FloatField(default=0)
	balance_amount = models.FloatField(default=0)
	def __str__(self):
                return self.skill_match.skill.skill_name + " - " + self.skill_match.customer.customer_name + " - " + self.student.customer_name
	def save(self, *args, **kwargs):
		self.skill_match.classes_given += 1
		self.skill_match.customer.classes_given += 1
		self.student.classes_taken += 1
		self.skill_match.skill.classes_given += 1
		self.skill_match.skill.topic.classes_given += 1
		super(Skill, self.skill_match.skill).save(*args, **kwargs)
		super(SkillTopic, self.skill_match.skill.topic).save(*args, **kwargs)
		super(SkillMatch, self.skill_match).save(*args, **kwargs)
		super(Customer, self.skill_match.customer).save(*args, **kwargs)
		super(Customer, self.student).save(*args, **kwargs)
                super(Session, self).save(*args, **kwargs)

def calculateTeacherAmount(timeDuration):
	timeSeconds = timeDuration.total_seconds()
	return (2.5*timeSeconds)/60


def calculateStudentAmount(timeDuration):
	seconds = timeDuration.total_seconds()
	minutes = seconds/60
	seconds = seconds%60
	if seconds > 0:
		minutes += 1
	roundedTimeDuration = minutes
	#print minutes
	cost = 0
	fixedCost = 0
	redCost = 0
	noRedCost = 0
	multiplicationFactor = 2
	if minutes > 0:
		fixedCost = multiplicationFactor
		minutes -= 5
		if minutes > 0:
			redCost = int(minutes) * multiplicationFactor
			minutes -= 5
			if minutes > 0:
				noRedCost = int(minutes) * multiplicationFactor
	cost = fixedCost + redCost + noRedCost
	return cost, roundedTimeDuration

class Call(models.Model):
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	belong_session = models.ForeignKey(Session, default=None)
	status = models.IntegerField(choices=CALLOPTIONS)
	follow_up = models.BooleanField()
	call_duration = models.DurationField(default = timedelta)
	#firstEntry = True;
	def __str__(self):
		#return "inserted"
               	return str(self.start_time) + " - " + str(self.end_time)
	def save(self, *args, **kwargs):
	        self.call_duration = self.end_time - self.start_time
		self.belong_session.start_time = min(self.start_time, self.belong_session.start_time)
		self.belong_session.end_time = max(self.end_time, self.belong_session.end_time)
		self.belong_session.call_time_range = self.belong_session.end_time - self.belong_session.start_time
		if self.follow_up == False:
			calls = Call.objects.filter(belong_session = self.belong_session)	
			self.belong_session.total_duration = timedelta()
			self.belong_session.total_duration = self.call_duration
			self.belong_session.total_calls = 1
			for call in calls:
				self.belong_session.total_duration += call.call_duration
				self.belong_session.total_calls += 1
			self.belong_session.amount_to_teacher = calculateTeacherAmount(self.belong_session.total_duration)
			x, self.belong_session.money_refund = calculateStudentAmount(self.belong_session.time_refund)
			self.belong_session.amount_from_student, self.belong_session.minutes_duration = calculateStudentAmount(self.belong_session.total_duration)
			self.belong_session.balance_amount = self.belong_session.amount_from_student - self.belong_session.money_refund
			self.belong_session.skill_match.customer.wallet_amount += self.belong_session.amount_to_teacher
			self.belong_session.student.wallet_amount -= self.belong_session.balance_amount
		super(Customer, self.belong_session.skill_match.customer).save(*args, **kwargs)
                super(Customer, self.belong_session.student).save(*args, **kwargs)
		super(Session, self.belong_session).save(*args, **kwargs)
        	super(Call, self).save(*args, **kwargs)
