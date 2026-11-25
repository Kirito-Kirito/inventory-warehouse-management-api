# from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsStaffOrReadOnly,IsAuthenticatedDeleteStaffOnly
from .models import Category, Product, Supplier, Warehouse
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    SupplierSerializer,
    WarehouseSerializer,
)



class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsStaffOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsStaffOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedDeleteStaffOnly]
    
    #Pagination, Searching, Filtering, and Ordering 
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ['name']

    filterset_fields = ['category', 'supplier']

    ordering_fields = ['name', 'current_stock', 'unit_price']

    # Low stock Alert Custom Endpoint
    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock_alerts(self, request):
        threshold = int(request.query_params.get('threshold', 10))

        low_stock_products = self.queryset.filter(current_stock__lte=threshold)

        page = self.paginate_queryset(low_stock_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)
