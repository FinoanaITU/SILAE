from django.shortcuts import render
from django.http import JsonResponse
from .analyse.file import FileAnalyse

def valueJson(request):
    data = FileAnalyse().dataByzip('DSN.zip')
    return JsonResponse(data, safe=False)