from utils.api import get_watcher
from rank.views import rank
from django.shortcuts import render, HttpResponseRedirect
from utils.constants import ErrorList

import operator

def index(request):
    return render(request, "index.html", locals())
def about(request):
    return render(request, "about.html", locals())

def result(request):
    return render(request, "result.html", locals())
def transition(request):
    return render(request, "transition.html", locals())

def testing(request):
    return render(request, "testing.html", locals())

def summoner(request):
    print "returning result"
    if request.is_ajax():
        #deal with the user input here.
        # rank(user)
        # redirect to result display page
        return render(request, "result.html", locals())
    return render(request, "search.html", locals())

def search(request):
    if request.is_ajax():
        if not 'name' in request.POST:
            return render(request, "search.html", locals())

        name = request.POST.get('name')

        try:
            me = get_watcher().get_summoner(name=name)
        except:
            error_code = ErrorList.USER_NOT_FOUND
            return render(request, "search.html", locals())
        match = get_watcher().get_match_list(me['id'],'na')
        match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:5]
        print(match_id_list)
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
        print "Friend id:\n"
        print friends_id

        for fid in friends_id:
            if fid == me['id']:
                continue
            #print all_players_id[fid]
            #arrayList for a friend to rank
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

        return render(request, "result.html", locals())
    return render(request, "search.html", locals())
