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
from django.contrib.auth.models import User


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
    # For superusers, provide an option to view system-wide data or filter by user
    if request.user.is_superuser:
        # Get selected user if any
        user_filter = request.GET.get('user_filter', 'all')
        
        if user_filter != 'all':
            try:
                selected_user_id = int(user_filter)
                selected_user = User.objects.get(id=selected_user_id)
                farms = Farm.objects.filter(owner=selected_user)
            except (ValueError, TypeError, User.DoesNotExist):
                farms = Farm.objects.all()
        else:
            farms = Farm.objects.all()
            
        # Count total farms
        farms_count = farms.count()        # Create context for superuser view with filtered stats
        if user_filter != 'all':
            # Get filtered statistics based on the selected user
            try:
                selected_user_id = int(user_filter)
                selected_user = User.objects.get(id=selected_user_id)
                
                # Get all farms for this user
                user_farms = Farm.objects.filter(owner=selected_user)
                farm_ids = user_farms.values_list('id', flat=True)
                
                # Count statistics specific to this user
                user_farms_count = user_farms.count()
                user_surveillance_count = Surveillance.objects.filter(farm__owner=selected_user).count()
                user_pests_count = Pest.objects.filter(created_by=selected_user).count()
                user_tasks_count = Task.objects.filter(farm__owner=selected_user).count()
                user_entries_count = EntryExitLog.objects.filter(farm__in=farm_ids).count()
                
                context = {
                    'is_superuser': True,
                    'farms': farms,
                    'farms_count': farms_count,
                    'users': User.objects.all(),
                    'current_user_filter': user_filter,
                    'total_users': 1,  # Just the selected user
                    'total_farms': user_farms_count,
                    'total_surveillance': user_surveillance_count,
                    'total_pests': user_pests_count,
                    'total_tasks': user_tasks_count,
                    'total_entries': user_entries_count
                }
            except (ValueError, TypeError, User.DoesNotExist):
                # Fallback to showing all statistics
                context = {
                    'is_superuser': True,
                    'farms': farms,
                    'farms_count': farms_count,
                    'users': User.objects.all(),
                    'current_user_filter': user_filter,
                    'total_users': User.objects.count(),
                    'total_farms': Farm.objects.count(),
                    'total_surveillance': Surveillance.objects.count(),
                    'total_pests': Pest.objects.count(),
                    'total_tasks': Task.objects.count(),
                    'total_entries': EntryExitLog.objects.count()
                }
        else:
            # Show all system statistics
            context = {
                'is_superuser': True,
                'farms': farms,
                'farms_count': farms_count,
                'users': User.objects.all(),
                'current_user_filter': user_filter,
                'total_users': User.objects.count(),
                'total_farms': Farm.objects.count(),
                'total_surveillance': Surveillance.objects.count(),
                'total_pests': Pest.objects.count(),
                'total_tasks': Task.objects.count(),
                'total_entries': EntryExitLog.objects.count()
            }
    else:
        # Regular user view - show only their farms
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
            'is_superuser': False,
            'farms': farms,
            'farms_count': farms_count,
            'ci_results': ci_results
        }

    return render(request, 'App2/profile.html', context)

@login_required
def farm_list(request):
    # Superuser can see all farms, regular users only see their own
    if request.user.is_superuser:
        # Get filter param from query string, default to viewing all
        user_filter = request.GET.get('user_filter', 'all')
        if user_filter != 'all':
            try:
                user_id = int(user_filter)
                farms = Farm.objects.filter(owner_id=user_id)
            except (ValueError, TypeError):
                farms = Farm.objects.all()
        else:
            farms = Farm.objects.all()
        
        # Pass the list of users for the filter dropdown
        context = {
            'farms': farms,
            'users': User.objects.all(),
            'current_user_filter': user_filter,
            'is_superuser': True
        }
    else:
        farms = Farm.objects.filter(owner=request.user)
        context = {
            'farms': farms,
            'is_superuser': False
        }
    
    return render(request, 'App2/farm_list.html', context)

