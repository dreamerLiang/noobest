from utils.api import get_watcher 
from utils.constants import ErrorList
from django.shortcuts import render, HttpResponseRedirect


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
        match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:9]


        for match_id in match_id_list:
            get_watcher().get_match(match_id)
 
        return render(request, "result.html", locals())

    return render(request, "search.html", locals())
