"This module redirect the request to the specified location"

from django.urls import path, re_path
from main import views

urlpatterns = [
      path('', views.index, name='index'),
      re_path(r'^countdown/(?P<time>.+)$', views.countdown, name='countdown'),
      re_path(r'^timer/(?P<uri>[a-zA-Z0-9]{6})/$', views.timer, name='timer'),
      path('*', views.error, name='error'),
]
