from django.conf.urls import url
from .views import new_building

app_name = 'management'

urlpatterns = [
    url(r'^new_building/$', new_building.view, name='new_building'),
]