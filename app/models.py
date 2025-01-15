from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from datetime import date


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    ejaculation_time = models.DateTimeField(null=True, blank=True)
    porn_time = models.DateTimeField(null=True, blank=True)
    masturbation_time = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(default = 1)
    ejaculation_target = models.IntegerField(default = 7)
    porn_target = models.IntegerField(default=7)
    masturbation_target = models.IntegerField(default=7)

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def non_ejaculation(self):
        return self.convert_time(timezone.now() - self.ejaculation_time) 

    def non_porn(self):
        return self.convert_time(timezone.now() - self.porn_time)

    def non_masturbation(self):
        return self.convert_time(timezone.now() - self.masturbation_time)

    def ejaculation_progress(self):
        return (self.non_ejaculation()["days"] / self.ejaculation_target) * 100

    def masturbation_progress(self):
        return (self.non_masturbation()["days"] / self.masturbation_target) * 100

    def porn_progress(self):
        return (self.non_porn()["days"] / self.porn_target) * 100

    def convert_time(self, time_delta):
        days = time_delta.days
        time_delta = time_delta.seconds + days * 86400
        minutes, seconds = divmod(time_delta, 60)
        hours, minutes = divmod(minutes, 60)
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }
