from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import string
import json
import os
import secrets
import math

def generate_random_string(length=3):
    return secrets.token_hex(length)



@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uri = generate_random_string()
        data_to_write = [uri, data['timestamp'], data['title']]

        if not os.path.exists('data.json'):
            with open('data.json', 'w') as f:
                  json.dump({}, f)

        with open("data.json", 'r+') as f:
            json_data = json.load(f)
            print(json_data, type(json_data))
            json_data[uri] = data_to_write

            f.seek(0)
            json.dump(json_data, f)
            f.truncate()

        return JsonResponse({"uri": uri})

    response = render(request, 'main/index.html')
    return response

def countdown(request,time):
    context = { "time" : time }
    response = render(request,'main/countdownexpire.html', context)
    return response

def timer(request,uri):
      status = False
      timestamp_title = 'Title'
      existing_timestamp_in_sec = 0
      current_timestamp_in_sec = math.floor(datetime.now().timestamp())

      with open('data.json','r') as f:
            try :
                  data = json.load(f)
                  existing_timestamp_in_sec = data[uri][1]
                  timestamp_title = data[uri][2]
                  status = True
            except:
                  return render(request, 'main/error.html')

      timeResponse =  existing_timestamp_in_sec - current_timestamp_in_sec
      context = { "time" : 0, 'title': timestamp_title, 'status': status }
      if (timeResponse > 0):
            context['time'] = timeResponse
      print(f'--------{context}---------')
      response = render(request,'main/countdownexpire.html', context)
      return response