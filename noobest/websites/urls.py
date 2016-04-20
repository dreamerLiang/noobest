from django.conf.urls import url
from websites import views

urlpatterns = [
    url(r'^$', views.index),
]