class EntryExitListView(LoginRequiredMixin, ListView):
    model = EntryExitLog
    template_name = 'App2/entryexit_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        if self.request.user.is_superuser:
            # Get filter param from query string, default to viewing all
            user_filter = self.request.GET.get('user_filter', 'all')
            if user_filter != 'all':
                try:
                    user_id = int(user_filter)
                    return EntryExitLog.objects.filter(farm__owner_id=user_id)
                except (ValueError, TypeError):
                    return EntryExitLog.objects.all()
            else:
                return EntryExitLog.objects.all()
        else:
            return EntryExitLog.objects.filter(farm__owner=self.request.user)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_superuser:
            context['users'] = User.objects.all()
            context['current_user_filter'] = self.request.GET.get('user_filter', 'all')
            context['is_superuser'] = True
        else:
            context['is_superuser'] = False
            
        return context

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
        # Superusers can access anything
        if self.request.user.is_superuser:
            return True
            
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
        context['is_superuser'] = self.request.user.is_superuser
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
        if self.request.user.is_superuser:
            # Get filter param from query string, default to viewing all
            user_filter = self.request.GET.get('user_filter', 'all')
            if user_filter != 'all':
                try:
                    user_id = int(user_filter)
                    return Pest.objects.filter(created_by_id=user_id)
                except (ValueError, TypeError):
                    return Pest.objects.all()
            else:
                return Pest.objects.all()
        else:
            return Pest.objects.filter(created_by=self.request.user)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_superuser:
            context['users'] = User.objects.all()
            context['current_user_filter'] = self.request.GET.get('user_filter', 'all')
            context['is_superuser'] = True
        else:
            context['is_superuser'] = False
            
        return context

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
        # Superusers can update any pest
        if self.request.user.is_superuser:
            return True
        # Regular users can only update their own pests
        return self.get_object().created_by == self.request.user

class PestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pest
    template_name = 'app2/pest_confirm_delete.html'
    success_url = reverse_lazy('App2:pest-list')

    def test_func(self):
        # Superusers can delete any pest
        if self.request.user.is_superuser:
            return True
        # Regular users can only delete their own pests
        pest = self.get_object()
        return pest.created_by == self.request.user

# SURVEILLANCE VIEWS
class SurveillanceListView(LoginRequiredMixin, ListView):
    model = Surveillance
    template_name = 'app2/surveillance_list.html'
    context_object_name = 'surveillance_records'

    def get_queryset(self):
        if self.request.user.is_superuser:
            # Get filter param from query string, default to viewing all
            user_filter = self.request.GET.get('user_filter', 'all')
            qs = Surveillance.objects.all()
            
            if user_filter != 'all':
                try:
                    user_id = int(user_filter)
                    qs = qs.filter(farm__owner_id=user_id)
                except (ValueError, TypeError):
                    pass
        else:
            qs = Surveillance.objects.filter(farm__owner=self.request.user)
            
        # Filter by severity if provided
        severity = self.request.GET.get('severity')
        if severity:
            qs = qs.filter(severity=severity)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['severity_filter'] = self.request.GET.get('severity')
        
        if self.request.user.is_superuser:
            context['users'] = User.objects.all()
            context['current_user_filter'] = self.request.GET.get('user_filter', 'all')
            context['is_superuser'] = True
        else:
            context['is_superuser'] = False
            
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
        # Allow superusers to view any surveillance record
        if self.request.user.is_superuser:
            return True
        # Regular users can only view their own records
        return self.get_object().farm.owner == self.request.user
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_superuser'] = self.request.user.is_superuser
        return context

class SurveillanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Surveillance
    form_class = SurveillanceForm
    template_name = 'app2/surveillance_form.html'
    success_url = reverse_lazy('App2:surveillance-list')

    def test_func(self):
        # Allow superusers to update any surveillance record
        if self.request.user.is_superuser:
            return True
        # Regular users can only update their own records
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
        # Allow superusers to delete any surveillance record
        if self.request.user.is_superuser:
            return True
        # Regular users can only delete their own records
        return self.get_object().farm.owner == self.request.user
    

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'App2/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.user.is_superuser:
            # Get filter param from query string, default to viewing all
            user_filter = self.request.GET.get('user_filter', 'all')
            if user_filter != 'all':
                try:
                    user_id = int(user_filter)
                    return Task.objects.filter(farm__owner_id=user_id).order_by('scheduled_date', 'scheduled_time')
                except (ValueError, TypeError):
                    return Task.objects.all().order_by('scheduled_date', 'scheduled_time')
            else:
                return Task.objects.all().order_by('scheduled_date', 'scheduled_time')
        else:
            return Task.objects.filter(farm__owner=self.request.user).order_by('scheduled_date', 'scheduled_time')
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_superuser:
            context['users'] = User.objects.all()
            context['current_user_filter'] = self.request.GET.get('user_filter', 'all')
            context['is_superuser'] = True
        else:
            context['is_superuser'] = False
            
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'App2/task_form.html'
    success_url = reverse_lazy('App2:task-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'App2/task_form.html'
    success_url = reverse_lazy('App2:task-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
        
    def test_func(self):
        # Superusers can update any task
        if self.request.user.is_superuser:
            return True
        # Regular users can only update their own tasks
        return self.get_object().farm.owner == self.request.user

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'App2/task_confirm_delete.html'
    success_url = reverse_lazy('App2:task-list')
    
    def test_func(self):
        # Superusers can delete any task
        if self.request.user.is_superuser:
            return True
        # Regular users can only delete their own tasks
        return self.get_object().farm.owner == self.request.user
