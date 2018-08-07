from django.conf.urls import url
from .views import reserve, guard

app_name = 'reservations'

urlpatterns = [
    url(r'^reserve/(?P<slot_id>\d+)$', reserve.view, name='reserve'),
    url(r'^guard/$', guard.view, name='guard'),
]