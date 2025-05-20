from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from App1.pests import get_pests_diseases
from django import template
from .models import Farm, Pest, Surveillance
from .forms import FarmForm, PestForm, SurveillanceForm

def home(request):
    """View for the home/landing page"""
    return render(request, "App1/index.html", {
        "title": "Home - Mango Monitoring",
    })


def project_list(request): 
    """View for the project list page showing all pests/diseases"""
    try:
        pests_diseases = get_pests_diseases()
        return render(request, "App1/projectlist.html", {
            "title": "Pests & Diseases - Mango Monitoring",
            "pests_diseases": pests_diseases
        })
    except Exception as e:
        # Log error in production: logger.error(f"Error fetching pests: {e}")
        return render(request, "App1/error.html", {
            "message": "Could not load pest data. Please try again later."
        })

def project_details(request, project_id):
    """View for the project details page showing specific pest/disease info"""
    try:
        pests_diseases = get_pests_diseases()
        project = next((p for p in pests_diseases if p.id == int(project_id)), None)
        
        if not project:
            raise Http404(f"Pest/Disease with ID {project_id} not found")
            
        # Prepare description if it's not already a dictionary
        if not isinstance(project.description, dict):
            project.description = {
                "general": project.description,
            }
    
        excluded_keys = ['general', 'eggs', 'immatures', 'adults']
        return render(request, "App1/projectdetails.html", {
            "title": f"{project.name} - Mango Monitoring",
            "project": project,
            "excluded_keys": ["excluded_keys"]  # Add this for template filtering
        })

    except ValueError:
        return redirect('App1:projectlist')
    except Exception as e:
        # Log error in production
        return render(request, "App1/error.html", {
            "message": "An error occurred while loading this page."
        })

def about(request):
    """View for the about page with team information"""
    team_members = [
        {"name": "Erri Petalas", "student_id": "S320775"},
        {"name": "Surendra Phuyal", "student_id": "S372088"},
        {"name": "Rekha Khadka", "student_id": "S372366"},
        {"name": "Dylan Tomlinson", "student_id": "S372936"}, 
    ]
    
    return render(request, "App1/about.html", {
        "title": "About - Mango Monitoring",
        "team_members": team_members
    })

# Farm CRUD Views (Class-based)
class FarmListView(LoginRequiredMixin, ListView):
    model = Farm
    template_name = 'App1/farm_list.html'
    context_object_name = 'farms'
    
    def get_queryset(self):
        # Only show farms owned by the current user
        return Farm.objects.filter(owner=self.request.user)

class FarmDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Farm
    template_name = 'App1/farm_detail.html'
    context_object_name = 'farm'
    
    def test_func(self):
        # Check if the user owns this farm
        farm = self.get_object()
        return farm.owner == self.request.user

class FarmCreateView(LoginRequiredMixin, CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'App1/farm_form.html'
    success_url = reverse_lazy('App1:farm_list')
    
    def form_valid(self, form):
        # Set the owner to the current user before saving
        form.instance.owner = self.request.user
        messages.success(self.request, 'Farm created successfully!')
        return super().form_valid(form)

class FarmUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = 'App1/farm_form.html'
    success_url = reverse_lazy('App1:farm_list')
    
    def test_func(self):
        # Check if the user owns this farm
        farm = self.get_object()
        return farm.owner == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Farm updated successfully!')
        return super().form_valid(form)

class FarmDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Farm
    template_name = 'App1/confirm_delete.html'
    success_url = reverse_lazy('App1:farm_list')
    context_object_name = 'object'
    
    def test_func(self):
        # Check if the user owns this farm
        farm = self.get_object()
        return farm.owner == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Farm deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Pest CRUD Views (Class-based)
class PestListView(LoginRequiredMixin, ListView):
    model = Pest
    template_name = 'App1/pest_list.html'
    context_object_name = 'pests'

class PestDetailView(LoginRequiredMixin, DetailView):
    model = Pest
    template_name = 'App1/pest_detail.html'
    context_object_name = 'pest'

class PestCreateView(LoginRequiredMixin, CreateView):
    model = Pest
    form_class = PestForm
    template_name = 'App1/pest_form.html'
    success_url = reverse_lazy('App1:pest_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Pest created successfully!')
        return super().form_valid(form)

class PestUpdateView(LoginRequiredMixin, UpdateView):
    model = Pest
    form_class = PestForm
    template_name = 'App1/pest_form.html'
    success_url = reverse_lazy('App1:pest_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Pest updated successfully!')
        return super().form_valid(form)

class PestDeleteView(LoginRequiredMixin, DeleteView):
    model = Pest
    template_name = 'App1/confirm_delete.html'
    success_url = reverse_lazy('App1:pest_list')
    context_object_name = 'object'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Pest deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Surveillance CRUD Views (Class-based)
class SurveillanceListView(LoginRequiredMixin, ListView):
    model = Surveillance
    template_name = 'App1/surveillance_list.html'
    context_object_name = 'records'
    
    def get_queryset(self):
        # Only show surveillance records for farms owned by the current user
        return Surveillance.objects.select_related('farm', 'pest').filter(farm__owner=self.request.user)

class SurveillanceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Surveillance
    template_name = 'App1/surveillance_detail.html'
    context_object_name = 'record'
    
    def test_func(self):
        # Check if the user owns the farm associated with this record
        record = self.get_object()
        return record.farm.owner == self.request.user

class SurveillanceCreateView(LoginRequiredMixin, CreateView):
    model = Surveillance
    form_class = SurveillanceForm
    template_name = 'App1/surveillance_form.html'
    success_url = reverse_lazy('App1:surveillance_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Surveillance record created successfully!')
        return super().form_valid(form)

class SurveillanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Surveillance
    form_class = SurveillanceForm
    template_name = 'App1/surveillance_form.html'
    success_url = reverse_lazy('App1:surveillance_list')
    
    def test_func(self):
        # Check if the user owns the farm associated with this record
        record = self.get_object()
        return record.farm.owner == self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Surveillance record updated successfully!')
        return super().form_valid(form)

class SurveillanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Surveillance
    template_name = 'App1/confirm_delete.html'
    success_url = reverse_lazy('App1:surveillance_list')
    context_object_name = 'object'
    
    def test_func(self):
        # Check if the user owns the farm associated with this record
        record = self.get_object()
        return record.farm.owner == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Surveillance record deleted successfully!')
        return super().delete(request, *args, **kwargs)

"""
Key changes:

Added LoginRequiredMixin to ensure users must be logged in to access CRUD functionality
Added UserPassesTestMixin to ensure users can only view/modify their own data
Used test_func() methods to verify ownership of resources
Filtered querysets to only show data belonging to the current user
Added success messages after CRUD operations
For SurveillanceForm, passed the current user to filter farms in the form

"""