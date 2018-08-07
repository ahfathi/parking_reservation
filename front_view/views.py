# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from management.models import Building
from reservations.models import Reservation
from parking.decorators import staff_required
# Create your views here.

def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('front_view:index'))

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('front_view:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)

@login_required
def buildings(request):
    buildings = Building.objects.all()
    context = {'buildings': buildings}
    return render(request, 'management/buildings.html', context)

@staff_required
def building(request, id):
    building = Building.objects.get(pk=id)
    return render(request, 'management/building.html', {'building': building})

@staff_required
def delete_building(request, id):
    try:
        Building.objects.get(pk=id).delete()
    finally:
        return HttpResponseRedirect(reverse('front_view:buildings'))

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
