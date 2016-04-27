from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from rank.constants import RANK_DEFAULT_CHOICES
from django.db import models


class Player(models.Model):
    username = models.CharField('username', max_length=255, blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)
    vector = models.CharField(max_length=255, blank=True, null=True)
    scores = models.CharField(max_length=255, blank=True, null=True)
    rank = models.IntegerField('rank', blank=True, null=True, choices=RANK_DEFAULT_CHOICES)
    division = models.IntegerField(blank=True, null=True)
    evaluation = models.IntegerField(blank=True, null=True, choices=RANK_DEFAULT_CHOICES)
