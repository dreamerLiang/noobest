#coding: utf-8

from riotwatcher import RiotWatcher, RateLimit
from kmean import Kmean
from rank.models import Player
from utils.api import get_watcher
import random
import time

names = ['danjuanmao', 'wukoutian', 'PicturedLighting', 'MYETM', 'lceland', 'Theifz', 'Eveloken']

target = []

for name in names:
	me = get_watcher().get_summoner(name=name)
	users = get_watcher().get_league([me['id']], region='na')[str(me['id'])][0]['entries']
	for user in users:
		player = Player.objects.get(username=user['playerOrTeamName'], userid=int(user['playerOrTeamId']))
		if user['division'] == "I":
			player.division = 1
		elif user['division'] == "II":
			player.division = 2
		elif user['division'] == "III":
			player.division = 3
		elif user['division'] == "IV":
			player.division = 4
		elif user['division'] == "V":
			player.division = 5
		player.save()
		
	# user_ids = [int(user['playerOrTeamId']) for user in users]
	# target.append(user_ids)

# open("training_user_ids.txt", "w").write(str(target))


# print len(data[0] + data[1] + data[2] + data[3] + data[4] + data[5] + data[6])


# points = [[1, 2], [2, 1], [3, 1], [5, 4], [5, 5], [6, 5], [7, 9], [99, 96], [94, 91], [92, 89]]
# algo = Kmean(points, 2)
# mu, clusters_points = algo.get_clusters()

# print "for league of legand"

# data = [[1,2,3,4], [2,3,4,5], [1,2,3,4], [8,8,8,9], [10,10,10,2]]
# algo = Kmean(data, 2)
# mu, clusters_points = algo.get_clusters()

# print mu
# print clusters_points
