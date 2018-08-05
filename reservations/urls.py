from django.conf.urls import url
from . import views

app_name = 'reservations'

urlpatterns = [
    url(r'^reserve/(?P<slot_id>\d+)$', views.reserve, name='reserve'),
    url(r'^me/reservations/$', views.my_reservations, name='my_reservations'),
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
]