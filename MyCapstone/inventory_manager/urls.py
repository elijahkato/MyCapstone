# inventory_manager/urls.py
from django.urls import path
from .views import (
    UserCreateView, InventoryItemListCreateView, InventoryItemDetailView,
    CategoryListCreateView, CategoryDetailView, InventoryChangeLogListView,
    landing_page, dashboard_view, register, inventory_detail_view, api_root  # Include api_root
)

urlpatterns = [
    # API Root Endpoint
    path('api/', api_root, name='api-root'),  # The API index page

    # API Endpoints
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('api/inventory/', InventoryItemListCreateView.as_view(), name='inventory-list-create'),
    path('api/inventory/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory-detail'),
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/inventory-change-logs/', InventoryChangeLogListView.as_view(), name='inventory-change-log'),

    # Template Views
    path('', landing_page, name='landing'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('register/', register, name='register'),
    path('inventory/<int:pk>/', inventory_detail_view, name='inventory-detail-view'),  # New URL pattern for the inventory detail HTML view
]
