from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from management.views import staff_reqired
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
from .models import Reservation
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
        end = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M')
        now = datetime.now()
        if now >= start:
            response_json = {'error_message': 'invalid input; start time must be set for later'}
            return HttpResponse(json.dumps(response_json))
        if start >= end:
            response_json = {'error_message': 'invalid input; start time must be smaller than end time'}
            return HttpResponse(json.dumps(response_json))
        reserved_slot = Slot.objects.get(pk=int(data['slot_id']))
        reservations = Reservation.objects.filter(slot=reserved_slot)
        now = datetime.now()
        for r in reservations:
            if (start >= r.start_time and start <= r.end_time) or (end >= r.start_time and end <= r.end_time):
                response_json = {'error_message': 'this time has been taken, please choose another time'}
                return HttpResponse(json.dumps(response_json))
        claims = {
            'Building': reserved_slot.segment.floor.building.label,
            'Floor': reserved_slot.segment.floor.label,
            'Segment': reserved_slot.segment.label,
            'Slot': reserved_slot.label,
            'start': data['start_time'],
            'end': data['end_time'],
        }
        token = jwt.encode(claims, SECRET_KEY).decode()
        reservation = Reservation(user=request.user, slot=reserved_slot, start_time=start, end_time=end, jwt_token=token)
        reservation.save()
        response_json = {
            'redirect_url': reverse('management:building', args=[reserved_slot.segment.floor.building.id]),
            'jwt_token': token,
        }
        return HttpResponse(json.dumps(response_json), status=201) #201 created
    except Exception as e:
        print(e)
        return HttpResponse(status=400) #400 bad request

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).all()
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})

@login_required
def details(request, id):
    reservation = Reservation.objects.get(pk=id)
    context = {
        'id': reservation.id,
        'building': reservation.slot.segment.floor.building.label,
        'floor': reservation.slot.segment.floor.label,
        'segment': reservation.slot.segment.label,
        'slot': reservation.slot.label,
        'start': reservation.start_time,
        'end': reservation.end_time,
        'token': reservation.jwt_token,
    }
    if reservation.user == request.user:
        return render(request, 'reservations/details.html', context)
    else:
        return HttpResponse(status=404) #not found

def delete(request, id):
    Reservation.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('reservations:my_reservations'))

@csrf_exempt
@staff_reqired
def guard(request):
    if request.method != 'POST':
        return render(request, 'reservations/guard.html')
    content = json.loads(request.body.decode())
    token = content['jwt_token']
    try:
        claims = jwt.decode(token, SECRET_KEY)
        start = datetime.strptime(claims['start'], '%Y-%m-%dT%H:%M')
        end = datetime.strptime(claims['end'], '%Y-%m-%dT%H:%M')
        now = datetime.now()
        print(now, start)
        if now < start:
            response_json = {'message': 'you are too soon, your reservation time is: {}'.format(claims['start'])}
        elif now > end:
            response_json = {'message': 'you are too late, your reservation has been expired'}
        else:
            response_json = {'message': 'you can pass'}
    except:
        response_json = {'message': 'unauthorized token'}
    finally:
        return HttpResponse(json.dumps(response_json))