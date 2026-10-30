import django_filters
from django_filters import rest_framework as filters
from museums.models import Museum

class MuseumFilter(filters.FilterSet):
    #filter by city
    city = filters.CharFilter(field_name="city", lookup_expr="icontains") #getting museums by city

    #filter by country
    country = filters.CharFilter(field_name="country", lookup_expr="icontains") #getting museums by country

    #filter by visitors
    visitors_min = filters.NumberFilter(field_name="visitors", lookup_expr="gte") #getting lowest attendance
    visitors_max = filters.NumberFilter(field_name="visitors", lookup_expr="lte") #getting highest attendance
    visitors_range = filters.RangeFilter(field_name="visitors") #getting ranges of attendance 

    #filter by admission
    admission_min = filters.NumberFilter(field_name="admission", lookup_expr="gte") #getting highest admission
    admission_max = filters.NumberFilter(field_name="admission", lookup_expr="lte") #getting lowest admission
    admission = filters.NumberFilter(field_name="admission", lookup_expr="exact") #getting museums with specific admission price
    cheaper_than = filters.BooleanFilter(method="filter_cheaper_than") #filter by admission below a certain number

    #filter by establishment year
    established = filters.NumberFilter(field_name="established", lookup_expr="exact") #getting museums established in a specific year
    established_old = filters.NumberFilter(field_name="established", lookup_expr="lte") #getting oldest established museums
    established_new = filters.NumberFilter(field_name="established", lookup_expr="gte") #getting most recently established museums
    older_than = filters.BooleanFilter(method="filter_older_than") #filter by establishment earlier than a certain year
    newer_than = filters.BooleanFilter(method="filter_newer_than") #filter by establishment later than a certain year

    #filter by type
    museum_type = filters.MultipleChoiceFilter(choices=Museum._meta.get_field('muesum_type').choices)

    #filter by days closed/open
    days_closed = filters.MultipleChoiceFilter(choices=Museum._meta.get_field('days_closed').choices)

    class Meta:
        model = Museum
        fields = {
            'name': ['icontains', 'istartswith'],
            'elevation': ['gte', 'lte'],
        }

    def filter_cheaper_than(self, queryset, name, value, price):
        #filters for museums with admission less than the given price
        if value:
            return queryset.filter(admission__lte=price)
        return queryset
    
    def filter_older_than(self, queryset, name, value, year):
        #filters for museums established earlier than the given year
        if value:
            return queryset.filter(established__lte=year)
        return queryset

    def filter_newer_than(self, queryset, name, value, year):
        if value:
            return queryset.filter(established__gte=year)
        return queryset