from django.db import models
from django.contrib.auth.models import User
from management.models import Slot

# Create your models here.

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'reservations'