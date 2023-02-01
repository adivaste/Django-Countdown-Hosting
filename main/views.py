"""This module contains the views functions """

import json
import os
import secrets
import math
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def generate_random_string(length=3):
    """This will generate the Random String for URL"""
    return secrets.token_hex(length)


@csrf_exempt
def index(request):
    """Return the index page"""

    if request.method == 'POST':
        data = json.loads(request.body)
        uri = generate_random_string()
        data_to_write = [uri, data['timestamp'], data['title']]

        if not os.path.exists('data.json'):
            with open('data.json', 'w', encoding="UTF-8") as file:
                json.dump({}, file)

        with open("data.json", 'r+', encoding="UTF-8") as file:
            json_data = json.load(file)
            json_data[uri] = data_to_write

            file.seek(0)
            json.dump(json_data, file)
            file.truncate()

        return JsonResponse({"uri": uri})

    response = render(request, 'main/index.html')
    return response

def countdown(request,time):
    """This function will render a countdown template with countdown"""
    context = { "time" : time }
    response = render(request,'main/countdownexpire.html', context)
    return response

def timer(request,uri):
    """Set timer function and store to database"""
    status = False
    timestamp_title = 'Title'
    existing_timestamp_in_sec = 0
    current_timestamp_in_sec = math.floor(datetime.now().timestamp())

    with open('data.json','r', encoding="UTF-8") as file:
        try :
            data = json.load(file)
            existing_timestamp_in_sec = data[uri][1]
            timestamp_title = data[uri][2]
            status = True
        except :
            return render(request, 'main/error.html')

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
