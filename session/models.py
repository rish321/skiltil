from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
#from proj.models import Skill
#from proj.models import SkillTopic
#from customers.models import SkillMatch
#from customers.models import Customer
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

class SessionQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        super(SessionQuerySet, self).delete(*args, **kwargs)

class Session(models.Model):
	objects = SessionQuerySet.as_manager()
	skill_match = models.ForeignKey("customers.SkillMatch", default=None)
	student = models.ForeignKey("customers.Customer", default=None)
	status = models.IntegerField(choices=CALLOPTIONS)
	time_refund = models.DurationField(default=timedelta)
	follow_up = models.BooleanField()
	total_calls = models.IntegerField(default=0)
	total_duration = models.DurationField(default=timedelta)
	minutes_duration = models.IntegerField(default=0)
	start_time = models.DateTimeField(default=timezone.now)
	end_time = models.DateTimeField(default=timezone.now)
	call_time_range = models.DurationField(default=timedelta)
	money_refund = models.FloatField(default=0)
	amount_to_teacher = models.FloatField(default=0)
	amount_from_student = models.FloatField(default=0)
	balance_amount = models.FloatField(default=0)
	def __str__(self):
                return self.skill_match.skill.skill_name + " - " + self.skill_match.customer.customer_name + " - " + self.student.customer_name

	def calculateTeacherAmount(self, timeDuration):
		timeSeconds = timeDuration.total_seconds()
		return (2.5*timeSeconds)/60

	def calculateStudentAmount(self, timeDuration):
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
		self.minutes_duration = roundedTimeDuration
		return cost

	def save(self, *args, **kwargs):
		calls = Call.objects.filter(belong_session = self)	
		self.total_duration = timedelta()
		self.total_calls = 0
		self.start_time = timezone.now()
		self.end_time = timezone.now().replace(year=1970, month=1, day=1, hour=0, minute=0, second=0)
		for call in calls:
			self.start_time = min(call.start_time, self.start_time)
			self.end_time = max(call.end_time, self.end_time)
			self.total_duration += call.call_duration
			self.total_calls += 1
		self.call_time_range = self.end_time - self.start_time
		self.amount_to_teacher = self.calculateTeacherAmount(self.total_duration)
		self.money_refund = self.calculateStudentAmount(self.time_refund)
		self.amount_from_student = self.calculateStudentAmount(self.total_duration)
		self.balance_amount = self.amount_from_student - self.money_refund
		super(Session, self).save(*args, **kwargs)
		self.skill_match.save(*args, **kwargs)
		self.student.save(*args, **kwargs)
	def delete(self, *args, **kwargs):
		skillMatch = self.skill_match
		student = self.student
		super(Session, self).delete(*args, **kwargs)
		skillMatch.save(*args, **kwargs)
		student.save(*args, **kwargs)

class CallQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        super(CallQuerySet, self).delete(*args, **kwargs)

class Call(models.Model):
	objects = CallQuerySet.as_manager()
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
		super(Call, self).save(*args, **kwargs)
		self.belong_session.save(*args, **kwargs)
	def delete(self, *args, **kwargs):
		belongSession = self.belong_session
		super(Call, self).delete(*args, **kwargs)
		belongSession.save(*args, **kwargs)
