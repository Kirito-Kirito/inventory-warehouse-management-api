from django.contrib import admin
from .models import StockMovement



@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'warehouse',
        'movement_type',
        'quantity',
        'user',
        'created_at'
    ]
    list_filter = ['movement_type', 'warehouse', 'created_at']

