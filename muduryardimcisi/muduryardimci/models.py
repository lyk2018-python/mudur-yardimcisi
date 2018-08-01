from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Site(models.Model):

    name = models.CharField(max_length=255, unique=True)
    year = models.DateField()
    logo = models.FileField(blank=True)
    is_active = models.BooleanField(default=False)
    domain = models.CharField(max_length=100)
    start_date = models.DateField()
    end_Date = models.DateField()
    total_morning_date = models.FloatField()
    total_afternoon_date = models.FloatField()
    total_evening_date = models.FloatField()

    def __str__(self):
        return self.domain

class Courses(models.Model):

    course_name = models.CharField(max_length=255)
    trainess = models.ForeignKey(
               default="",
               to=settings.AUTH_USER_MODEL,
               on_delete=models.CASCADE,
               related_name="trainess_name",
                        )

    trainer = models.ForeignKey(
              default="",
              to=settings.AUTH_USER_MODEL,
              on_delete=models.CASCADE,
              related_name="trainer_name",
              )

    authorized_trainer = models.ForeignKey(
                         default="",
                         to=settings.AUTH_USER_MODEL,
                         on_delete=models.CASCADE,
                         related_name="authorized_trainer_name",
                         )

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name_plural = "Courses"

class Check(models.Model):

    course_id = models.ForeignKey(
                default="",
                to=Courses,
                related_name="Check_Course_id",
                on_delete=models.CASCADE
                                  )
    user_id = models.ForeignKey(
               default="",
               to=settings.AUTH_USER_MODEL,
               related_name="Check_user_id",
               on_delete=models.CASCADE
    )

    course_check = models.CharField(max_length=255, unique=True) # öğrenci Tablosu yapılacak
    check_morning = models.BooleanField(default=False)
    check_afternoon = models.BooleanField(default=False)
    check_evening = models.BooleanField(default=False)

    def __str__(self):
        return self.course_check

class Note(models.Model):
    user_id = models.ForeignKey(
            default="",
            to=settings.AUTH_USER_MODEL,
            related_name="Note_user_id",
            on_delete=models.CASCADE,
            )
    trainer_id = models.ForeignKey(
            default="",
            to=settings.AUTH_USER_MODEL,
            related_name="Note_trainer_id",
            on_delete=models.CASCADE,
            )
    notes = models.TextField(
            max_length=2000
            )
    site_id = models.ForeignKey(
            default="",
            to=Site,
            related_name="Note_site_id",
            on_delete=models.CASCADE,
            )

    def __str__(self):
        return self.notes