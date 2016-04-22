from django.shortcuts import render
from utils.api import watcher
from django.shortcuts import render, HttpResponseRedirect


def index(request):
	return render(request, "index.html", locals())
def about(request):
	#return HttpResponseRedirect("about.html")
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
	return render(request, "result.html", locals())