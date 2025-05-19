"""
URL configuration for MangoMonitoring project.
 
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from App1 import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('about', views.about, name='about'), # about page
    # All URLs defined in App1.urls will be accessible from the root URL
    path('', include('App1.urls')),
    path('myfarms/', include(('App2.urls', 'App2'), namespace='App2')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)