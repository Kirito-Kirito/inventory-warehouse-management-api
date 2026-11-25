# from rest_framework.permissions import IsAuthenticated
# from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from .models import StockMovement
from .serializers import StockMovementSerializer
from inventory.permissions import IsStaffOrReadOnly



class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all().order_by('-created_at')
    serializer_class = StockMovementSerializer

    permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        if 'user' in self.request.data and self.request.data['user'] is None:
            raise ValidationError({'user': ['This field may not be null']})

        if serializer.validated_data.get('user') is not None:
            serializer.save()
        else:
            serializer.save(user=self.request.user)
            
        # user = self.request.user
        # if getattr(user, 'role') in ['ADMIN', 'MANAGER']:
        #     serializer.save()
        # else:
        #     serializer.save(user=user)

        # serializer.save(
        #     user=self.request.user if self.request.user.is_authenticated else None
        # )

        # with transaction.atomic():
        #     movement = serializer.save(
        #         user=self.request.user if self.request.user.is_authenticated else None
        #     )
            # product = movement.product
            # quantity = movement.quantity
            # if movement.movement_type == 'IN':
            #     if quantity <= 0:
            #         raise ValidationError(
            #             {
            #                 'detail':
            #                     f'Stock can not be zero or negative!'
                            
            #             }
            #         )
            #     product.current_stock += quantity
            # elif movement.movement_type == 'OUT':
            #     if product.current_stock < quantity:
            #         raise ValidationError(
            #             {
            #                 'detail': (
            #                     f'Stock not enough! Current stock is'
            #                     f' {product.current_stock}.'
            #                 )
            #             }
            #         )
            #     product.current_stock -= quantity
            # elif movement.movement_type == 'ADJUSTMENT':
            #     product.current_stock = quantity
            # product.save()