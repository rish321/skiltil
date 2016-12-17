#from __future__ import unicode_literals

#from django.db import models

# Create your models here.
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from customers.models import SkillMatch

class SkillTopic(models.Model):
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

class Skill(models.Model):
	objects = SkillQuerySet.as_manager()
	skill_name = models.CharField(max_length=200)
	topic = models.ForeignKey(SkillTopic, default=None)
	image_src = models.CharField(max_length=200)
	details = models.TextField(default="")
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
