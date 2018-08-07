from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from management.models import Building, Floor, Segment, Slot
from django.urls import reverse
from django.http import HttpResponse
from parking.decorators import staff_required
import json

@csrf_exempt
@staff_required
def view(request):
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
        response_json = {'redirect_url': reverse('front_view:buildings')}
        print(json.dumps(response_json))
        return HttpResponse(json.dumps(response_json), status=201) #201 created
    except Exception as e:
        print(e)
        return HttpResponse(status=400,content_type="application/json") #400 bad request