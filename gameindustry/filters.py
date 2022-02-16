import django_filters
from matplotlib.pyplot import title
from .models import *

"""Imports all from gameindustry.models"""

class OfferFilter(django_filters.FilterSet):
    """lookup_expr: Behaves as WHERE clause in SQL. """
    """icontains: case insensitive containment test. Checks on the database if information stored contains the string passed into the form rather than exact match. SQL equivalent is "ILIKE"  """
    """label: Used to specify how fields should be displayed on the form/filter"""
    """field_name: directs to the name of the model field filtered against."""
    titleF = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    employerF = django_filters.CharFilter(field_name='employer', lookup_expr='icontains', label='Company')
    locationF = django_filters.CharFilter(field_name='location', lookup_expr='icontains', label='Location')
    experienceF = django_filters.CharFilter(field_name='experience', lookup_expr='icontains', label='Experience')
    requirementsF = django_filters.CharFilter(field_name='requirements', lookup_expr='icontains', label='Requirements')
    
    class Meta:
        model = Offer
        fields = ['titleF', 'employerF', 'locationF', 'experienceF', 'requirementsF']
        
