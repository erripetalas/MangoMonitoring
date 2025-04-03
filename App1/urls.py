from django.urls import path, re_path
from . import views

app_name = 'App1'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    re_path(r'^project/(?P<project_id>\d+)/$', views.project_details, name='project_details'),
    path('about/', views.about, name='about'),
]