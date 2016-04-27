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
league = {0: 1, 1: 6, 2: 2, 3: 0, 4: 4, 5: 5, 6: 3}

mu = [
   [2.9985751419647575, 3.2927085890083183, 2.2499402637632047, 3.328697734056021], 
   [1.5315154200639154, 4.210701202480217, 5.736962597498994, 2.522155219524458], 
   [2.0147844512448128, 3.6438221008976264, 3.5490984611013845, 3.0577500291761655], 
   [1.615236075747171, 3.6807129155959872, 2.078928093252369, 2.743454999583669], 
   [4.319758882805678, 3.2732471383479638, 2.3451340763637765, 3.559368219774286], 
   [4.23911216061878, 3.3324712768246103, 4.225852798458452, 3.5043462359868975], 
   [1.0050078064408936, 4.9368636207499135, 3.2376914847135443, 1.9868617315462598]
]

def get_distance(point_a, point_b):
    return numpy.sqrt(sum((numpy.array(point_a) - numpy.array(point_b)) ** 2))

def get_rank(vector):
    distances = [get_distance(m, vector) for m in mu]
    index = distances.index(min(distances))
    return index, RANK_DEFAULT_CHOICES[league[index]]

def get_vector(data):
    vector = [data[key] for key in items]
    vector[1] = math.sqrt(vector[1])
    vector[0] *= 0.68
    vector[3] *= 2.25
    return vector

def get_data(fid, all_players_id):
    minionsKilled = 0
    goldEarned = 0
    totalDamageDealtToChampions = 0
    wardsPlaced = 0
    kills = 0
    assists = 0
    deaths = 0
    damage_per_gold = 0
    cs_per_minute = 0
    kda = 0
    wardsPlaced_per_minute = 0
    arrayList_for_rank = []
    for data in all_players_id[fid]:
        specific_match = data[0]
        position = data[1]
        match_time = specific_match['matchDuration']
        print match_time
        for participants in specific_match['participants'][position - 1]['stats']:
            if str(participants) == 'goldEarned':
                goldEarned = specific_match['participants'][position - 1]['stats'][participants] 
            elif str(participants) == 'totalDamageDealtToChampions':
                totalDamageDealtToChampions = specific_match['participants'][position - 1]['stats'][participants] 
            elif str(participants) == 'minionsKilled': 
                minionsKilled = specific_match['participants'][position - 1]['stats'][participants]
            elif str(participants) == 'wardsPlaced':
                wardsPlaced = specific_match['participants'][position - 1]['stats'][participants] 
            elif str(participants) == 'kills':
                kills = specific_match['participants'][position - 1]['stats'][participants]
            elif str(participants) == 'assists':
                assists = specific_match['participants'][position - 1]['stats'][participants]
            elif str(participants) == 'deaths':
                deaths = specific_match['participants'][position - 1]['stats'][participants]
        damage_per_gold += float(totalDamageDealtToChampions) / float(goldEarned)
        cs_per_minute += float(minionsKilled) / float((match_time / 60))
        kda += float((kills + assists)) / float((deaths + 1))
        wardsPlaced_per_minute += float(wardsPlaced)

    damage_per_gold /= len(all_players_id[fid])
    cs_per_minute /= len(all_players_id[fid])  
    kda /= len(all_players_id[fid])
    wardsPlaced_per_minute /= len(all_players_id[fid])

    data = {
    	'damage_per_gold': damage_per_gold,
        'cs_per_minute': cs_per_minute,
        'kda': kda,
    	'wards_placed_per_minute': wardsPlaced_per_minute
    }

    return data

def get_score(vector, index):
    scores = dict()
    scores['total'] = 0
    for i in range(len(vector)):
        score = float(vector[i]) / float(mu[index][i]) * 100 
        if score > 100:
            score = 100
        scores[items[i]] = score
        scores['total'] += score * importance[i]
    return scores

