from django import forms
from .models import Rake, TIPPLER_CHOICES, RAKE_STATUS_CHOICES

class RakeForm(forms.ModelForm):
    """Form for adding/editing rake information"""
    class Meta:
        model = Rake
        fields = [
            'rake_id', 'tippler', 'rake_in_time', 'rake_completed_time',
            'rake_status', 'rake_type', 'rake_material', 'reported_by', 'remarks'
        ]
        widgets = {
            'rake_id': forms.TextInput(attrs={'class': 'form-control'}),
            'tippler': forms.Select(attrs={'class': 'form-select'}),
            'rake_in_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'rake_completed_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'rake_status': forms.Select(attrs={'class': 'form-select'}),
            'rake_type': forms.TextInput(attrs={'class': 'form-control'}),
            'rake_material': forms.TextInput(attrs={'class': 'form-control'}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class RakeFilterForm(forms.Form):
    """Form for filtering rakes in the dashboard"""
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    tippler = forms.ChoiceField(
        choices=[('', 'All Tipplers')] + list(TIPPLER_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + list(RAKE_STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 