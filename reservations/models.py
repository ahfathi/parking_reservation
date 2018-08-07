from django.db import models
from management.models import Slot
from django.contrib.auth.models import User

# Create your models here.

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    jwt_token = models.TextField()
    expired = models.BooleanField(default=False)
    class Meta:
        indexes = [
            models.Index(fields=['expired', 'slot']),
            models.Index(fields=['user']),
        ]