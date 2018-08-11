from django.contrib import admin
from .models import Slot, Segment, Floor, Building
from django.http import HttpResponse
import csv
from .pdfgen import DataToPdf

# Register your models here.

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('label', 'segment_label', 'floor_label', 'building_label', 'status')
    list_filter = ('segment__floor__building', 'segment__floor', 'segment', 'label')
    actions = ['download_csv', 'download_pdf', 'disable', 'enable']

    def download_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="slots_table.csv"'
        headers = ['Slot', 'Segment', 'Floor', 'Building']
        writer = csv.DictWriter(response, fieldnames=headers)
        writer.writeheader()
        for slot in queryset:
            writer.writerow({
                'Slot': slot.label,
                'Segment': slot.segment.label,
                'Floor': slot.segment.floor.label,
                'Building': slot.segment.floor.building.label
                })
        return response
    download_csv.short_description = 'Download CSV'

    def download_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="slots_table.pdf"'
        fields = (
            ('slot', 'Slot'),
            ('segment', 'Segment'),
            ('floor', 'Floor'),
            ('building', 'Building'),
        )
        data = []
        for slot in queryset:
            data.append({
                'slot': slot.label,
                'segment': slot.segment.label,
                'floor': slot.segment.floor.label,
                'building': slot.segment.floor.building.label
                })
        doc = DataToPdf(fields, data)
        doc.export(response)
        return response
    download_pdf.short_description = 'Download PDF'

    def disable(self, request, queryset):
        for slot in queryset:
            slot.disabled = True
            slot.save()
    def enable(self, request, queryset):
        for slot in queryset:
            slot.disabled = False
            slot.save()

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ('label', 'floor_label', 'building_label', 'status')
    list_filter = ('floor__building', 'floor', 'label')
    actions = ['disable', 'enable']

    def disable(self, request, queryset):
        for segment in queryset:
            segment.disabled = True
            segment.save()
    def enable(self, request, queryset):
        for segment in queryset:
            segment.disabled = False
            segment.save()

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('label', 'building_label', 'status')
    list_filter = ('building', 'label')
    actions = ['disable', 'enable']

    def disable(self, request, queryset):
        for floor in queryset:
            floor.disabled = True
            floor.save()
    def enable(self, request, queryset):
        for floor in queryset:
            floor.disabled = False
            floor.save()

admin.site.register(Building)