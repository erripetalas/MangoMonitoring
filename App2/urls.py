from django.urls import path
from . import views
from .views import EntryExitCreateView,TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView


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
    path('manage-farms/', views.farm_list, name='farm-list'),
    
    # Entry/Exit Log URLs
    path('entryexit/', views.EntryExitListView.as_view(), name='entry-exit-list'),
    path('entryexit/create/', EntryExitCreateView.as_view(), name='entry-exit-create'),
    path('entryexit/<int:pk>/edit/', views.EntryExitUpdateView.as_view(), name='entryexit-edit'),
    path('entryexit/<int:pk>/delete/', views.EntryExitDeleteView.as_view(), name='entryexit-delete'),


    # Task CRUD URLs
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),

    # Pest CRUD URLs
    path('pests/', views.PestListView.as_view(), name='pest-list'),
    path('pests/create/', views.PestCreateView.as_view(), name='pest-create'),
    path('pests/<int:pk>/delete/', views.PestDeleteView.as_view(), name='pest-delete'),
    path('pests/<int:pk>/update/', views.PestUpdateView.as_view(), name='pest-update'),


    # Surveillance CRUD URLs
    path('surveillance/', views.SurveillanceListView.as_view(), name='surveillance-list'),
    path('surveillance/create/', views.SurveillanceCreateView.as_view(), name='surveillance-create'),
    path('surveillance/<int:pk>/', views.SurveillanceDetailView.as_view(), name='surveillance-detail'),
    path('surveillance/<int:pk>/update/', views.SurveillanceUpdateView.as_view(), name='surveillance-update'),
    path('surveillance/<int:pk>/delete/', views.SurveillanceDeleteView.as_view(), name='surveillance-delete'),
]