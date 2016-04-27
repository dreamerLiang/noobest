from __future__ import unicode_literals
from rank.constants import RANK_DEFAULT_CHOICES
from django.db import models
import json

class Player(models.Model):
    username = models.CharField('username', max_length=255, blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)
    vector = models.CharField(max_length=255, blank=True, null=True)
    scores = models.CharField(max_length=255, blank=True, null=True)
    friends = models.CharField(max_length=255, blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField('rank', blank=True, null=True, choices=RANK_DEFAULT_CHOICES)
    division = models.IntegerField(blank=True, null=True)
    evaluation = models.IntegerField(blank=True, null=True, choices=RANK_DEFAULT_CHOICES)

    def get_user_vector_cs(self):
    	return int (1000 * json.loads(self.vector.replace("'", '"'))['cs_per_minute'])

    def get_user_vector_wd(self):
    	return int (1000 * json.loads(self.vector.replace("'", '"'))['wards_placed_per_minute'])

    def get_user_vector_kda(self):
    	return int (1000 * json.loads(self.vector.replace("'", '"'))['kda'])

    def get_user_vector_dmg(self):
    	return int (1000 * json.loads(self.vector.replace("'", '"'))['damage_per_gold'])