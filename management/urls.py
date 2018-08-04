from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

app_name = 'management'

urlpatterns = [
    url(r'^buildings/$', views.buildings, name='buildings'),
    url(r'^buildings/(?P<id>\d+)', views.building, name='building'),
    url(r'^buildings/new/$', views.new_building, name='new_building'),
]