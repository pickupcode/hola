from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

def login(request):

    data= {'resultado':'True'}
    json_data= json.dumps(data)
    print(json_data)
    return HttpResponse(json_data, content_type= 'application/json')

def register(request):

    data= {'resultado':'False'}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')
