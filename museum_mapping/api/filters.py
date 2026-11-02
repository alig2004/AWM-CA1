import django_filters
from django_filters import rest_framework as filters
from museums.models import Museum

class MuseumFilter(filters.FilterSet):
    # visitors filters
    visitors_min = filters.NumberFilter(field_name="visitors", lookup_expr='gte')
    visitors_max = filters.NumberFilter(field_name="visitors", lookup_expr='lte')
    visitors_range = filters.RangeFilter(field_name="visitors")

    # admission filters
    admission_min = filters.NumberFilter(field_name="admission", lookup_expr='gte')
    admission_max = filters.NumberFilter(field_name="admission", lookup_expr='lte')
    #unemployment_max = filters.NumberFilter(field_name="unemployment_rate", lookup_expr='lte')

    # established filters
    established_min = filters.NumberFilter(field_name="established", lookup_expr='gte')
    established_max = filters.NumberFilter(field_name="established", lookup_expr='lte')

    # Geographic filters
    city = filters.CharFilter(lookup_expr='icontains')
    country = filters.CharFilter(lookup_expr='icontains')

    # Multiple choice filters
    museum_type = filters.MultipleChoiceFilter(choices=Museum._meta.get_field('museum_type').choices)

    # Custom method filters
    large_museums = filters.BooleanFilter(method='filter_large_museums')
    free = filters.BooleanFilter(method='filter_free_museums')

    class Meta:
        model = Museum
        fields = {
            'name': ['icontains', 'istartswith'],
            'elevation': ['gte', 'lte'],
        }

    def filter_large_museums(self, queryset, name, value):
        """Filter for museums with visitors > 150,000 """
        if value:
            return queryset.filter(visitors__gte=150000)
        return queryset

    def filter_free_museums(self, queryset, name, value):
        """Filter for museums with admission = 0 """
        if value:
            return queryset.filter(admission__lte=0.0)
        return queryset