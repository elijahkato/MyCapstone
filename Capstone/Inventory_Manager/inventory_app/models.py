from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

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

    
    item_image_thumbnail = ImageSpecField(
        source='item_image',
        processors=[ResizeToFill(100, 100)],  # Resize the image to 100x100 pixels for the thumbnail
        format='JPEG',
        options={'quality': 80}
    )
    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'

    def __str__(self):
        return f"{self.item_name} (Quantity: {self.item_qty})"

# Inventory Change Log model
class InventoryChangeLog(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='change_logs', verbose_name="Inventory Item")
    change_quantity = models.IntegerField(verbose_name="Change in Quantity", validators=[MinValueValidator(-10000), MaxValueValidator(10000)], null=True, blank=True)  # Changed to reflect quantity changes
    change_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Change in Price", null=True, blank=True)  # New field to log price changes
    reason = models.CharField(max_length=255, verbose_name="Reason for Change")
    date_changed = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Date Changed")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='change_logs', verbose_name="Changed By")
    change_details = models.TextField(verbose_name="Change Details", blank=True)  # Log other details about what changed

    class Meta:
        verbose_name = "Inventory Change Log"
        verbose_name_plural = "Inventory Change Logs"
        constraints = [
            models.CheckConstraint(
                check=models.Q(change_quantity__isnull=False) | models.Q(change_price__isnull=False),
                name='quantity_or_price_nonnull'
            ),
        ]

    def __str__(self):
        return f"Change for {self.inventory_item.item_name} by {self.changed_by.email}"

    def clean(self):
        # Validate that at least one of quantity or price has changed
        if self.change_quantity == 0 and not self.change_price:
            raise ValidationError("You must log either a change in quantity or price.")
        if self.change_quantity and (self.inventory_item.item_qty + self.change_quantity < 0):
            raise ValidationError("Change amount would result in negative inventory.")


# Signal to log changes to InventoryItem
@receiver(pre_save, sender=InventoryItem)
def log_inventory_item_changes(sender, instance, **kwargs):
    if instance.pk:
        # Get the original data before changes
        previous = InventoryItem.objects.get(pk=instance.pk)
        changes = {}
        change_quantity = instance.item_qty - previous.item_qty
        change_price = instance.item_price - previous.item_price if instance.item_price != previous.item_price else None

        # Compare fields to detect changes
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
                change_quantity=change_quantity if change_quantity != 0 else None,
                change_price=change_price if change_price is not None else None,
                reason=kwargs.get('reason', 'No reason provided'),
                changed_by=instance.owner,  # Or adjust how this is set
                change_details=changes if changes else {}
            )