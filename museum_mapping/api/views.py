from rest_framework import viewsets, status
from rest_framework.decorators import action 
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Count, Avg, Min, Max, Sum

from museums.models import Museum
from .serializers import MuseumSerializer

class MuseumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Museum.objects.all()
    serializer_class = MuseumSerializer
    pagination_class = None 

    def get_queryset(self):
        queryset = Museum.objects.all()