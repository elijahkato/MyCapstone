from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import (
    UserRegistrationView, UserListCreateView, UserProfileView, UserDetailView,
    CategoryListCreateView, CategoryDetailView,
    InventoryItemListCreateView, InventoryItemDetailView, InventoryLevelListView,
    InventoryChangeLogListView, ApiRootViewAuthenticated, InventoryChangeLogDetailView, 
    LowStockItemsView
)

urlpatterns = [
    # API ROOT views
    path('', ApiRootViewAuthenticated.as_view(), name='api_root_authenticated'),  # API root view for authenticated users
    #path('', ApiRootViewAllowAny.as_view(), name='api_root_open'),  # API root view for registration

    # User Registration
    path('register/', UserRegistrationView.as_view(), name='user_registration'),  # Register a new user

    # User Management
    path('users/', UserListCreateView.as_view(), name='user_list_create'),  # List all users or create a new user
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),  # Retrieve, Update, or Delete a user
    path('user/', UserProfileView.as_view(), name='user_profile'),  # Retrieve the currently logged-in user's profile

    # Category Management
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),  # List all categories or create a new category
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),  # Retrieve, Update, or Delete a category

    # Inventory Item Management
    path('inventory/', InventoryItemListCreateView.as_view(), name='inventory_list_create'),  # List all inventory items or create a new inventory item
    path('inventory/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory_detail'),  # Retrieve, Update, or Delete an inventory item
    path('inventory-levels/', InventoryLevelListView.as_view(), name='inventory_levels'),
    path('inventory/low-stock/', LowStockItemsView.as_view(), name='low_stock_items'),

    # Inventory Change Log Management
    path('inventory-change-logs/', InventoryChangeLogListView.as_view(), name='inventory_change_logs'),  # List all inventory change logs
    path('inventory-change-logs/<int:pk>/', InventoryChangeLogDetailView.as_view(), name='inventory_change_log_detail'),  # Retrieve an inventory change log

    # JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # JWT token verify
]
