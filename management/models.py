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
        verbose_name_plural = 'buildings'

class Floor(Base):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'floors'

class Segment(Base):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'segments'

class Slot(Base):
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'slots'
