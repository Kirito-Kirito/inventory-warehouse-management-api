from django.contrib import admin
from .models import Category, Product, Supplier, Warehouse

#admin.site.register(Supplier, SupplierAdmin)
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'contact_person',
        'email',
        'phone',
        'created_at'
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'sku',
        'name',
        'category',
        'supplier',
        'unit_price',
        'current_stock',
    ]
    #for searching by sku and name keyword
    search_fields = ['sku', 'name']
    #for filtering by category and supplier
    list_filter = ['category', 'supplier']