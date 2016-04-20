from django.shortcuts import render
from utils.api import watcher


def index(request):
	return render(request, "index.html", locals())

def summoner(request):
	if request.is_ajax():
		#deal with the user input here.
		# rank(user)
		# redirect to result display page
		return render(request, "result.html", locals())
	return render(request, "search.html", locals())

