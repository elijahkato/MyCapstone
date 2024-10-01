from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, InventoryItem, InventoryChangeLog

User = get_user_model()

# Custom User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
    
        user.set_password(validated_data['password'])
        user.save()
        return user

# Custom User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture']
        read_only_fields = ['id', 'email']

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category', 'cat_description']
        read_only_fields = ['id']

# Inventory Item Serializer
class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')

    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='owner')

    class Meta:
        model = InventoryItem
        fields = ['id', 'item_name', 'item_description', 'item_qty', 'item_price', 'category', 'category_id', 'date_added', 'last_updated', 'owner', 'owner_id', 'item_image']
        read_only_fields = ['id', 'date_added', 'last_updated', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user  # Automatically set the owner
        return super().create(validated_data)
    
    def validate(self, data):
        item_qty = data.get('item_qty', 0)
        item_price = data.get('item_price', 0.0)

        if item_qty < 0:
            raise serializers.ValidationError("Item Quantity cannot be less than 0.")
        
        if item_price < 0:
            raise serializers.ValidationError("Item Price cannot be less than 0.")
        return data

class InventoryChangeLogSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer(read_only=True)
    inventory_item_id = serializers.PrimaryKeyRelatedField(queryset=InventoryItem.objects.all(), write_only=True, source='inventory_item')

    class Meta:
        model = InventoryChangeLog
        fields = ['id', 'inventory_item', 'inventory_item_id', 'change_amount', 'reason', 'date_changed', 'changed_by']
        read_only_fields = ['id', 'date_changed', 'changed_by']

    def validate_change_amount(self, value):
        if value == 0:
            raise serializers.ValidationError("Change Amount cannot be 0.")
        return value

    def create(self, validated_data):
        validated_data['changed_by'] = self.context['request'].user
        return super().create(validated_data)