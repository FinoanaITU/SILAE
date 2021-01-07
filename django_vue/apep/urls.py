from os import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url('json/', views.valueJson)
]
