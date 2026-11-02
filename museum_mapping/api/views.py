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
    pagination_class = None  # Disable pagination for clean GeoJSON

    def get_queryset(self):
        queryset = Museum.objects.all()

        # visitors filters
        visitors_min = self.request.query_params.get('visitors_min')
        visitors_max = self.request.query_params.get('visitors_max')

        if visitors_min:
            queryset = queryset.filter(visitors__gte=visitors_min)
        if visitors_max:
            queryset = queryset.filter(visitors__lte=visitors_max)

        # Category filters
        city = self.request.query_params.get('city')
        museum_type = self.request.query_params.get('museum_type')

        if city:
            queryset = queryset.filter(city=city)
        if museum_type:
            queryset = queryset.filter(museum_type=museum_type)

        return queryset

    def list(self, request, *args, **kwargs):
        """Override list to return proper GeoJSON FeatureCollection"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get comprehensive cities statistics"""
        queryset = self.get_queryset()

        stats = {
            'total_museums': queryset.count(),
            'total_visitors': queryset.aggregate(Sum('visitors'))['visitors__sum'] or 0,
            'visitor_stats': {
                'min': queryset.aggregate(Min('visitors'))['visitors__min'] or 0,
                'max': queryset.aggregate(Max('visitors'))['visitors__max'] or 0,
                'avg': int(queryset.aggregate(Avg('visitors'))['visitors__avg'] or 0),
            },
            'cities_count': queryset.values('city').distinct().count(),
            'museum_types_distribution': dict(
                queryset.values('museum_type')
                .annotate(count=Count('id'))
                .values_list('museum_type', 'count')
            ),
        }

        return Response(stats)

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Find cities near a point"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        distance_km = request.query_params.get('distance', 50)

        if not lat or not lng:
            return Response(
                {'error': 'lat and lng parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            point = Point(float(lng), float(lat), srid=4326)
            distance_m = float(distance_km) * 1000

            nearby_museums = Museum.objects.filter(
                location__distance_lte=(point, distance_m)
            ).annotate(
                distance=Distance('location', point)
            ).order_by('distance')[1:11]

            serializer = self.get_serializer(nearby_museums, many=True)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid coordinates or distance'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def within_bounds(self, request):
        """Find cities within bounding box"""
        data = request.data
        required_fields = ['west', 'south', 'east', 'north']

        if not all(field in data for field in required_fields):
            return Response(
                {'error': f'Required fields: {required_fields}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            west, south, east, north = [float(data[field]) for field in required_fields]

            museums_in_bounds = Museum.objects.filter(
                latitude__gte=south,
                latitude__lte=north,
                longitude__gte=west,
                longitude__lte=east
            )

            serializer = self.get_serializer(museums_in_bounds, many=True)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid bounding box coordinates'},
                status=status.HTTP_400_BAD_REQUEST
            )