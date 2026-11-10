from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from logistic.filters import ProductFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', ]


class StockViewSet(ModelViewSet):
    queryset = (
        Stock.objects
        .prefetch_related('positions__product')
        .distinct()
    )
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['address', 'products']
    search_fields = ['address', 'products__title', 'products__description']

