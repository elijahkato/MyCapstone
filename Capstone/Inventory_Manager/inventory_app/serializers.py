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
    email = serializers.EmailField(required=True)
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
     
    # Validate the category name    
    def validate(self, data):
        category = data.get('category', None)
        if category is None:
            raise serializers.ValidationError("Category name cannot be empty.")
        return data
    

# Inventory Item Serializer
class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')

    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='owner')
    formatted_price = serializers.SerializerMethodField()
    class Meta:
        model = InventoryItem
        fields = ['id', 'item_name', 'item_description', 'item_qty', 'formatted_price', 'category', 'category_id', 'date_added', 'last_updated','low_stock_threshold', 'owner', 'owner_id', 'item_image']
        read_only_fields = ['id', 'date_added', 'last_updated', 'owner']
    
    def get_formatted_price(self, obj):
        return "N{:,.2f}".format(obj.item_price)

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
    
    # Update method to handle partial updates
    def update(self, instance, validated_data):
        instance.item_name = validated_data.get('item_name', instance.item_name)
        instance.item_description = validated_data.get('item_description', instance.item_description)
        instance.item_qty = validated_data.get('item_qty', instance.item_qty)
        instance.item_price = validated_data.get('item_price', instance.item_price)
        instance.low_stock_threshold = validated_data.get('low_stock_threshold', instance.low_stock_threshold)
        instance.category = validated_data.get('category', instance.category)
        instance.item_image = validated_data.get('item_image', instance.item_image)
        instance.save()
        return instance

# Inventory Change Log Serializer
class InventoryChangeLogSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer(read_only=True)
    inventory_item_id = serializers.PrimaryKeyRelatedField(queryset=InventoryItem.objects.all(), write_only=True, source='inventory_item')

    changed_by = serializers.CharField(source='changed_by.email', read_only=True)

    class Meta:
        model = InventoryChangeLog
        fields = ['id', 'inventory_item', 'inventory_item_id', 'change_quantity', 'change_price', 'reason', 'date_changed', 'changed_by']
        read_only_fields = ['id', 'date_changed', 'changed_by']

    # Validate the change in quantity or price
    def validate(self, data):
        # Ensure at least one of quantity or price has been modified
        if data.get('change_quantity') == 0 and not data.get('change_price'):
            raise serializers.ValidationError("Either quantity or price must be updated.")
        return data
    
    # Override the create method to automatically set the changed_by field
    def create(self, validated_data):
        validated_data['changed_by'] = self.context['request'].user
        return super().create(validated_data)
    
    
    


