from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models, transaction
from inventory.models import Product, Warehouse


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = 'IN', 'Stock In'
        OUT = 'OUT', 'Stock Out'
        ADJUSTMENT = 'ADJUSTMENT', 'Stock Adjustment'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='movements')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    reference_no = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'{self.movement_type}: {self.quantity} of {self.product.name} by'
            f'{self.user}'
        )

    def save(self, *args, **kwargs):
        #if there is new pk(id), (it's only new record). prevent from stock validation for existing record to edit. 
        is_new = self.pk is None

        #Not to change data from database(rollback) if something happen an error etc.. 
        with transaction.atomic():
            if is_new:
                product = self.product.__class__.objects.select_for_update().get(
                    pk=self.product.pk
                )
            quantity = self.quantity

            if self.movement_type == 'IN':
                if quantity <= 0:
                    raise ValidationError('Stock can not be zero or negative!')
                product.current_stock += quantity
            elif self.movement_type == 'OUT':
                if product.current_stock < quantity:
                    raise ValidationError(
                        f'Stock not enough! Current stock is {product.current_stock}.'
                    )
                product.current_stock -= quantity
            elif self.movement_type == 'ADJUSTMENT':
                product.current_stock = quantity

            product.save()
            self.product = product
        super().save(*args, **kwargs)
