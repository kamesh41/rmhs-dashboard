from django import forms
from crispy_forms.helper import FormHelper
from .models import (
    Material, Destination, Source,
    FeedingOperation, StackingOperation, ReclaimingOperation,
    ReceivingOperation, CrushingOperation, 
    AREA_CHOICES, SHIFT_CHOICES
)
from django.utils import timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class FilterForm(forms.Form):
    """Form for filtering operations in the dashboard"""
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    shift = forms.ChoiceField(
        choices=[('', 'All Shifts')] + list(SHIFT_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    area = forms.ChoiceField(
        choices=[('', 'All Areas')] + list(AREA_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class FeedingOperationForm(forms.ModelForm):
    """Form for adding/editing feeding operations"""
    material_name = forms.CharField(
        label="Material Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    destination_name = forms.CharField(
        label="Destination",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = FeedingOperation
        fields = ['date', 'shift', 'area', 'quantity', 'reported_by', 'remarks']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class StackingOperationForm(forms.ModelForm):
    """Form for adding/editing stacking operations"""
    material_name = forms.CharField(
        label="Material Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    destination_name = forms.CharField(
        label="Destination",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StackingOperation
        fields = ['date', 'shift', 'area', 'quantity', 'reported_by', 'remarks']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ReclaimingOperationForm(forms.ModelForm):
    """Form for adding/editing reclaiming operations"""
    material_name = forms.CharField(
        label="Material Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    source_name = forms.CharField(
        label="Source",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ReclaimingOperation
        fields = ['date', 'shift', 'area', 'quantity', 'reported_by', 'remarks']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ReceivingOperationForm(forms.ModelForm):
    """Form for adding/editing receiving operations"""
    material_name = forms.CharField(
        label="Material Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    source_name = forms.CharField(
        label="Source",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ReceivingOperation
        fields = ['date', 'shift', 'area', 'quantity', 'reported_by', 'remarks']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CrushingOperationForm(forms.ModelForm):
    """Form for adding/editing crushing operations"""
    material_name = forms.CharField(
        label="Material Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CrushingOperation
        fields = ['date', 'shift', 'area', 'quantity', 'crushing_details', 'reported_by', 'remarks']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'crushing_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

