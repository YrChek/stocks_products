from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', ]


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    # filterset_fields = ['products', ]

    def get_queryset(self):
        queryset = Stock.objects.all()
        product = self.request.query_params.get('products', False)
        if not product:
            return queryset

        marker = True
        for number in '0123456789':
            if number in product:
                marker = False
                break
        if marker:
            queryset = Stock.objects.filter(products__title__icontains=product)
            return queryset

        queryset = Stock.objects.filter(products__pk=product)
        return queryset
