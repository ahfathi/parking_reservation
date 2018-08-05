from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from .models import LiveReservation
from users.models import UserReservation
from management.models import Slot
from parking.settings import SECRET_KEY
import json
from datetime import datetime
import jwt

# Create your views here.

@login_required
@csrf_exempt
def reserve(request, slot_id):
    if request.method != 'POST':
        slot = Slot.objects.get(pk=slot_id)
        return render(request, 'reservations/reserve.html', {'slot': slot})
    content = request.body.decode()
    try:
        data = json.loads(content)
        start = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
        end = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
        reserved_slot = Slot.objects.get(pk=int(data['slot_id']))
        reservations = LiveReservation.objects.filter(slot=reserved_slot)
        for r in reservations:
            if (start > r.start_time and start < r.end_time) or (end > r.start_time and end < r.end_time):
                response_json = {'error_memssage': 'this time has been taken, please choose another time'}
                return HttpResponse(json.dumps(response_json), status=409) #409 conflict
        reservation = LiveReservation(user=request.user, slot=reserved_slot, start_time=start, end_time=end)
        reservation.save()
        claims = {
            'Building': reserved_slot.segment.floor.building.label,
            'Floor': reserved_slot.segment.floor.label,
            'Segment': reserved_slot.segment.label,
            'Slot': reserved_slot.label,
            'start': data['start_time'],
            'end': data['end_time'],
        }
        token = jwt.encode(claims, SECRET_KEY)
        response_json = {
            'redirect_url': reverse('users:building', args=reserved_slot.segment.floor.building.id),
            'jwt_token': token,
        }
        reservation = UserReservation(jwt_token=token)
        reservation.save()
        return HttpResponse(json.dumps(response_json), status=201) #201 created
    except Exception as e:
        print(e)
        return HttpResponse(status=400) #400 bad request

@login_required
def my_reservations(request):
    reservations = UserReservation.objects.filter(user=request.user).all()
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})

@login_required
def details(request, id):
    reservation = UserReservation.objects.get(pk=id)
    context = {
        'building': reservation.slot.segment.floor.building.label,
        'floor': reservation.slot.segment.floor.label,
        'segment': reservation.slot.segment.label,
        'slot': reservation.slot.label,
        'token': reservation.jwt_token,
    }
    if reservation.user == request.user:
        return render(request, 'reservations/details.html', context)
    else:
        return HttpResponse(status=404) #not found