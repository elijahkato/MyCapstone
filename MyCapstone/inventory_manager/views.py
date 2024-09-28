from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, InventoryItem, Category, InventoryChangeLog
from .serializers import (UserSerializer, InventoryItemSerializer,
                          CategorySerializer, InventoryChangeLogSerializer)
from .permissions import IsOwnerOrReadOnly
from .forms import CustomUserCreationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# User Registration View (API)
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Inventory Item Views (API)
class InventoryItemListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class InventoryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

# Category Views (API)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Inventory Change Log View (API)
class InventoryChangeLogListView(generics.ListAPIView):
    queryset = InventoryChangeLog.objects.all()
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['inventory_item']

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# Public landing page - no authentication required
def landing_page(request):
    return render(request, 'landing.html')

# Protected dashboard view - requires login
@login_required
def dashboard_view(request, pk=None):
    inventory_items = InventoryItem.objects.filter(owner=request.user)  # Ensure only items belonging to the user are displayed
    selected_item = None

    if pk:
        selected_item = get_object_or_404(InventoryItem, pk=pk, owner=request.user)  # Ensure the selected item belongs to the user

    context = {
        'inventory_items': inventory_items,
        'selected_item': selected_item
    }

    return render(request, 'pages/dashboard.html', context)

# New view for displaying inventory item details in an HTML template
@login_required
def inventory_detail_view(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk, owner=request.user)  # Retrieve the specific item belonging to the logged-in user
    return render(request, 'pages/inventory_detail.html', {'item': item})

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register': reverse('user-register', request=request, format=format),
        'login': reverse('token_obtain_pair', request=request, format=format),
        'token-refresh': reverse('token_refresh', request=request, format=format),
        'inventory': reverse('inventory-list-create', request=request, format=format),
        'inventory-detail': reverse('inventory-detail', args=[1], request=request, format=format),  # Example with ID 1
        'categories': reverse('category-list-create', request=request, format=format),
        'category-detail': reverse('category-detail', args=[1], request=request, format=format),  # Example with ID 1
        'inventory-change-logs': reverse('inventory-change-log', request=request, format=format),
    })
