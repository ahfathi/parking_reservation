from django.contrib import admin
from .models import Slot, Segment, Floor, Building
import csv

# Register your models here.

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('label', 'segment', 'floor', 'building')
    list_display_links = ('label', 'segment', 'floor', 'building')
    list_filter = ('segment__floor__building', 'segment__floor', 'segment', 'label')
    actions = ['download_csv']

    def download_csv(self, request, queryset):
        pass
    download_csv.short_description = 'Download Selected as CSV'

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ('label', 'floor', 'building')
    list_display_links = ('label', 'floor', 'building')
    list_filter = ('floor__building', 'floor', 'label')

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('label', 'building')
    list_display_links = ('label', 'building')
    list_filter = ('building', 'label')

admin.site.register(Building)