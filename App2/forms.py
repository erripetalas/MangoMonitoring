from django import forms
from .models import Farm, PlantLocation, Surveillance, Pest

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'total_plants', 'farm_size']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'total_plants': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'farm_size': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
        }

class PlantLocationForm(forms.ModelForm):
    class Meta:
        model = PlantLocation
        fields = ['name', 'description', 'number_of_plants']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'number_of_plants': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class PestForm(forms.ModelForm):
    class Meta:
        model = Pest
        fields = ['name', 'description', 'reference_pest_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'reference_pest_id': forms.NumberInput(attrs={'class': 'form-control', 'required': False}),
        }

class SurveillanceForm(forms.ModelForm):
    class Meta:
        model = Surveillance
        fields = [
            'farm', 'location', 'date_observed', 'time_observed',
            'plants_inspected', 'plant_part', 'pest', 'severity',
            'pest_count','weather_conditions','notes'
        ]
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'date_observed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_observed': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'plants_inspected': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'plant_part': forms.Select(attrs={'class': 'form-control'}),
            'pest': forms.Select(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'pest_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'weather_conditions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Sunny, Rainy, Humid'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only show farms owned by the user
            self.fields['farm'].queryset = Farm.objects.filter(owner=user)
            # Only show pests created by the user
            self.fields['pest'].queryset = Pest.objects.filter(created_by=user)
            # Update location choices based on selected farm
            if self.is_bound and 'farm' in self.data:
                try:
                    farm_id = int(self.data.get('farm'))
                    self.fields['location'].queryset = PlantLocation.objects.filter(farm_id=farm_id)
                except (ValueError, TypeError):
                    self.fields['location'].queryset = PlantLocation.objects.none()
            elif self.instance.pk:
                self.fields['location'].queryset = self.instance.farm.locations.all()
            else:
                self.fields['location'].queryset = PlantLocation.objects.none()