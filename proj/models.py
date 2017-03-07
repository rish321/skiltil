# from __future__ import unicode_literals

# from django.db import models

# Create your models here.
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from customers.models import SkillMatch
from base.models import BaseModel

from django.utils import timezone
from tinymce import models as tinymce_models
import math
from HTMLParser import HTMLParser


# class BaseModel(models.Model):
#	created_date = models.DateTimeField(auto_now_add=True)
#	modified_date = models.DateTimeField(auto_now=True)
#
#	class Meta:
#        	abstract = True

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


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
    topic_code = models.CharField(max_length=200, default="")
    clicks = models.IntegerField(default=0)
    classes_given = models.IntegerField(default=0)

    def __str__(self):
        return self.topic_name

    def generate_code(self, topic_name):
        val = BaseModel.findVal(topic_name)
        if SkillTopic.objects.filter(topic_code=val).count() != 0:
            x = 2
            while True:
                val = "{0}{1}".format(val, x)
                if SkillTopic.objects.filter(topic_code=val).count() == 0:
                    break
                x += 1
                if x > 10000000:
                    raise Exception("Name is super popular!")
        return ''.join(e for e in val if e.isalnum())

    def save(self, *args, **kwargs):
        skills = Skill.objects.filter(topic=self)
        if len(self.topic_code) == 0:
            self.topic_code = self.generate_code(self.topic_name)
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
    image_src = models.CharField(max_length=200, blank=True)
    details = tinymce_models.HTMLField(default="", blank=True)
    course_structure = tinymce_models.HTMLField(default="", blank=True)
    pre_requisites = tinymce_models.HTMLField(default="", blank=True)
    exclusive = models.BooleanField(default=False)
    total_classes = models.IntegerField(default=1)
    first_class_time = models.DurationField(default=timezone.timedelta(minutes = 30), blank=True)
    subsequent_class_time = models.DurationField(default=timezone.timedelta, blank=True)
    skill_code = models.CharField(max_length=200, default="")
    clicks = models.IntegerField(default=0)
    classes_given = models.IntegerField(default=0)
    no_teachers = models.IntegerField(default=0)
    skill_rating = models.FloatField(default=0)
    skill_rating_count = models.IntegerField(default=0)
    student_pricing = models.ForeignKey("pricing.PriceModel", default=None, null=True, blank=True,
                                        related_name='skill_student_pricing')
    teacher_pricing = models.ForeignKey("pricing.PriceModel", default=None, null=True, blank=True,
                                        related_name='skill_teacher_pricing')

    def __str__(self):
        return self.skill_name + " - " + self.topic.topic_name

    def get_skill_rating(self):
        return math.ceil(self.skill_rating / 2 * 10.0) / 10

    def get_plain_text(self):
        return strip_tags(self.details)

    def add_skill_rating(self, skill_rating):
        existingRating = self.skill_rating * self.skill_rating_count
        existingRating += skill_rating
        self.skill_rating_count += 1
        self.skill_rating = existingRating / self.skill_rating_count
        self.save()

    def update_teacher_rating(self, old_skill_rating, skill_rating):
        existingRating = self.skill_rating * self.skill_rating_count
        existingRating += (skill_rating - old_skill_rating)
        self.skill_rating = existingRating / self.skill_rating_count
        self.save()

    def generate_code(self, skill_name):
        val = BaseModel.findVal(skill_name)
        if Skill.objects.filter(skill_code=val).count() != 0:
            x = 2
            while True:
                val = "{0}{1}".format(val, x)
                if Skill.objects.filter(skill_code=val).count() == 0:
                    break
                x += 1
                if x > 10000000:
                    raise Exception("Name is super popular!")
        return ''.join(e for e in val if e.isalnum())

    def remaining_classes(self):
        return self.total_classes - 1

    def first_session_time(self):
        return str(int(self.first_class_time.total_seconds() / 60)) + " minutes"

    def first_class_cost(self):
        return int(self.student_pricing.calculateAmount(self.first_class_time, False))

    def first_class_cost_range(self):
        return str(int(self.student_pricing.calculateAmount(self.first_class_time, False))) + " - " + str(int(self.student_pricing.calculateAmount(self.first_class_time + timezone.timedelta(minutes = 10), False)))

    def subsequent_session_time(self):
        return str(int(self.subsequent_class_time.total_seconds() / 60)) + " minutes"

    def discounted_price(self):
        return int(math.ceil((self.first_class_cost() + (self.total_classes - 1) * self.subsequent_class_cost()) * 0.9))

    def subsequent_class_cost(self):
        return int(self.student_pricing.calculateAmount(self.subsequent_class_time, False))

    def subsequent_class_cost_range(self):
        return str(int(self.student_pricing.calculateAmount(self.subsequent_class_time, False))) + " - " + str(int(self.student_pricing.calculateAmount(self.subsequent_class_time + timezone.timedelta(minutes = 10), False)))

    def classes_single_column(self):
        return self.total_classes == 1 and self.first_class_time.total_seconds() > 0

    def first_class_show(self):
        return self.first_class_time.total_seconds() > 0

    def save(self, *args, **kwargs):
        if len(self.skill_code) == 0:
            self.skill_code = self.generate_code(self.skill_name)
        self.classes_given = 0
        skillMatches = SkillMatch.objects.filter(skill=self)
        self.no_teachers = len(skillMatches)
        self.skill_rating = 0
        self.skill_rating_count = 0
        for skillMatch in skillMatches:
            self.classes_given += skillMatch.classes_given
            self.skill_rating += skillMatch.teacher_rating * skillMatch.teacher_rating_count
            self.skill_rating_count += skillMatch.teacher_rating_count
        if self.skill_rating_count > 0:
            self.skill_rating /= self.skill_rating_count
        super(Skill, self).save(*args, **kwargs)
        self.topic.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        topic = self.topic
        super(Skill, self).delete(*args, **kwargs)
        topic.save(*args, **kwargs)
