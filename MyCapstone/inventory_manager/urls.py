# inventory_manager/urls.py

from django.urls import path
from .views import (
    UserListCreateView, UserProfileView,
    CategoryListCreateView, CategoryDetailView,
    InventoryItemListCreateView, InventoryItemDetailView,
    InventoryChangeLogListView, InventoryChangeLogDetailView
)

urlpatterns = [
    # User Management
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
    path('user/', UserProfileView.as_view(), name='user_profile'),

    # Category Management
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),

    # Inventory Item Management
    path('inventory/', InventoryItemListCreateView.as_view(), name='inventory_list_create'),
    path('inventory/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory_detail'),

    # Inventory Change Log Management
    path('inventory-change-logs/', InventoryChangeLogListView.as_view(), name='inventory_change_logs'),
    path('inventory-change-logs/<int:pk>/', InventoryChangeLogDetailView.as_view(), name='inventory_change_log_detail'),
]
