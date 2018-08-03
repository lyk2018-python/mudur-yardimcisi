from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Site(models.Model):

    name = models.CharField(max_length=255, unique=True)
    year = models.DateField()
    logo = models.FileField(blank=True)
    is_active = models.BooleanField(default=False)
    domain = models.CharField(max_length=100)
    start_date = models.DateField()
    end_Date = models.DateField()
    course_start = models.CharField(max_length=15,default="")
    total_morning_date = models.FloatField()
    total_afternoon_date = models.FloatField()
    total_evening_date = models.FloatField()

    def __str__(self):
        return self.domain

class Courses(models.Model):
    course_name = models.CharField(max_length=255)

    course_token = models.CharField(
                   max_length=255,
                   default="",
                   null="")


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(
                default=None,
                to=Courses,
                on_delete=models.CASCADE,
                blank=True,
                null=True,
                )

    email = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True,
            )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="""Telefon numaranız 5340775723 şeklinde girilmelidir."
                                          14 haneye kadar izin verilir. """,)

    cellphone = models.CharField(validators=[phone_regex],max_length=14)
    telegram_username = models.CharField(
                        max_length=25,
                        blank=True,
                        null=True,)
    is_trainer = models.BooleanField(
                 default=False,

    )
    def __str__(self):
        return self.email