from django.conf.urls import url
from websites import views
from websites import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index', views.index),
    url(r'^about', views.about),
    url(r'^summoner', views.summoner),
    url(r'^search', views.search),
    url(r'^result/(?P<username>[-\w]+)', views.result),
    url(r'^transition/(?P<username>[-\w]+)', views.transition),
    url(r'^testing', views.testing),
]
