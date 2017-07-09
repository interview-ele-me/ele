from django.db import models
from django.contrib.auth.models import User


class Prize(models.Model):
    name = models.CharField(max_length=100, default='')
    total_num = models.IntegerField(default=0)
    lucky_num = models.IntegerField(default=0)
    img = models.FileField(upload_to='prize_image/')


class UserByPrize(models.Model):
    user = models.ForeignKey(User)
    prize = models.ForeignKey(Prize)
    lucky_num = models.IntegerField(default=0)
    create_time = models.DateField(auto_now=True)


class Result(models.Model):
    user = models.ForeignKey(User)
    prize = models.ForeignKey(Prize)
    lucky_num = models.IntegerField(default=0)
