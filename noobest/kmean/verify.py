from rank.models import Player
from kmean.kmean import Kmean
from rank.training import search
from utils.api import get_watcher
from rank.constants import RANK_DEFAULT_CHOICES

import json
import math
import numpy

items = ['cs_per_minute', 'wards_placed_per_minute', 'kda', 'damage_per_gold']
importance = [0.3, 0.2, 0.3, 0.2]

def get_distance(point_a, point_b):
	return numpy.sqrt(sum((numpy.array(point_a) - numpy.array(point_b)) ** 2))

def score(point, index):
	total = 0
	for i in range(len(point)):
		score = float(point[i]) / float(mu[index][i]) * 100 
		if score > 100:
			score = 100
		print "score on " + items[i] + " " + str(score)
		total += score * importance[i]
	return total


players = Player.objects.all()

vectors = [player.vector for player in players]
vectors = [json.loads(vector.replace("'", '"')) for vector in vectors]
points = [[vector[key] for key in items] for vector in vectors]
for point in points:
	point[0] *= 0.68
	point[3] *= 2.25
	point[1] = math.sqrt(point[1])

algo = Kmean(points, 7)
mu, clusters_points = algo.get_clusters()

mu = [m.tolist() for m in mu]

# mu = [
# 	[2.9985751419647575, 3.2927085890083183, 2.2499402637632047, 3.328697734056021], 
# 	[1.5315154200639154, 4.210701202480217, 5.736962597498994, 2.522155219524458], 
# 	[2.0147844512448128, 3.6438221008976264, 3.5490984611013845, 3.0577500291761655], 
# 	[1.615236075747171, 3.6807129155959872, 2.078928093252369, 2.743454999583669], 
# 	[4.319758882805678, 3.2732471383479638, 2.3451340763637765, 3.559368219774286], 
# 	[4.23911216061878, 3.3324712768246103, 4.225852798458452, 3.5043462359868975], 
# 	[1.0050078064408936, 4.9368636207499135, 3.2376914847135443, 1.9868617315462598]
# ]

mu_scores = [get_distance(m, [0,0,0,0]) for m in mu]
# print mu_scores
mu_scores = sorted(mu_scores)
# print mu_scores

league = {}

for i in mu:
	league[mu.index(i)] = mu_scores.index(get_distance(i, [0,0,0,0]))

name = 'caaaaaaaaaaaaake'
me = get_watcher().get_summoner(name=name)
userid = int(me['id'])
data = search(userid)
point = [data[key] for key in items]
point[1] = math.sqrt(point[1])
point[0] *= 0.68
point[3] *= 2.25

distances = [get_distance(m, point) for m in mu]
index = distances.index(min(distances))
print score(point, index)
print RANK_DEFAULT_CHOICES[league[index]]


count = 0
players = Player.objects.all()
for player in players:
	vector = json.loads(player.vector.replace("'", '"'))
	point = [vector[key] for key in items]
	point[1] = math.sqrt(point[1])
	distances = [get_distance(m, point) for m in mu]
	index = distances.index(min(distances))
	if abs(league[index] - player.rank) <= 2:
		count += 1

print float(count) / len(players)