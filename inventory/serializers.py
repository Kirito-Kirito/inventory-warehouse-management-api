from rest_framework import serializers
from .models import Category, Product, Supplier, Warehouse


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        #all of fields form model
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    #read only and relational data's format to show beautiful format, can add more fields
    category_name = serializers.ReadOnlyField(source= 'category.name')
    supplier_name = serializers.ReadOnlyField(source= 'supplier.name')

    class Meta:
        model = Product
        # fields = '__all__'
        fields = [
            'id',
            'sku',
            'name',
            'category',
            'category_name',
            'supplier',
            'supplier_name',
            'unit_price',
            'current_stock',
            'reorder_level',
            'created_at',
            'updated_at'
        ]