# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Building, Floor, Segment, Slot
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
import json
import hashlib

# Create your views here.

# @csrf_exempt
# def register(request):
#     if request.method != 'POST':
#         return HttpResponse(status=405) #method not allowed
#     content = request.body.decode()
#     response = json.loads(content)
#     try:
#         user_name = response['username']
#         password = response['password']
#     except:
#         return HttpResponse(status=400) #bad request
#     hsh = hashlib.md5(password.encode()).hexdigest()
#     user = User(username=user_name, password=hsh)
#     user.save()
#     return HttpResponse(status=201) #created

# @csrf_exempt
# def login(request):
#     if request.method != 'POST':
#         return HttpResponse(status=405) #method not allowed
#     content = request.body.decode()
#     response = json.loads(content)
#     try:
#         user_name = response['username']
#         password = response['password']
#     except:
#         return HttpResponse(status=400) #bad request
#     try:
#         user = User.objects.get(username=user_name)
#     except:
#         return HttpResponse(status=401) #unauthorized
#     hsh = hashlib.md5(password.encode()).hexdigest()
#     if hsh == user.password:
#         pass #make jwt for a user
#     else:
#         return HttpResponse(status=401) #unauthorized

def logout_view(request):
    logout(request)
    return HttpResponse(reverse('management:index.html'))

def index(request):
    return render(request, 'management/index.html')

def buildings(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('management:login'))
    buildings = Building.objects.all()
    context = {'buildings': buildings}
    return render(request, 'management/buildings.html', context)

@csrf_exempt
def new_building(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('management:login'))
    if request.method != 'POST':
        return HttpResponse(status=405) #method not allowed
    content = request.body.decode()
    try:
        building = json.loads(content)
        b = Building(label=building['label'])
        b.save()
        for floor in building['floors']:
            f = Floor(label=floor['label'], building=b)
            f.save()
            for segment in floor['segments']:
                se = Segment(label=segment['label'], floor=f)
                se.save()
                for slot in segment['slots']:
                    sl = Slot(label=slot, segment=se)
                    sl.save()
        return HttpResponse(status=201) #created
    except Exception as e:
        print(e)
        return HttpResponse(status=400) #bad request