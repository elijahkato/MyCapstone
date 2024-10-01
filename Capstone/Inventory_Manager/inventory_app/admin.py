# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, InventoryItem, InventoryChangeLog

# Customizing the CustomUser admin interface
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'profile_picture')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )


# Registering the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'cat_description')
    search_fields = ('category',)
    ordering = ('category',)


# Registering the InventoryItem model
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'category', 'item_qty', 'item_price', 'owner', 'date_added', 'last_updated')
    list_filter = ('category', 'owner')
    search_fields = ('item_name', 'category__category', 'owner__email')
    ordering = ('-date_added',)
    readonly_fields = ('date_added', 'last_updated')

    # Display related data in dropdowns
    autocomplete_fields = ['category', 'owner']


# Registering the InventoryChangeLog model
@admin.register(InventoryChangeLog)
class InventoryChangeLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventory_item', 'change_amount', 'reason', 'date_changed', 'changed_by')
    search_fields = ('inventory_item__item_name', 'changed_by__email')
    list_filter = ('inventory_item', 'changed_by')
    ordering = ('-date_changed',)
    readonly_fields = ('date_changed',)
    
    # Display related data in dropdowns
    autocomplete_fields = ['inventory_item', 'changed_by']
