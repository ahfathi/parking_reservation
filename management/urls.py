from django.conf.urls import url
from . import views

app_name = 'management'

urlpatterns = [
    url(r'^new-building$', views.new_building, name='new_building'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
]