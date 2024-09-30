from django.contrib import admin
from .models import CustomUser, InventoryItem, Category, InventoryChangeLog

# Custom admin configuration for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff', 'date_joined')

# Custom admin configuration for InventoryItem
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'category', 'owner', 'date_added', 'last_updated')
    search_fields = ('name', 'category__name', 'owner__email')
    list_filter = ('category', 'owner', 'date_added')

# Custom admin configuration for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Custom admin configuration for InventoryChangeLog
class InventoryChangeLogAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'change_amount', 'reason', 'date_changed', 'changed_by')
    search_fields = ('inventory_item__name', 'changed_by__email')
    list_filter = ('inventory_item', 'date_changed', 'changed_by')

# Registering the models with the custom admin configurations
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(InventoryChangeLog, InventoryChangeLogAdmin)
