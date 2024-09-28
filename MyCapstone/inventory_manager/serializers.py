# inventory_manager/serializers.py

from rest_framework import serializers
from .models import CustomUser, InventoryItem, Category, InventoryChangeLog

# Custom User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Inventory Item Serializer
class InventoryItemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ['owner', 'date_added', 'last_updated']

# Inventory Change Log Serializer
class InventoryChangeLogSerializer(serializers.ModelSerializer):
    changed_by = serializers.ReadOnlyField(source='changed_by.email')
    item_name = serializers.ReadOnlyField(source='inventory_item.name')

    class Meta:
        model = InventoryChangeLog
        fields = '__all__'
