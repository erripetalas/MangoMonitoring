from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from .models import Farm, PlantLocation, Surveillance, Pest
from .forms import FarmForm, PlantLocationForm, SurveillanceForm, PestForm, SurveillanceFilterForm
from statistics import mean, stdev
from math import sqrt
from scipy.stats import t
from django.db.models import Avg


# AUTHENTICATION VIEWS
def logout_view(request):
    logout(request)
    return redirect('App2:login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('App2:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'App2/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('App2:profile')
    else:
        form = UserCreationForm()
    return render(request, 'App2/register.html', {'form': form})

from statistics import mean, stdev
from math import sqrt
from scipy.stats import t

@login_required
def profile_view(request):
    farms = request.user.farms.all()[:5]
    ci_results = []

    for farm in farms:
        inspections = farm.surveillance_records.all().values_list('pest_count', flat=True)
        if len(inspections) >= 2:
            sample = list(inspections)
            n = len(sample)
            mean_val = mean(sample)
            std_dev = stdev(sample)
            stderr = std_dev / sqrt(n)
            t_score = t.ppf(0.975, df=n - 1)
            margin = t_score * stderr
            lower = round(mean_val - margin, 2)
            upper = round(mean_val + margin, 2)

            ci_results.append({
                'farm_name': farm.name,
                'mean': round(mean_val, 2),
                'lower': lower,
                'upper': upper,
                'margin_of_error': round(margin, 2)
            })

    context = {
        'farms': farms,
        'farms_count': request.user.farms.count(),
        'ci_results': ci_results
    }
    return render(request, 'App2/profile.html', context)




# OWNER Mixin
class OwnerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        if hasattr(obj, 'owner'):
            return obj.owner == self.request.user
        elif hasattr(obj, 'farm'):
            return obj.farm.owner == self.request.user
        return False

# FARM VIEWS
class FarmListView(LoginRequiredMixin, ListView):
    model = Farm
    template_name = 'app2/farm_list.html'
    context_object_name = 'farms'

    def get_queryset(self):
        return Farm.objects.filter(owner=self.request.user)

class FarmCreateView(LoginRequiredMixin, CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'app2/farm_form.html'
    success_url = reverse_lazy('App2:farm-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class FarmDetailView(LoginRequiredMixin, OwnerMixin, DetailView):
    model = Farm
    template_name = 'app2/farm_detail.html'

class FarmUpdateView(LoginRequiredMixin, OwnerMixin, UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = 'app2/farm_form.html'
    success_url = reverse_lazy('App2:farm-list')

class FarmDeleteView(LoginRequiredMixin, OwnerMixin, DeleteView):
    model = Farm
    template_name = 'app2/farm_confirm_delete.html'
    success_url = reverse_lazy('App2:farm-list')

# LOCATION VIEWS
class LocationCreateView(LoginRequiredMixin, CreateView):
    model = PlantLocation
    form_class = PlantLocationForm
    template_name = 'app2/location_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.farm = get_object_or_404(Farm, pk=kwargs['farm_pk'], owner=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farm'] = self.farm
        return context

    def form_valid(self, form):
        form.instance.farm = self.farm
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('App2:farm-detail', kwargs={'pk': self.farm.pk})

# PEST VIEWS
class PestListView(LoginRequiredMixin, ListView):
    model = Pest
    template_name = 'app2/pest_list.html'
    context_object_name = 'pests'

    def get_queryset(self):
        return Pest.objects.filter(created_by=self.request.user)

class PestCreateView(LoginRequiredMixin, CreateView):
    model = Pest
    form_class = PestForm
    template_name = 'app2/pest_form.html'
    success_url = reverse_lazy('App2:pest-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pest
    template_name = 'app2/pest_confirm_delete.html'
    success_url = reverse_lazy('App2:pest-list')

    def test_func(self):
        pest = self.get_object()
        return pest.created_by == self.request.user

# SURVEILLANCE VIEWS
class SurveillanceListView(LoginRequiredMixin, ListView):
    model = Surveillance
    template_name = 'app2/surveillance_list.html'
    context_object_name = 'surveillance_records'

    def get_queryset(self):
        qs = Surveillance.objects.filter(farm__owner=self.request.user)
        severity = self.request.GET.get('severity')
        if severity:
            qs = qs.filter(severity=severity)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['severity_filter'] = self.request.GET.get('severity')
        return context

class SurveillanceCreateView(LoginRequiredMixin, CreateView):
    model = Surveillance
    form_class = SurveillanceForm
    template_name = 'app2/surveillance_form.html'
    success_url = reverse_lazy('App2:surveillance-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class SurveillanceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Surveillance
    template_name = 'app2/surveillance_detail.html'

    def test_func(self):
        return self.get_object().farm.owner == self.request.user

class SurveillanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Surveillance
    form_class = SurveillanceForm
    template_name = 'app2/surveillance_form.html'
    success_url = reverse_lazy('App2:surveillance-list')

    def test_func(self):
        return self.get_object().farm.owner == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class SurveillanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Surveillance
    template_name = 'app2/surveillance_confirm_delete.html'
    success_url = reverse_lazy('App2:surveillance-list')

    def test_func(self):
        return self.get_object().farm.owner == self.request.user
