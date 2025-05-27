from django.urls import path
from . import views

app_name = 'App2'

urlpatterns = [
    #Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    # Add signup and other farm management URLs here
    
    # Farm CRUD URLs
    path('farms/create/', views.FarmCreateView.as_view(), name='farm-create'),
    path('farms/<int:pk>/', views.FarmDetailView.as_view(), name='farm-detail'),
    path('farms/<int:pk>/update/', views.FarmUpdateView.as_view(), name='farm-update'),
    path('farms/<int:pk>/delete/', views.FarmDeleteView.as_view(), name='farm-delete'),
    
    # Pest CRUD URLs
    path('pests/', views.PestListView.as_view(), name='pest-list'),
    path('pests/create/', views.PestCreateView.as_view(), name='pest-create'),
    path('pests/<int:pk>/delete/', views.PestDeleteView.as_view(), name='pest-delete'),

    # Surveillance CRUD URLs
    path('surveillance/', views.SurveillanceListView.as_view(), name='surveillance-list'),
    path('surveillance/create/', views.SurveillanceCreateView.as_view(), name='surveillance-create'),
    path('surveillance/<int:pk>/', views.SurveillanceDetailView.as_view(), name='surveillance-detail'),
    path('surveillance/<int:pk>/update/', views.SurveillanceUpdateView.as_view(), name='surveillance-update'),
    path('surveillance/<int:pk>/delete/', views.SurveillanceDeleteView.as_view(), name='surveillance-delete'),
]