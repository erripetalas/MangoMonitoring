from django.urls import path
from . import views

app_name = 'App2'

urlpatterns = [
    # Placeholder login view
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    # Add signup and other farm management URLs here
]
