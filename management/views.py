# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Building, Floor, Segment, Slot
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import hashlib

# Create your views here.

def staff_reqired(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.is_staff:
            return HttpResponseRedirect(reverse('users:login'))
        return func(*args, **kwargs)
    return wrapper

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def buildings(request):
    buildings = Building.objects.all()
    context = {'buildings': buildings}
    return render(request, 'management/buildings.html', context)

@staff_reqired
def building(request, id):
    building = Building.objects.get(pk=id)
    return render(request, 'management/building.html', {'building': building})

@csrf_exempt
@staff_reqired
def new_building(request):
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
        response_json = {'redirect_url': reverse('management:buildings')}
        print(json.dumps(response_json))
        return HttpResponse(json.dumps(response_json), status=201) #201 created
    except Exception as e:
        print(e)
        return HttpResponse(status=400) #400 bad request

@staff_reqired
def delete_building(request, id):
    try:
        Building.objects.get(pk=id).delete()
    finally:
        return HttpResponseRedirect(reverse('management:buildings'))