from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Farm, Surveillance, Pest, EntryExitLog, Task 
from .forms import FarmForm, SurveillanceForm, PestForm, SurveillanceFilterForm, EntryExitLogForm, TaskForm  
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

# PROFILE VIEW

@login_required
def profile_view(request):
    farms = request.user.farms.all()
    farms_count = farms.count()

    ci_results = []

    for farm in farms:
        # Get all pest counts from Surveillance entries related to this farm
        pest_counts = Surveillance.objects.filter(farm=farm).values_list('pest_count', flat=True)

        # Convert to list of integers
        pest_counts = [count for count in pest_counts if count is not None]

        if len(pest_counts) >= 2:
            n = len(pest_counts)
            mean_val = mean(pest_counts)
            std_err = stdev(pest_counts) / sqrt(n)
            t_value = t.ppf(0.975, df=n - 1)  # 95% CI
            margin_of_error = round(t_value * std_err, 2)

            ci_results.append({
                'farm_name': farm.name,
                'mean': round(mean_val, 2),
                'lower': round(mean_val - margin_of_error, 2),
                'upper': round(mean_val + margin_of_error, 2),
                'margin_of_error': margin_of_error
            })

    context = {
        'farms': farms,
        'farms_count': farms_count,
        'ci_results': ci_results
    }

    return render(request, 'App2/profile.html', context)

@login_required
def farm_list(request):
    farms = Farm.objects.filter(owner=request.user)
    return render(request, 'App2/farm_list.html', {'farms': farms})

class EntryExitListView(LoginRequiredMixin, ListView):
    model = EntryExitLog
    template_name = 'App2/entryexit_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return EntryExitLog.objects.filter(farm__owner=self.request.user)

class EntryExitCreateView(LoginRequiredMixin, CreateView):
    model = EntryExitLog
    form_class = EntryExitLogForm
    template_name = 'App2/entryexit_form.html'
    success_url = reverse_lazy('App2:entry-exit-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EntryExitUpdateView(LoginRequiredMixin, UpdateView):
    model = EntryExitLog
    form_class = EntryExitLogForm
    template_name = 'App2/entryexit_form.html'
    success_url = reverse_lazy('App2:entry-exit-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EntryExitDeleteView(LoginRequiredMixin, DeleteView):
    model = EntryExitLog
    template_name = 'App2/entryexit_confirm_delete.html'
    success_url = reverse_lazy('App2:entry-exit-list')


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
class FarmCreateView(LoginRequiredMixin, CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'app2/farm_form.html'
    success_url = reverse_lazy('App2:profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class FarmDetailView(LoginRequiredMixin, OwnerMixin, DetailView):
    model = Farm
    template_name = 'app2/farm_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_farms'] = Farm.objects.filter(owner=self.request.user)
        return context
    
class FarmUpdateView(LoginRequiredMixin, OwnerMixin, UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = 'app2/farm_form.html'
    success_url = reverse_lazy('App2:profile')

class FarmDeleteView(LoginRequiredMixin, OwnerMixin, DeleteView):
    model = Farm
    template_name = 'app2/farm_confirm_delete.html'
    success_url = reverse_lazy('App2:profile')

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

class PestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pest
    form_class = PestForm
    template_name = 'App2/pest_form.html'
    success_url = reverse_lazy('App2:pest-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().created_by == self.request.user

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
    

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'App2/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(farm__owner=self.request.user).order_by('scheduled_date', 'scheduled_time')

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'App2/task_form.html'
    success_url = reverse_lazy('App2:task-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'App2/task_form.html'
    success_url = reverse_lazy('App2:task-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'App2/task_confirm_delete.html'
    success_url = reverse_lazy('App2:task-list')
