from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from management.models import Slot
from reservations.models import Reservation
from parking.settings import SECRET_KEY
from datetime import datetime
import json
import jwt

@login_required
@csrf_exempt
def view(request, slot_id):
    if request.method != 'POST':
        slot = Slot.objects.get(pk=slot_id)
        return render(request, 'reserve.html', {'slot': slot})
    content = request.body.decode()
    try:
        data = json.loads(content)
    except ValueError as e:
        json_response = {'error_message': 'invalid json'}
        print(e, json_response)
        return HttpResponse(json.dumps(json_response), status=400) #400 bad request
    try:
        start = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
        end = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M')
    except ValueError as e:
        json_response = {'error_message': 'invalid time format'}
        pritn(e, json_response)
        return HttpResponse(json.dumps(json_response), status=400) #400 bad request
    now = datetime.now()
    if now >= start:
        response_json = {'error_message': 'invalid input; start time must be set for later'}
        return HttpResponse(json.dumps(response_json), status=400)
    if start >= end:
        response_json = {'error_message': 'invalid input; start time must be smaller than end time'}
        return HttpResponse(json.dumps(response_json), status=400)
    try:
        reserved_slot = Slot.objects.get(pk=int(data['slot_id']))
    except Slot.DoesNotExist as e:
        json_response = {'error_message': 'slot does not exist'}
        print(e, json_response)
        return HttpResponse(json.dumps(response_json), status=400) #400 bad request
    if reserved_slot.disabled:
        json_response = {'error_message': 'slot is disabled'}
        print(json_response)
        return HttpResponse(json.dumps(response_json), status=403) #403 forbidden
    reservations = Reservation.objects.filter(expired=False, slot=reserved_slot)
    now = datetime.now()
    for r in reservations:
        if now >= r.end_time:
            r.expired = True
            r.save()
            continue
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
        'redirect_url': reverse('front_view:building', args=[reserved_slot.segment.floor.building.id]),
        'jwt_token': token,
    }
    return HttpResponse(json.dumps(response_json), status=201) #201 created
