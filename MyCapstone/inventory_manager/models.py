from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="Username")
    email = models.EmailField(unique=True, db_index=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Last Name")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_staff = models.BooleanField(default=False, verbose_name="Is Staff")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date Joined")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

# Category Model for inventory items
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name", db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# InventoryItem Model
class InventoryItem(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Item Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items', verbose_name="Category")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inventory_items', verbose_name="Owner")

    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"

    def __str__(self):
        return f"{self.name} (Quantity: {self.quantity})"

# InventoryChangeLog Model to track inventory changes
class InventoryChangeLog(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='change_logs', verbose_name="Inventory Item")
    change_amount = models.IntegerField(verbose_name="Change Amount")
    reason = models.CharField(max_length=255, verbose_name="Reason for Change")
    date_changed = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Date Changed")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='change_logs', verbose_name="Changed By")

    class Meta:
        verbose_name = "Inventory Change Log"
        verbose_name_plural = "Inventory Change Logs"

    def __str__(self):
        return f"{self.change_amount} change for {self.inventory_item.name} by {self.changed_by.email}"
