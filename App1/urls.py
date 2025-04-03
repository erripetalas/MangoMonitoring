from django.urls import path, re_path
from . import views

app_name = "App1"

urlpatterns = [
    #Homepage URL
    path('', views.home, name="home"),
    
    #project list page URL
    path("projects", views.project_list, name="project_list"),
    
    # Project details page - uses regex to capture a project_id parameter
    # The regex (?P<project_id>\d+) captures one or more digits and names it "project_id"
    # This will match URLs like "/project/1/", "/project/2/", etc.
    re_path(r'^project/(?P<project_id>\d+)/$', views.project_details, name="project_details"),
    
    # About page - matches "/about/"
    path("about/", views.about, name="about"),
]