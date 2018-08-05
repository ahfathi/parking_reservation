from django.db import models
from management.models import Slot
from django.contrib.auth.models import User

# Create your models here.

class LiveReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class Meta:
        verbose_name_plural = 'reservations'