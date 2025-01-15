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

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def non_ejaculation(self):
        return self.convert_time(timezone.now() - self.ejaculation_time) 

    def non_porn(self):
        return self.convert_time(timezone.now() - self.porn_time)

    def non_masturbation(self):
        return self.convert_time(timezone.now() - self.masturbation_time)

    def convert_time(self, time_delta):
        time_delta = time_delta.seconds
        minutes, seconds = divmod(time_delta, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }
