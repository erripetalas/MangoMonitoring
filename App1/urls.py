from django.urls import path, re_path
from . import views
 
app_name = "App1"
 
urlpatterns = [
    # Homepage URL
    path('', views.home, name="index"),
    
    #project list page URL
    path("projects", views.project_list, name="projectlist"),
     path('', views.surveillance_list, name='surveillance_list'),

    path('farms/', views.farm_list, name='farm_list'),
    path('farms/create/', views.farm_create, name='farm_create'),
    path('farms/<int:pk>/update/', views.farm_update, name='farm_update'),
    path('farms/<int:pk>/delete/', views.farm_delete, name='farm_delete'),

    path('pests/', views.pest_list, name='pest_list'),
    path('pests/create/', views.pest_create, name='pest_create'),
    path('pests/<int:pk>/update/', views.pest_update, name='pest_update'),
    path('pests/<int:pk>/delete/', views.pest_delete, name='pest_delete'),

    path('surveillance/create/', views.surveillance_create, name='surveillance_create'),
    path('surveillance/<int:pk>/update/', views.surveillance_update, name='surveillance_update'),
    path('surveillance/<int:pk>/delete/', views.surveillance_delete, name='surveillance_delete'),
    # Project details page - uses regex to capture a project_id parameter
    # The regex (?P<project_id>\d+) captures one or more digits and names it "project_id"
    # This will match URLs like "/project/1/", "/project/2/", etc.
    
    re_path(r'^project/(?P<project_id>\d+)/$', views.project_details, name="projectdetails"),
    
    # About page - matches "/about/"
    path("about/", views.about, name="about"),
]