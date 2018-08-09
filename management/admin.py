from django.contrib import admin
from .models import Slot, Segment, Floor, Building
from django.http import HttpResponse
import csv
from .pdfgen import DataToPdf

# Register your models here.

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('label', 'segment', 'floor', 'building')
    list_display_links = ('label', 'segment', 'floor', 'building')
    list_filter = ('segment__floor__building', 'segment__floor', 'segment', 'label')
    actions = ['download_csv', 'download_pdf']

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