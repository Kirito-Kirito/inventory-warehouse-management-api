from rest_framework import serializers
from .models import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):

    product_name = serializers.ReadOnlyField(source = 'product.name')
    warehouse_name = serializers.ReadOnlyField(source = 'warehouse.name')
    user_name = serializers.ReadOnlyField(source = 'user.username')

    class Meta:
        model = StockMovement
        fields = [
            'id',
            'product',
            'product_name',
            'warehouse',
            'warehouse_name',
            'movement_type',
            'quantity',
            'user',
            'user_name',
            'created_at'
        ]
        read_only_fields = ['id','created_at']
    #Serializer is checking the field-level check and after that, this is object-level validation
    def validate(self, attrs):
        #if the value is update self.instance is check value from attrs
        movement_type = attrs.get(
            'movement_type', getattr(self.instance, 'movement_type', None)
        )
        quantity = attrs.get('quantity', getattr(self.instance, 'quantity', None))
        product = attrs.get('product', getattr(self.instance, 'product', None))

        if (
            movement_type == 'IN' 
            and quantity is not None 
            and quantity <= 0
        ):
            raise serializers.ValidationError('Stock can not be zero or negative!')
        if (
            movement_type == 'OUT'
            and product is not None
            and quantity is not None
        ):
            if product.current_stock < quantity:
                raise serializers.ValidationError(
                    f'Stock not enought! Current stock is {product.current_stock}.'
                )
        return attrs
