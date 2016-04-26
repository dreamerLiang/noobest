from django.shortcuts import render

# Create your views here.
def rank(data):
    return 100

def get_vector(fid, all_players_id):
    minionsKilled = 0
    goldEarned = 0
    totalDamageDealtToChampions = 0
    wardsPlaced = 0
    kills = 0
    assists = 0
    deaths = 0
    # core needed data
    damage_per_gold = 0
    cs_per_minute = 0
    kda = 0
    #kill_contribution = 0
    wardsPlaced_per_minute = 0
    arrayList_for_rank = []
    for data in all_players_id[fid]:
        #print data
        specific_match = data[0]
        position = data[1]
        #set match time
        match_time = specific_match['matchDuration']
        print match_time
        for participants in specific_match['participants'][position - 1]['stats']:
            if str(participants) == 'goldEarned':
                goldEarned = specific_match['participants'][position - 1]['stats'][participants] 
                print str(position) + " " + str(participants) + ":" + str(goldEarned) #+ str(specific_match['participants'][position - 1]['stats'][participants])  
            elif str(participants) == 'totalDamageDealtToChampions':
                totalDamageDealtToChampions = specific_match['participants'][position - 1]['stats'][participants] 
                print str(position) + " " + str(participants) + ":" + str(totalDamageDealtToChampions)  
            elif str(participants) == 'minionsKilled': 
                minionsKilled = specific_match['participants'][position - 1]['stats'][participants]
                print str(position) + " " + str(participants) + ":" + str(minionsKilled)
            elif str(participants) == 'wardsPlaced':
                wardsPlaced = specific_match['participants'][position - 1]['stats'][participants] 
                print str(position) + " " + str(participants) + ":" + str(wardsPlaced) 
            elif str(participants) == 'kills':
                kills = specific_match['participants'][position - 1]['stats'][participants]
                print str(position) + " " + str(participants) + ":" + str(kills)
            elif str(participants) == 'assists':
                assists = specific_match['participants'][position - 1]['stats'][participants]
                print str(position) + " " + str(participants) + ":" + str(assists)
            elif str(participants) == 'deaths':
                deaths = specific_match['participants'][position - 1]['stats'][participants]
                print str(position) + " " + str(participants) + ":" + str(deaths)
        #get needed data
        damage_per_gold += float(totalDamageDealtToChampions) / float(goldEarned)
        cs_per_minute += float(minionsKilled) / float((match_time / 60))
        kda += float((kills + assists)) / float((deaths + 1))
        #kill_contribution += float((kills + assists)) / float(teamKills)
        wardsPlaced_per_minute += float(wardsPlaced) / float((match_time / 60))
        print ""
        print "damage_per_gold :" + str(damage_per_gold)
        print "cs_per_minute :" + str(cs_per_minute)
        print "kda :" + str(kda)
        #print "kill_contribution :" + str(kill_contribution)
        print "wardsPlaced_per_minute :" + str(wardsPlaced_per_minute)
        print "" 
    #culmultate the data
    damage_per_gold /= len(all_players_id[fid])
    cs_per_minute /= len(all_players_id[fid])  
    kda /= len(all_players_id[fid])
    #kill_contribution /= len(all_players_id[fid])
    wardsPlaced_per_minute /= len(all_players_id[fid])
    #print average
    print ""
    print "friend_id :" + str(fid)
    print "total damage_per_gold :" + str(damage_per_gold)
    print "total cs_per_minute :" + str(cs_per_minute)
    print "total kda :" + str(kda)
    #print "total kill_contribution :" + str(kill_contribution)
    print "total wardsPlaced_per_minute :" + str(wardsPlaced_per_minute)
    print ""

    data = {
    	'damage_per_gold': damage_per_gold,
        'cs_per_minute': cs_per_minute,
        'kda': kda,
    	'wardsPlaced_per_minute': wardsPlaced_per_minute
    }
    return data

def get_score(data):
	#do something
	#WARNNING: only used for testing, not the real algorithm
	score = 0
	for d in data:
	    score += data[d]
	return score


