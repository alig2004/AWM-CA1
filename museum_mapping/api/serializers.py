from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from museums.models import Museum

class MuseumSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Museum
        geo_field = 'location'
        fields = [
            'name',
            'city',
            'country',
            'latitude',
            'longitude',
            'location',
            'elevation',
            'visitors',
            'admission',
            'established',
            'museum_type',
            #'days_closed',
        ]