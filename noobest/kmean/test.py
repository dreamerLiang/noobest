#coding: utf-8

from riotwatcher import RiotWatcher, RateLimit
import random
from kmean import Kmean

#watcher = RiotWatcher('96a7f2b9-8718-44e3-b5f9-d6316ffc47e3')

keys = ['03351eab-47cc-4a7f-97e0-af22a7c43782', 'b7f9571e-eeef-4c8d-a5a8-cb835a6f940d', '96a7f2b9-8718-44e3-b5f9-d6316ffc47e3']

watchers = [RiotWatcher(key, limits=(RateLimit(10, 10), )) for key in keys]

def get_watcher():
	while not watchers[0].can_make_request():
		temp = watchers.pop(0)
		watchers.append(temp)
	return watchers[0]

names = ['danjuanmao', 'Mr Ha1f', 'wukoutian', 'lceland', 'simple cup lin', 'Dsola', 'FlaminG GUI', 'PicturedLighting', 'MYETM']

name = 'wukoutian'
me = get_watcher().get_summoner(name=name)
match = get_watcher().get_match_list(me['id'],'na')
match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:9]

match_id = match_id_list[0]
match_detail = get_watcher().get_match(match_id)

print match_detail




# points = [[1, 2], [2, 1], [3, 1], [5, 4], [5, 5], [6, 5], [7, 9], [99, 96], [94, 91], [92, 89]]
# algo = Kmean(points, 2)
# mu, clusters_points = algo.get_clusters()

# print "for league of legand"

# data = [[1,2,3,4], [2,3,4,5], [1,2,3,4], [8,8,8,9], [10,10,10,2]]
# algo = Kmean(data, 2)
# mu, clusters_points = algo.get_clusters()

# print mu
# print clusters_points
