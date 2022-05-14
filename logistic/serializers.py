from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        for postion in positions:
            StockProduct.objects.create(
                stock=stock,
                **postion
            )

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        pos = instance.id

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        for position in positions:
            pr = position.get('product')
            print(pr.pk)
            st = StockProduct.objects.filter(stock=pos, product=pr.pk)
            if len(st) == 0:
                StockProduct.objects.create(
                    stock=stock,
                    **position
                )
            else:
                st[0].quantity = position.get('quantity')
                st[0].price = position.get('price')
                st[0].save()

        return stock
