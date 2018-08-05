from django.db import models
from reservations.models import LiveReservation

# Create your models here.

class UserReservation(LiveReservation):
    jwt_token = models.TextField();