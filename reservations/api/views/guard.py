from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from parking.decorators import staff_required
from parking.settings import SECRET_KEY
from datetime import datetime
import json
import jwt

@csrf_exempt
@staff_required
def view(request):
    if request.method != 'POST':
        return render(request, 'guard.html')
    content = json.loads(request.body.decode())
    try:
        token = content['jwt_token']
    except ValueError as e:
        json_response = {'error_message': 'invalid json'}
        print(e, json_response)
        return HttpResponse(json.dumps(json_response), status=400) #400 bad request
    try:
        claims = jwt.decode(token, SECRET_KEY)
        start = datetime.strptime(claims['start'], '%Y-%m-%dT%H:%M')
        end = datetime.strptime(claims['end'], '%Y-%m-%dT%H:%M')
        now = datetime.now()
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