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
]

