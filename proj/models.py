#from __future__ import unicode_literals

#from django.db import models

# Create your models here.
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class SkillTopic(models.Model):
	topic_name = models.CharField(max_length=200)
	def __str__(self):
	        return self.topic_name

class Skill(models.Model):
	skill_name = models.CharField(max_length=200)
	topic = models.ForeignKey(SkillTopic, default=None)
	image_src = models.CharField(max_length=200)
	details = models.TextField(default="")
	clicks = models.IntegerField(default=0)
	def __str__(self):
        	return self.skill_name + " - " + self.topic.topic_name
