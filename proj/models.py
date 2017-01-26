#from __future__ import unicode_literals

#from django.db import models

# Create your models here.
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from customers.models import SkillMatch
from base.models import BaseModel

from django.utils import timezone

#class BaseModel(models.Model):
#	created_date = models.DateTimeField(auto_now_add=True)
#	modified_date = models.DateTimeField(auto_now=True)
#
#	class Meta:
#        	abstract = True

class CustomerRequest(BaseModel):
	contact_name = models.CharField(max_length=50, blank=False)
	contact_phone = models.CharField(max_length=50, blank=False)
	contact_email = models.CharField(max_length=50, blank=True)
	default_skill = models.CharField(max_length=50, blank=True)
	skill = models.CharField(max_length=200, blank=True)
	preferred_communication_time = models.CharField(max_length=50, blank=True)
	content = models.TextField(blank=True)

	def __str__(self):
        	return self.contact_name + " - " + self.contact_phone + " - " + self.contact_email + " - " + self.default_skill + " - " + self.skill




class SkillTopic(BaseModel):
	topic_name = models.CharField(max_length=200)
	clicks = models.IntegerField(default=0)
	classes_given = models.IntegerField(default=0)
	def __str__(self):
	        return self.topic_name
	def save(self, *args, **kwargs):
		skills = Skill.objects.filter(topic = self)
		self.clicks = 0
		self.classes_given = 0
		for skill in skills:
			self.clicks += skill.clicks
			self.classes_given += skill.classes_given
		super(SkillTopic, self).save(*args, **kwargs)
		

class SkillQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
		obj.delete(*args, **kwargs)
        super(SkillQuerySet, self).delete(*args, **kwargs)

class Skill(BaseModel):
	objects = SkillQuerySet.as_manager()
	skill_name = models.CharField(max_length=200)
	topic = models.ForeignKey(SkillTopic, default=None)
	image_src = models.CharField(max_length=200, blank = True)
	details = models.TextField(default="", blank = True)
	clicks = models.IntegerField(default=0)
	classes_given = models.IntegerField(default=0)
	no_teachers = models.IntegerField(default=0)
	def __str__(self):
        	return self.skill_name + " - " + self.topic.topic_name
	def save(self, *args, **kwargs):
		self.classes_given = 0
		skillMatches = SkillMatch.objects.filter(skill = self)
		self.no_teachers = len(skillMatches)
		for skillMatch in skillMatches:
			self.classes_given += skillMatch.classes_given
		super(Skill, self).save(*args, **kwargs)
		self.topic.save(*args, **kwargs)
	def delete(self, *args, **kwargs):
		topic = self.topic
		super(Skill, self).delete(*args, **kwargs)
		topic.save(*args, **kwargs)
