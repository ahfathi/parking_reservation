from django.db import models
from django.urls import reverse
from django.utils.html import format_html

# Create your models here.

class Base(models.Model):
    label = models.CharField(max_length=32)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default=False)
    class Meta:
        abstract = True
    def __str__(self):
        return self.label
    def status(self):
        if self.disabled:
            text = format_html('<span style="color:red">disabled</span>')
        else:
            text = format_html('<span style="color:green">enabled</span>')
        return text

class Building(Base):
    #location
    class Meta:
        unique_together = (('label',),)
class Floor(Base):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    def building_label(self):
        url = reverse('admin:management_building_change', args=[self.building.id])
        return format_html("<a href={}>{}</a>", url, self.building.label)
    building_label.admin_order_field = 'building'
    class Meta:
        unique_together = (('label', 'building'),)

class Segment(Base):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    def floor_label(self):
        url = reverse('admin:management_floor_change', args=[self.floor.id])
        return format_html("<a href={}>{}</a>", url, self.floor.label)
    def building_label(self):
        url = reverse('admin:management_building_change', args=[self.floor.building.id])
        return format_html("<a href={}>{}</a>", url, self.floor.building.label)
    building_label.admin_order_field = 'floor__building'
    floor_label.admin_order_field = 'floor'
    class Meta:
        unique_together = (('label', 'floor'),)
    
class Slot(Base):
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    def segment_label(self):
        url = reverse('admin:management_segment_change', args=[self.segment.id])
        return format_html("<a href={}>{}</a>", url, self.segment.label)
    def floor_label(self):
        url = reverse('admin:management_floor_change', args=[self.segment.floor.id])
        return format_html("<a href={}>{}</a>", url, self.segment.floor.label)
    def building_label(self):
        url = reverse('admin:management_building_change', args=[self.segment.floor.building.id])
        return format_html("<a href={}>{}</a>", url, self.segment.floor.building.label)
    building_label.admin_order_field = 'segment__floor__building'
    floor_label.admin_order_field = 'segment__floor'
    segment_label.admin_order_field = 'segment'
    class Meta:
        unique_together = (('label', 'segment'),)
