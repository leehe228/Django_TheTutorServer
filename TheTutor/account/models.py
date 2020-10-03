from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(models.Model):
    userid = models.CharField(primary_key=True, max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=100, default="")
    time_day = models.CharField(max_length=30, default="0-0-0-0-0-0-0")
    time_sub = models.CharField(max_length=30, default="0-0-0-0-0-0-0-0-0-0")
    todo_name = models.CharField(max_length=300, default="0:0")
    todo_num = models.IntegerField(default=1)
    sub_name = models.CharField(max_length=200, default="")
    sub_num = models.IntegerField(default=0)
    idCode = models.IntegerField(default=0)

    def __str__(self):
        return self.userid

