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

@csrf_exempt
def new_building(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('users:login'))
    if request.method != 'POST':
        return HttpResponse('new_building')
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