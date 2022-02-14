import django_filters
from matplotlib.pyplot import title
from .models import *

class OfferFilter(django_filters.FilterSet):
    titleF = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    employerF = django_filters.CharFilter(field_name='employer', lookup_expr='icontains', label='Company')
    locationF = django_filters.CharFilter(field_name='location', lookup_expr='icontains', label='Location')
    experienceF = django_filters.CharFilter(field_name='experience', lookup_expr='icontains', label='Experience')
    requirementsF = django_filters.CharFilter(field_name='requirements', lookup_expr='icontains', label='Requirements')
    
    class Meta:
        model = Offer
        fields = ['titleF', 'employerF', 'locationF', 'experienceF', 'requirementsF']
        
