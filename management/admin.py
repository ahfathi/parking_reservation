from django.contrib import admin
from .models import Slot, Segment, Floor, Building

# Register your models here.
admin.site.register(Slot)
admin.site.register(Segment)
admin.site.register(Floor)
admin.site.register(Building)