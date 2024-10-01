# core/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('api/', include('inventory_manager.urls')),  # Include your app's URLs at the "api/" path
]
