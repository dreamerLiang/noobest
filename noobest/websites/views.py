from django.shortcuts import render
from utils.api import watcher as w


def index(request):
    return render(request, "index.html", locals())

def summoner(request):
    if request.is_ajax():
        #deal with the user input here.
        if not 'name' in request.POST:
        #return false

        #get user name
        name = request.POST.get('name')
        # check if the name exist
        if not exists('name'):
            return render(request, "error.html", locals())
        else:
            # check if we have API calls remaining
            print(w.can_make_request())

            me = w.get_summoner(name=name)
            print(me)

            match = w.get_match_list(me['id'],'na')
            #print(match)
            match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:9]
            print(match_id_list)
            for i in match_id_list:
                w.get_match(i)
 




            #rank(user)
            # redirect to result display page
            return render(request, "result.html", locals())
    return render(request, "search.html", locals())
