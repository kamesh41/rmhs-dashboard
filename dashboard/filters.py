import django_filters
from django import forms
from .models import Operation, AREA_CHOICES, SHIFT_CHOICES, OPERATION_TYPES
from django.db.models import Q
from django.utils import timezone

# Create a new list with "All Areas" option
AREA_CHOICES_WITH_ALL = [('', 'All Areas')] + list(AREA_CHOICES)
SHIFT_CHOICES_WITH_ALL = [('', 'All Shifts')] + list(SHIFT_CHOICES)

class OperationFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        lookup_expr='exact'
    )
    date_from = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        field_name='date',
        lookup_expr='gte'
    )
    date_to = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        field_name='date',
        lookup_expr='lte'
    )
    shift = django_filters.ChoiceFilter(choices=SHIFT_CHOICES_WITH_ALL, widget=forms.Select(attrs={'class': 'form-control'}))
    area = django_filters.ChoiceFilter(choices=AREA_CHOICES_WITH_ALL, widget=forms.Select(attrs={'class': 'form-control'}))
    operation_type = django_filters.ChoiceFilter(
        choices=[('', 'All Types')] + list(OPERATION_TYPES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Operation
        fields = ['date', 'date_from', 'date_to', 'shift', 'area', 'operation_type'] 