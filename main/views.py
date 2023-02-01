"""This module contains the views functions """

import json
import secrets
import math
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main import models

def generate_random_string(length=3):
    """This will generate the Random String for URL"""
    return secrets.token_hex(length)


@csrf_exempt
def index(request):
    """Return the index page"""

    if request.method == 'POST':
        data = json.loads(request.body)
        uri = generate_random_string()

        countdown_info = models.CountdownInfo(title=data['title'], timestamp=data['timestamp'],
        uri=uri)
        countdown_info.save()

        return JsonResponse({"uri": uri})

    response = render(request, 'main/index.html')
    return response

def countdown(request,time):
    """This function will render a countdown template with countdown [endpoint : /countdown/56]"""
    context = { "time" : time }
    response = render(request,'main/countdownexpire.html', context)
    return response

def timer(request,uri):
    """Set timer function and store to database [endpoint : /timer/rQWAsa]"""
    status = False
    timestamp_title = 'Title'
    existing_timestamp_in_sec = 0
    current_timestamp_in_sec = math.floor(datetime.now().timestamp())

    countdown_info =  models.CountdownInfo.objects.get(uri=uri)
    if countdown_info:
        existing_timestamp_in_sec = int(countdown_info.timestamp)
        timestamp_title = countdown_info.title
        status = True

    time_response =  existing_timestamp_in_sec - current_timestamp_in_sec
    context = { "time" : 0, 'title': timestamp_title, 'status': status }

    if time_response > 0 :
        context['time'] = time_response
    response = render(request,'main/countdownexpire.html', context)
    return response

def error(request):
    """Returns a Error Page"""
    context = {}
    response = render(request,'main/error.html', context)
    return response
