from django.db import models

# Create your models here.

class Base(models.Model):
    label = models.CharField(max_length=32)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __str__(self):
        return self.label    

class Building(Base):
    #location
    class Meta:
        unique_together = (('label',),)
class Floor(Base):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('label', 'building'),)

class Segment(Base):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    def building(self):
        return self.floor.building
    building.admin_order_field = 'floor__building'
    class Meta:
        unique_together = (('label', 'floor'),)
    
class Slot(Base):
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    def floor(self):
        return self.segment.floor
    def building(self):
        return self.floor().building
    building.admin_order_field = 'segment__floor__building'
    floor.admin_order_field = 'segment__floor'
    class Meta:
        unique_together = (('label', 'segment'),)
