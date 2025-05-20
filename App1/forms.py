from django import forms
from .models import Farm, Pest, Surveillance

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location']  # Excluding owner as it will be set automatically
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PestForm(forms.ModelForm):
    class Meta:
        model = Pest
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class SurveillanceForm(forms.ModelForm):
    class Meta:
        model = Surveillance
        fields = ['farm', 'pest', 'date_observed', 'severity', 'notes']
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),
            'pest': forms.Select(attrs={'class': 'form-control'}),
            'date_observed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SurveillanceForm, self).__init__(*args, **kwargs)
        
        # Filter farms to show only those owned by the current user
        if user:
            self.fields['farm'].queryset = Farm.objects.filter(owner=user)

"""
Key changes:

Specified individual fields instead of using __all__ to have more control
Added form widgets with CSS classes for better styling
For the SurveillanceForm, added a custom __init__ method that filters the farm queryset to only show farms owned by the current user
Added a date input widget to properly render the date_observed field
The FarmForm doesn't include the owner field as we'll set it automatically in the view

"""