from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

app_name = 'management'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', login, {'template_name': 'management/login.html'}, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^buildings/$', views.buildings, name='buildings'),
    url(r'^buildings/new/$', views.new_building, name='new_building'),
]