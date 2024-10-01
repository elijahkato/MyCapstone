from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Category, InventoryItem, InventoryChangeLog
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django.urls import reverse
from .serializers import UserRegistrationSerializer, UserSerializer, CategorySerializer, InventoryItemSerializer, InventoryChangeLogSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

User = get_user_model()

class ApiRootViewAuthenticated(APIView):
    permission_classes = [IsAuthenticated]  # Only allow authenticated access

    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse('user_list_create', request=request),
            'profile': reverse('user_profile', request=request),
            'categories': reverse('category_list_create', request=request),
            'inventory_items': reverse('inventory_list_create', request=request),
            'inventory_change_logs': reverse('inventory_change_logs', request=request),
            'token': reverse('token_obtain_pair', request=request),
            'token_refresh': reverse('token_refresh', request=request),
            'token_verify': reverse('token_verify', request=request),
        })

class ApiRootViewAllowAny(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access

    def get(self, request, *args, **kwargs):
        return Response({
            'register': reverse('user_registration',),
        })


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to register

# User Management: List all users or create a new user (for Admins only)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only admin can create or list users


# User Management: Retrieve, Update, or Delete a user (for Admins only)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only admin can modify user details


# User Management: Retrieve the currently logged-in user's profile
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access their profile

    def get_object(self):
        return self.request.user  # Return the currently logged-in user


# Category Management: List all categories or create a new category
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # Any authenticated user can view or create categories


# Category Management: Retrieve, Update, or Delete a category
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # Admins can modify; others can only view


# Inventory Item Management: List all inventory items or create a new inventory item
class InventoryItemListCreateView(generics.ListCreateAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admins can view all items, while regular users can view only their items
        if self.request.user.is_staff:
            return InventoryItem.objects.all()
        return InventoryItem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Custom validation before creation
        item_qty = serializer.validated_data.get('item_qty', 0)
        if item_qty < 0:
            raise serializer.ValidationError({"item_qty": "Item Quantity cannot be less than 0."})
        serializer.save(owner=self.request.user)  # Automatically assign the logged-in user as owner


# Inventory Item Management: Retrieve, Update, or Delete an inventory item
class InventoryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return InventoryItem.objects.none()
        # Admins can view all items, while regular users can view only their items
    
        if self.request.user.is_staff:
            return InventoryItem.objects.all()
        return InventoryItem.objects.filter(owner=self.request.user)

    # def get_queryset(self):
    #     # Admins can view all items, while regular users can view only their items
    #     if self.request.user.is_staff:
    #         return InventoryItem.objects.all()
    #     return InventoryItem.objects.filter(owner=self.request.user)


# Inventory Change Log Management: List all inventory change logs or create a new inventory change log
class InventoryChangeLogListView(generics.ListCreateAPIView):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admins can view all change logs, while regular users can view only their logs
        if self.request.user.is_staff:
            return InventoryChangeLog.objects.all()
        return InventoryChangeLog.objects.filter(changed_by=self.request.user)

    def perform_create(self, serializer):
        # Custom validation before creation
        change_amount = serializer.validated_data.get('change_amount', 0)
        if change_amount == 0:
            raise serializer.ValidationError({"change_amount": "Change Amount cannot be 0."})
        serializer.save(changed_by=self.request.user)


# Inventory Change Log Management: Retrieve, Update, or Delete an inventory change log
class InventoryChangeLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [IsOwnerOrReadOnly]


    def get_queryset(self):
        # Check if it's a swagger_fake_view
        if getattr(self, 'swagger_fake_view', False):
            return InventoryChangeLog.objects.none()  # Return an empty queryset for schema generation
        
        # For authenticated users
        if self.request.user.is_staff:
            return InventoryChangeLog.objects.all()
        return InventoryChangeLog.objects.filter(changed_by=self.request.user)
    # def get_queryset(self):
    #     # Admins can view all change logs, while regular users can view only their logs
    #     if self.request.user.is_staff:
    #         return InventoryChangeLog.objects.all()
    #     return InventoryChangeLog.objects.filter(changed_by=self.request.user)

