from django.shortcuts import render
from django.http import JsonResponse
from .analyse.file import FileAnalyse
from .analyse.pdf import pdf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json

@csrf_exempt
def valueJson(request):
    file = request.FILES['DSN']
    analyse = FileAnalyse()
    if analyse.isZipFileUpload(file.name):
        data = analyse.dataByzip(file)
    else:
        file_data_content = analyse.getFileContent(file = file)
        data = [analyse.compareFileAndDoc(type='autre', file_data = file_data_content)]
        print(data)

    return JsonResponse(data, safe=False)

@csrf_exempt
def generatePDF(request):
    data = json.loads(request.body)
    generate = pdf()
    print(json.dumps(data))
    generate.createPDF(data)
    return JsonResponse({'wawa': 20})