from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from datetime import date


class User(AbstractUser):
    ACT_LIST = ["ejaculation", "porn", "masturbation"]

    birth_date = models.DateField(null=True, blank=True)
    ejaculation_time = models.DateTimeField(null=True, blank=True)
    porn_time = models.DateTimeField(null=True, blank=True)
    masturbation_time = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(default = 1)
    ejaculation_target = models.IntegerField(default = 1)
    porn_target = models.IntegerField(default=1)
    masturbation_target = models.IntegerField(default=1)

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def no_action(self, act_code):
        time_field_name = self.ACT_LIST[act_code] + "_time"
        time_field_value = getattr(self, time_field_name)
        return timezone.now() - time_field_value

    def action_progress(self, act_code):
        time_delta = self.no_action(act_code).days * 86400 + self.no_action(act_code).seconds
        target_field_name = self.ACT_LIST[act_code] + "_target"
        target_time = getattr(self, target_field_name) * 86400
        return time_delta / target_time * 100

    def convert_time(self, act_code):
        time_delta = self.no_action(act_code)
        days = time_delta.days
        time_delta = time_delta.seconds + days * 86400
        minutes, seconds = divmod(time_delta, 60)
        hours, minutes = divmod(minutes, 60)
        hours %= 24
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }
