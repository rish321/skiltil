from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
# from proj.models import Skill
# from proj.models import SkillTopic
# from customers.models import SkillMatch
# from customers.models import Customer
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import python_2_unicode_compatible
from datetime import timedelta
from datetime import datetime
from operator import attrgetter
from django.utils import timezone
from base.models import BaseModel
#from base.fields import SeparatedValuesField
from django.contrib.postgres.fields import JSONField

# from proj.models import BaseModel
# from djangotoolbox.fields import ListField

CALLOPTIONS = (
    (0, 'OnGoing'),
    (1, 'Finished'),
    (2, 'Unfinished'),
    (3, 'Scheduled'),
)

RATINGOPTIONS = (
    (-1, -1),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


class SessionQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        super(SessionQuerySet, self).delete(*args, **kwargs)


class Session(BaseModel):
    objects = SessionQuerySet.as_manager()
    order_id = models.CharField(max_length=20, default="")
    skill_match = models.ForeignKey("customers.SkillMatch", default=None)
    student = models.ForeignKey("customers.Customer", default=None)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    rescheduled_time = models.DateTimeField(null=True, blank=True)
    estimate_duration = models.DurationField(default=timedelta)
    #scheduled_time_dump = JSONField(blank=True, null=True)
    status = models.IntegerField(choices=CALLOPTIONS, default=3)
    time_refund = models.DurationField(default=timedelta)
    follow_up = models.BooleanField()
    student_rating = models.IntegerField(choices=RATINGOPTIONS, default=-1)
    student_comments = models.TextField(default="", blank=True)
    teacher_rating = models.IntegerField(choices=RATINGOPTIONS, default=-1)
    teacher_comments = models.TextField(default="", blank=True)
    session_number = models.IntegerField(default=1)
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
    student_pricing = models.ForeignKey("pricing.PriceModel", default=None, null=True, blank=True, related_name='student_pricing')
    teacher_pricing = models.ForeignKey("pricing.PriceModel", default=None, null=True, blank=True, related_name='teacher_pricing')

    def get_start_time(self):
        return self.start_time

    def __str__(self):
        return self.skill_match.skill.skill_name + " - " + self.skill_match.customer.customer_name + " - " + self.student.customer_name + " - Session" + str(
            self.session_number)

    def calculateTeacherAmount(self, timeDuration):
        return self.teacher_pricing.calculateAmount(timeDuration, True)
        '''timeSeconds = timeDuration.total_seconds()
        return (2.5 * timeSeconds) / 60'''

    def getEstimatedMinutes(self):
        return self.estimate_duration.total_seconds()/60

    def calculateStudentAmount(self, timeDuration):
        return self.student_pricing.calculateAmount(timeDuration, False)
        '''timeSeconds = timeDuration.total_seconds()
        minutes = timeSeconds / 60
        timeSeconds = timeSeconds % 60
        if timeSeconds > 0:
            minutes += 1
        roundedTimeDuration = minutes
        # print minutes
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
        return cost'''

    def getMinuteDuration(self):
        time_seconds = self.total_duration.total_seconds()
        minutes = time_seconds / 60
        time_seconds %= 60
        if time_seconds > 0:
            minutes += 1
        return minutes

    def calculateEstimatedStudentAmount(self):
        return self.calculateStudentAmount(self.estimate_duration)

    def calculateEstimatedTeacherAmount(self):
        return self.calculateTeacherAmount(self.estimate_duration)

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.__stud_rating = self.student_rating
        self.__teach_rating = self.teacher_rating

    def save(self, *args, **kwargs):
        calls = Call.objects.filter(belong_session=self)
        self.total_duration = timedelta()
        self.total_calls = 0
        self.start_time = timezone.now()
        self.end_time = timezone.now().replace(year=1970, month=1, day=1, hour=0, minute=0, second=0)
        if self.rescheduled_time == None:
            self.rescheduled_time = self.scheduled_time
        for call in calls:
            self.start_time = min(call.start_time, self.start_time)
            self.end_time = max(call.end_time, self.end_time)
            self.total_duration += call.call_duration
            self.total_calls += 1
        self.call_time_range = self.end_time - self.start_time
        if self.student_pricing is None:
            if self.skill_match.student_pricing is None:
                self.student_pricing = self.skill_match.skill.student_pricing
            else:
                self.student_pricing = self.skill_match.student_pricing
        if self.teacher_pricing is None:
            if self.skill_match.teacher_pricing is None:
                self.teacher_pricing = self.skill_match.skill.teacher_pricing
            else:
                self.teacher_pricing = self.skill_match.teacher_pricing
        self.amount_to_teacher = self.calculateTeacherAmount(self.total_duration)
        self.money_refund = self.calculateStudentAmount(self.time_refund)
        self.amount_from_student = self.calculateStudentAmount(self.total_duration)
        self.minutes_duration = self.getMinuteDuration()
        self.balance_amount = self.amount_from_student - self.money_refund
        super(Session, self).save(*args, **kwargs)
        self.order_id = hex(self.id + 100000).split('x')[1].upper()
        super(Session, self).save(*args, **kwargs)
        sessions = Session.objects.filter(student=self.student).filter(
            skill_match__skill=self.skill_match.skill).order_by('start_time')
        #print sessions
        number = 1
        for session in sessions:
            session.session_number = number
            number += 1
            super(Session, session).save(*args, **kwargs)
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


CALLMODEOPTIONS = (
    ("skype", 'Skype'),
    ("gmail", 'Gmail Call'),
    ("appear", 'Appear.in'),
    ("imo", 'Imo'),
    ("whatsapp", 'Whatsapp Call'),
    ("facebook", 'Facebook Call'),
    ("zoom", 'Zoom'),
    ("phone", 'Phone'),
    ("chat", 'Chat'),
    ("sms", 'SMS'),
    ("others", 'Others'),
)

VIDEOCALLRATINGOPTIONS = (
    (1, "Couldn\'t be copleted"),
    (2, "Many breakages"),
    (3, "No breakage but not a good call"),
    (4, "Decent call without breakages"),
    (5, "Excellent call"),
)

MONITOREDOPTIONS = (
    ("fully", "Fully monitored"),
    ("partially", "Partially Monitored"),
    ("notmonitor", "Not Monitored"),
    ("couldnot", "Could Not Monitor"),
)


class Call(BaseModel):
    objects = CallQuerySet.as_manager()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    belong_session = models.ForeignKey(Session, default=None)
    status = models.IntegerField(choices=CALLOPTIONS, default=1)
    follow_up = models.BooleanField()
    call_mode = models.CharField(max_length=20, choices=CALLMODEOPTIONS, default="skype")
    platform_tries = models.IntegerField(default=1)
    teacher_visible = models.BooleanField(default=True)
    teacher_audible = models.BooleanField(default=True)
    student_visible = models.BooleanField(default=True)
    student_audible = models.BooleanField(default=True)
    video_call_rating = models.IntegerField(choices=VIDEOCALLRATINGOPTIONS, default=4)
    monitored = models.CharField(max_length=20, choices=MONITOREDOPTIONS, default="fully")
    call_duration = models.DurationField(default=timedelta)

    # firstEntry = True;
    def __str__(self):
        # return "inserted"
        return str(self.start_time) + " - " + str(self.end_time)

    def save(self, *args, **kwargs):
        self.call_duration = self.end_time - self.start_time
        super(Call, self).save(*args, **kwargs)
        self.belong_session.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        belongSession = self.belong_session
        super(Call, self).delete(*args, **kwargs)
        belongSession.save(*args, **kwargs)
