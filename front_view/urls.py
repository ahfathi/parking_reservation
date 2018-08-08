from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

app_name = 'front_view'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^buildings/$', views.buildings, name='buildings'),
    url(r'^buildings/(?P<id>\d+)/$', views.building, name='building'),
    url(r'^buildings/delete/(?P<id>\d+)/$', views.delete_building, name='delete_building'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^my_reservations/$', views.my_reservations, name='my_reservations'),
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
]