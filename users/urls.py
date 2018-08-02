from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

app_name = 'users'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]