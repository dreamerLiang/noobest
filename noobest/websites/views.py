from utils.api import get_watcher
from rank.views import rank
from django.shortcuts import render, HttpResponseRedirect

import operator

def index(request):
    return render(request, "index.html", locals())
def about(request):
    return render(request, "about.html", locals())

def result(request):
    return render(request, "result.html", locals())

def transition(request):
    return render(request, "transition.html", locals())

def summoner(request):
    if request.is_ajax():
        #deal with the user input here.
        # rank(user)
        # redirect to result display page
        return render(request, "result.html", locals())
    return render(request, "search.html", locals())

def search(request):
    if request.is_ajax():
        # if not 'name' in request.POST:
        #     return render(request, "search.html", locals())

        # name = request.POST.get('name')

        # try:
        #     me = get_watcher().get_summoner(name=name)
        # except:
        #     error_code = ErrorList.USER_NOT_FOUND
        #     return render(request, "search.html", locals())
        # match = get_watcher().get_match_list(me['id'],'na')
        # match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:15]
        # match_details = []
        # all_players_id = dict()

        # for match_id in match_id_list:
        #     match_detail = get_watcher().get_match(match_id)
        #     match_details.append(match_detail)
        #     for data in match_detail['participantIdentities']:
        #         if data['player']['summonerId'] in all_players_id:
        #             all_players_id[data['player']['summonerId']] += 1
        #         else:
        #             all_players_id[data['player']['summonerId']] = 1

        # sorted_all_players_id = sorted(all_players_id.items(), key=operator.itemgetter(1))
        # friends_id = [key for key, value in sorted_all_players_id if value > 1]
        # print friends_id
        return render(request, "result.html", locals())
 
    return render(request, "search.html", locals())
