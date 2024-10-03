from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Custom User model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True, verbose_name="Email Address")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name='Profile Picture')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

# Category model
class Category(models.Model):
    category = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Category Name')
    cat_description = models.TextField(blank=True, null=True, verbose_name='Description')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.category

# Inventory Item model
class InventoryItem(models.Model):
    item_name = models.CharField(max_length=100, db_index=True)
    item_description = models.TextField(blank=True, null=True, verbose_name='Item Description')
    item_qty = models.PositiveIntegerField(default=0, verbose_name='Item Quantity')
    item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Item Price')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_items', verbose_name='Category')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date Added')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='Last Updated')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inventory_items', verbose_name='Owner')
    item_image = models.ImageField(upload_to='item_images/', null=True, blank=True, verbose_name='Item Image')

    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'

    def __str__(self):
        return f"{self.item_name} (Quantity: {self.item_qty})"

class InventoryChangeLog(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='change_logs', verbose_name="Inventory Item")
    change_amount = models.IntegerField(verbose_name="Change Amount", validators=[MinValueValidator(-10000), MaxValueValidator(10000)])
    reason = models.CharField(max_length=255, verbose_name="Reason for Change")
    date_changed = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Date Changed")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='change_logs', verbose_name="Changed By")
    change_details = models.JSONField(verbose_name="Change Details", default=dict, blank=True)  # Ensure it's always a valid JSON

    class Meta:
        verbose_name = "Inventory Change Log"
        verbose_name_plural = "Inventory Change Logs"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(change_amount=0),
                name='change_amount_nonzero'
            ),
        ]

    def __str__(self):
        return f"{self.change_amount} change for {self.inventory_item.item_name} by {self.changed_by.email}"

    def clean(self):
        if self.change_amount == 0 and not self.change_details:
            raise ValidationError("Change amount cannot be zero, and no other changes were made.")
        if self.inventory_item.item_qty + self.change_amount < 0:
            raise ValidationError("Change amount would result in negative inventory.")

    def save(self, *args, **kwargs):
        # Ensure that validation is executed
        self.full_clean()
        super().save(*args, **kwargs)

# Signal to log changes to InventoryItem
@receiver(pre_save, sender=InventoryItem)
def log_inventory_item_changes(sender, instance, **kwargs):
    if instance.pk:
        # Get the original data before changes
        previous = InventoryItem.objects.get(pk=instance.pk)
        changes = {}
        change_amount = instance.item_qty - previous.item_qty

        # Compare all fields to detect changes
        fields_to_check = ['item_name', 'item_description', 'item_qty', 'item_price', 'category']
        for field in fields_to_check:
            old_value = getattr(previous, field)
            new_value = getattr(instance, field)
            if old_value != new_value:
                changes[field] = {'old': old_value, 'new': new_value}

        # If any changes are detected, log them
        if changes:
            InventoryChangeLog.objects.create(
                inventory_item=instance,
                change_amount=change_amount,
                reason="Automatically logged change",  # This can be updated via the API/UI
                changed_by=instance.owner,  # You might want to adjust how this is set, depending on your flow
                change_details=changes
            )