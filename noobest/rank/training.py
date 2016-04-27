from rank.models import Player
from utils.api import get_watcher
import time
import json
def search(my_id):
    if True:
        match = get_watcher().get_match_list(my_id,'na')
        match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:9]
        match_details = []
        all_players_id = dict()
        for match_id in match_id_list:
            match_detail = get_watcher().get_match(match_id)
            match_details.append(match_detail)
            for data in match_detail['participantIdentities']:
                if data['player']['summonerId'] in all_players_id:
                    all_players_id[data['player']['summonerId']].append([match_detail, data['participantId']])
                else:
                    all_players_id[data['player']['summonerId']] = [[match_detail, data['participantId']]]
        friends_id = [key for key, value in all_players_id.items() if len(value) > 1]
        for fid in friends_id:
            if fid != my_id:
                continue
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
                'kda':kda, 
                'wards_placed_per_minute':wardsPlaced_per_minute
            }
            return data

count = 0
players = Player.objects.all()
players = [player for player in players if json.loads(player.vector.replace("'", '"'))['wards_placed_per_minute'] < 1]
for player in players:
    try:
        player.vector = search(player.userid)
        player.save()
        time.sleep(2)
    except:
        pass
    count += 1
    print float(count) / len(players)
