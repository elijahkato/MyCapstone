from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Category, InventoryItem, InventoryChangeLog
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from .serializers import UserRegistrationSerializer, UserSerializer, CategorySerializer, InventoryItemSerializer, InventoryChangeLogSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

User = get_user_model()

# Root API views
class ApiRootViewAuthenticated(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({
            'register': reverse('user_registration', request=request),
        })

# User management views
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Category views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

# Inventory item views
class InventoryItemListCreateView(generics.ListCreateAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return InventoryItem.objects.all()
        return InventoryItem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        item_qty = serializer.validated_data.get('item_qty', 0)
        if item_qty < 0:
            raise serializer.ValidationError({"item_qty": "Item Quantity cannot be less than 0."})
        serializer.save(owner=self.request.user)

class InventoryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return InventoryItem.objects.none()
        if self.request.user.is_staff:
            return InventoryItem.objects.all()
        return InventoryItem.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
    # Get old instance for comparison
        old_instance = self.get_object()
        updated_instance = serializer.save()

        changes = {}
        # Log quantity change if applicable
        if old_instance.item_qty != updated_instance.item_qty:
            changes['change_quantity'] = updated_instance.item_qty - old_instance.item_qty
        # Log price change if applicable
        if old_instance.item_price != updated_instance.item_price:
            changes['change_price'] = updated_instance.item_price - old_instance.item_price

        if changes:
            InventoryChangeLog.objects.create(
                inventory_item=updated_instance,
                change_quantity=changes.get('change_quantity', None),
                change_price=changes.get('change_price', None),
                reason=self.request.data.get('reason', 'No reason provided'),
                changed_by=self.request.user,
                change_details=f"Changes: {changes}"
            )


# Inventory change log views
class InventoryChangeLogListView(generics.ListAPIView):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return InventoryChangeLog.objects.all()
        return InventoryChangeLog.objects.filter(changed_by=self.request.user)

class InventoryChangeLogDetailView(generics.RetrieveAPIView):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return InventoryChangeLog.objects.none()
        if self.request.user.is_staff:
            return InventoryChangeLog.objects.all()
        return InventoryChangeLog.objects.filter(changed_by=self.request.user)
