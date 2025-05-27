from django import forms
from .models import Farm, Surveillance, Pest, EntryExitLog
from django.utils.safestring import mark_safe
from django.db.models import Q

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

class PestForm(forms.ModelForm):
    reference_pest_id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'min': '8'
        }),
        help_text="Use 8 or above (IDs 1-7 are reserved for system pests). Leave empty if not needed."
    )
    
    class Meta:
        model = Pest
        fields = ['name', 'description', 'reference_pest_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            # reference_pest_id widget is defined above
        }
        
    def clean_reference_pest_id(self):
        reference_pest_id = self.cleaned_data.get('reference_pest_id')
        if reference_pest_id is not None:
            if 1 <= reference_pest_id <= 7:
                raise forms.ValidationError("Reference pest IDs 1-7 are reserved for system pests. Please use 8 or higher, or leave empty.")
        return reference_pest_id
    

class SurveillanceForm(forms.ModelForm):
    class Meta:
        model = Surveillance
        fields = [
            'farm', 'date_observed', 'time_observed',  
            'plants_inspected', 'plant_part', 'pest', 'severity',
            'pest_count','weather_conditions','notes'
        ]
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),  
            'date_observed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_observed': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'plants_inspected': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'plant_part': forms.Select(attrs={'class': 'form-control'}),  
            'pest': forms.Select(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'pest_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'weather_conditions': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only show farms owned by the user
            self.fields['farm'].queryset = Farm.objects.filter(owner=user)
            # Show ALL pests: system pests (1-7) AND user-created pests
            self.fields['pest'].queryset = Pest.objects.all().order_by('reference_pest_id', 'name')


class SurveillanceFilterForm(forms.Form):
    pest = forms.ModelChoiceField(queryset=Pest.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    farm = forms.ModelChoiceField(queryset=Farm.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    severity = forms.ChoiceField(
        choices=[('', 'All'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['farm'].queryset = Farm.objects.filter(owner=user)
            self.fields['pest'].queryset = Pest.objects.filter(reference_pest_id__in=[1, 2, 3, 4, 5, 6, 7])
            self.fields['pest'].label = mark_safe('Pest <a href="/pests/info/" target="_blank" class="ms-2">(More Info)</a>')

class EntryExitLogForm(forms.ModelForm):
    class Meta:
        model = EntryExitLog
        fields = ['farm', 'company_name', 'person_name', 'purpose', 'date', 'time', 'remarks']
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['farm'].queryset = Farm.objects.filter(owner=user)
