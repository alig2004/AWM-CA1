from django.shortcuts import render
from django.db.models import Avg, Count, Max, Min, Sum

from museums.models import Museum

def index(request):
    #main dashboard view
    context = {
        'total_museums': Museum.objects.count(),
        'total_cities': Museum.objects.values_list('city', flat=True).distinct().order_by('city'),
        'total_countries': Museum.objects.values_list('country', flat=True).distinct().order_by('country'),
        'museum_types': [choice[0] for choice in Museum._meta.get_field('museum_type')],
    }
    
    return render(request, 'dashboard/index.html', context)

"""
#will fill this in if theres enough time to look into doing an analytics page
def analytics(request):
    #analytics page with stats
    museum_queryset = Museum.objects.all()

    museum_stats = {
        'total_museums': ...,
        'total_vistors': ...,
        'avg_visitors': ...,
        'max_visitors': ...,
        'min_visitors': ..., 
    }

    context = {
        'museum_stats': museum_stats,
    }

    return render(request, 'dashboard/analytics.html', context)
"""