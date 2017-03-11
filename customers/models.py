# from __future__ import unicode_literals

# from django.db import models

# Create your models here.
from django.db import models
# from proj.models import Skill
from session.models import Session
from payment.models import Payment, Payout, Transfer
from django.utils.encoding import python_2_unicode_compatible
from base.models import BaseModel
from allauth.socialaccount.models import SocialAccount

GENDEROPTIONS = (
    ('f', 'Female'),
    ('m', 'Male'),
    ('o', 'Other'),
    ('d', 'Decline to State'),
)


class Customer(BaseModel):
    customer_name = models.CharField(max_length=200)
    social = models.ForeignKey(SocialAccount, default=None, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, choices=GENDEROPTIONS, default='d')
    image = models.CharField(max_length=200, blank=True)
    skype_id = models.CharField(max_length=200, blank=True)
    gmail_id = models.CharField(max_length=200, blank=True)
    paytm_id = models.CharField(max_length=200, blank=True)
    customer_code = models.CharField(max_length=200, default="")
    no_subjects = models.IntegerField(default=0)
    wallet_amount = models.FloatField(default=0)
    classes_taken = models.IntegerField(default=0)
    classes_given = models.IntegerField(default=0)
    student_rating = models.FloatField(default=0)
    student_rating_count = models.IntegerField(default=0)
    teacher_rating = models.FloatField(default=0)
    teacher_rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.customer_name

    def add_student_rating(self, stud_rating):
        existingRating = self.student_rating*self.student_rating_count
        existingRating += stud_rating
        self.student_rating_count += 1
        self.student_rating = existingRating/self.student_rating_count
        self.save()

    def update_student_rating(self, old_stud_rating, stud_rating):
        existingRating = self.student_rating * self.student_rating_count
        existingRating += (stud_rating - old_stud_rating)
        self.student_rating = existingRating / self.student_rating_count
        self.save()

    def add_teacher_rating(self, teach_rating):
        existingRating = self.teacher_rating*self.teacher_rating_count
        existingRating += teach_rating
        self.teacher_rating_count += 1
        self.teacher_rating = existingRating/self.teacher_rating_count
        self.save()

    def update_teacher_rating(self, old_teach_rating, teach_rating):
        existingRating = self.teacher_rating * self.teacher_rating_count
        existingRating += (teach_rating - old_teach_rating)
        self.teacher_rating = existingRating / self.teacher_rating_count
        self.save()

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
        sessions = Session.objects.filter(student=self)
        self.student_rating = 0
        self.student_rating_count = 0
        for session in sessions:
            self.wallet_amount -= session.balance_amount
            if session.student_rating != -1:
                self.student_rating += session.student_rating
                self.student_rating_count += 1
        if self.student_rating_count > 0:
            self.student_rating /= self.student_rating_count
        self.classes_taken = len(sessions)
        self.classes_given = 0
        skillMatches = SkillMatch.objects.filter(customer=self)
        self.no_subjects = len(skillMatches)
        self.teacher_rating = 0
        self.teacher_rating_count = 0
        for skillMatch in skillMatches:
            self.teacher_rating += skillMatch.teacher_rating*skillMatch.teacher_rating_count
            self.teacher_rating_count += skillMatch.teacher_rating_count
            self.classes_given += skillMatch.classes_given
            teacher_sessions = Session.objects.filter(skill_match=skillMatch)
            for session in teacher_sessions:
                self.wallet_amount += session.amount_to_teacher
        if self.teacher_rating_count > 0:
            self.teacher_rating /= self.teacher_rating_count
        payments = Payment.objects.filter(customer=self)
        for payment in payments:
            self.wallet_amount += payment.amount
        payouts = Payout.objects.filter(customer=self)
        for payout in payouts:
            self.wallet_amount -= payout.amount
        transfers = Transfer.objects.filter(customer=self)
        for transfer in transfers:
            self.wallet_amount -= transfer.amount
        transfers = Transfer.objects.filter(customer_to_transfer=self)
        for transfer in transfers:
            self.wallet_amount += transfer.amount
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
    details = models.TextField(default="", blank=True)
    classes_given = models.IntegerField(default=0)
    teacher_rating = models.FloatField(default=0)
    teacher_rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.skill.skill_name + " - " + self.customer.customer_name

    def add_teacher_rating(self, teach_rating):
        existingRating = self.teacher_rating*self.teacher_rating_count
        existingRating += teach_rating
        self.teacher_rating_count += 1
        self.teacher_rating = existingRating/self.teacher_rating_count
        self.save()

    def update_teacher_rating(self, old_teach_rating, teach_rating):
        existingRating = self.teacher_rating * self.teacher_rating_count
        existingRating += (teach_rating - old_teach_rating)
        self.teacher_rating = existingRating / self.teacher_rating_count
        self.save()

    def save(self, *args, **kwargs):
        sessions = Session.objects.filter(skill_match=self)
        self.classes_given = len(sessions)
        self.teacher_rating = 0
        self.teacher_rating_count = 0
        for session in sessions:
            if session.teacher_rating != -1:
                self.teacher_rating += session.teacher_rating
                self.teacher_rating_count += 1
        if self.teacher_rating_count > 0:
            self.teacher_rating /= self.teacher_rating_count
        super(SkillMatch, self).save(*args, **kwargs)
        self.skill.save(*args, **kwargs)
        self.customer.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        skill = self.skill
        customer = self.customer
        super(SkillMatch, self).delete(*args, **kwargs)
        skill.save(*args, **kwargs)
        customer.save(*args, **kwargs)
