from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Museum(models.Model):
    MUSEUM_TYPE_CHOICE = [
        ("art", "Art Museum"),
        ("natural history", "Natural History Museum"),
        ("maritime", "Maritime Museum"),
        ("military", "Military Museum"),
        ("science", "Science Museum"),
        ("transport", "Transport Museum"),
        ("history", "History Museum"),
        ("technology", "Technology Museum")
    ]

    #basic information
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    #geographic data
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(srid=4326, null=True, blank=True, spatial_index=True,)
    elevation = models.IntegerField(null=True, blank=True)

    #other information
    visitors = models.IntegerField() #annual visitors
    admission = models.FloatField() #price of admission for an adult
    established = models.IntegerField() #year of establishment
    museum_type = models.CharField(max_length=30, choices=MUSEUM_TYPE_CHOICE, default='history') #type of museum
    
    time_opened = models.CharField(max_length=5) 
    time_closed = models.CharField(max_length=5) 

    def save(self, *args, **kwargs):
        if self.latitude is not None and self.longitude is not None:
            self.location = Point(float(self.longitude), float(self.latitude), srid=4326)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.city}"

    class Meta:
        db_table = 'museums'
        unique_together = ['name', 'city']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['museum_type']),
            models.Index(fields=['visitors']),
        ]