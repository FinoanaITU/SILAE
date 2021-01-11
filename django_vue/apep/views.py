from django.shortcuts import render
from django.http import JsonResponse
from .analyse.file import FileAnalyse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def valueJson(request):
    file = request.FILES['DSN']
    analyse = FileAnalyse()
    if analyse.isZipFileUpload(file.name):
        data = analyse.dataByzip(file)
    else:
        file_data_content = analyse.getFileContent(file = file)
        data = analyse.compareFileAndDoc(type='autre', file_data = file_data_content)

    return JsonResponse(data, safe=False)