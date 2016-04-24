from utils.api import get_watcher
from rank.views import rank
from django.shortcuts import render, HttpResponseRedirect
from utils.constants import ErrorList

import operator

def index(request):
    return render(request, "index.html", locals())
def about(request):
    return render(request, "about.html", locals())

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
        match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:20]
        match_details = []
        all_players_id = dict()

        for match_id in match_id_list:
            match_detail = get_watcher().get_match(match_id)
            match_details.append(match_detail)
            for data in match_detail['participantIdentities']:
                if data['player']['summonerName'] in all_players_id:
                    all_players_id[data['player']['summonerName']].append([match_detail, data['participantId']])
                else:
                    all_players_id[data['player']['summonerName']] = [[match_detail, data['participantId']]]

        friends_id = [key for key, value in all_players_id.items() if len(value) > 1]
        print "Friend id:\n"
        print friends_id

        for fid in friends_id:
            #print all_players_id[fid]
            for data in all_players_id[fid]:
                #print data
                specific_match = data[0]
                #print specific_match
                for participants in specific_match['participants'][0]['stats']:
                    print specific_match['participants'][0]['stats'][participants]    
                
        # for match_detail in match_details:
        #     for data in match_detail['participantIdentities']:
        #         if data['player']['summonerName'] in friends_id:
        #             print data['player']['summonerName']

        #for friends_id_object in friends_id:
        #     for data in match_detail['participantIdentities']:
        #         if data['player']['summonerId'] == friends_id_object:
        #             print friends_id_object
                #summonerId_list_in_Game = match_detail['summonerID']
                # if found:      
                #     print 'found'
        return render(request, "result.html", locals())
 
        # if not exists('name'):
        #     return render(request, "error.html", locals())
        # else:
        #     # check if we have API calls remaining
        #    print(get_watcher().can_make_request())

        # try:
        #     me = get_watcher().get_summoner(name=name)
        #     print(me)
        # except:
        #     error_code = ErrorList.USER_NOT_FOUND
        #     return render(request, "search.html", locals())

        # match = get_watcher().get_match_list(me['id'],'na')
        # #print(match)
        # match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:9]
        # print(match_id_list)
        # match_result_list[9]
        # count = 0
        # for match_id in match_id_list:
        #     match_result_list[count] = get_watcher().get_match(match_id)
        #     count = count + 1
            
        # #rank(user)
        # rank(match_result_list)

        # redirect to result display page

        #return render(request, "result.html", locals())
    return render(request, "search.html", locals())
