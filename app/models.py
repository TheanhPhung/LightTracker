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
        return timezone.now() - self.ejaculation_time

    def non_porn(self):
        return timezone.now() - self.porn_time

    def non_masturbation(self):
        return timezone.now() - self.masturbation_time
