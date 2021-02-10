from os import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url('json/', views.valueJson),
    url('generatePDF/', views.generatePDF),
    url('generateExcel/', views.generateExcel),
    url('sendEmail/', views.sendEmail),
]
