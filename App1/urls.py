from django.urls import path, re_path
from . import views
 
app_name = "App1"
 
urlpatterns = [
    # Homepage URL
    path('', views.home, name="index"),
    
    # Project list page URL
    path("projects", views.project_list, name="projectlist"),
    
    # Project details page - 
    re_path(r'^project/(?P<project_id>\d+)/$', views.project_details, name="projectdetails"),
    
    # About page - matches "/about/"
    path("about/", views.about, name="about"),
    
    # Farm CRUD URLs
    path('farms/', views.FarmListView.as_view(), name='farm_list'),
    path('farms/<int:pk>/', views.FarmDetailView.as_view(), name='farm_detail'),  # <int:pk> captures the primary key (ID) of the farm as an integer  
    path('farms/create/', views.FarmCreateView.as_view(), name='farm_create'),
    path('farms/<int:pk>/update/', views.FarmUpdateView.as_view(), name='farm_update'),
    path('farms/<int:pk>/delete/', views.FarmDeleteView.as_view(), name='farm_delete'),
    
    # Pest CRUD URLs
    path('pests/', views.PestListView.as_view(), name='pest_list'),
    path('pests/<int:pk>/', views.PestDetailView.as_view(), name='pest_detail'),
    path('pests/create/', views.PestCreateView.as_view(), name='pest_create'),
    path('pests/<int:pk>/update/', views.PestUpdateView.as_view(), name='pest_update'),
    path('pests/<int:pk>/delete/', views.PestDeleteView.as_view(), name='pest_delete'),
    
    # Surveillance CRUD URLs
    path('surveillance/', views.SurveillanceListView.as_view(), name='surveillance_list'),
    path('surveillance/<int:pk>/', views.SurveillanceDetailView.as_view(), name='surveillance_detail'),
    path('surveillance/create/', views.SurveillanceCreateView.as_view(), name='surveillance_create'),
    path('surveillance/<int:pk>/update/', views.SurveillanceUpdateView.as_view(), name='surveillance_update'),
    path('surveillance/<int:pk>/delete/', views.SurveillanceDeleteView.as_view(), name='surveillance_delete'),
]

