from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Log out the user
def logout_view(request):
    logout(request)
    return redirect('App2:login')

# Profile page (requires login)
@login_required
def profile_view(request):
    return render(request, 'App2/profile.html')

# Handle user registration
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

# Handle user login
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
