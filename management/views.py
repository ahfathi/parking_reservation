# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Building, Floor, Segment, Slot
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import json
import hashlib

# Create your views here.

def index(request):
    return render(request, 'index.html')

def buildings(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('users:login'))
    buildings = Building.objects.all()
    context = {'buildings': buildings}
    return render(request, 'management/buildings.html', context)

def building(request, id):
    building = Building.objects.get(pk=id)
    return render(request, 'management/building.html', {'building': building})

@csrf_exempt
def new_building(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('users:login'))
    if request.method != 'POST':
        return render(request, 'management/new_building.html')
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
        response = "HTTP/1.1 201 CREATED\r\n\r\nRedirectionUrl: {}".format(reverse('management:buildings'))
        return HttpResponse(response) #created
    except Exception as e:
        print(e)
        response = "HTTP/1.1 400 BAD REQUEST\r\n\r\n<h1>Bad Request</h1>"
        return HttpResponse(response) #bad request