from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = StockProduct
        fields = ['product', 'product_id', 'price', 'quantity']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(source='stockproduct_set', many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('stockproduct_set')

        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                price=position['price'],
                quantity=position['quantity']
            )

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('stockproduct_set')

        stock = super().update(instance, validated_data)

        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={
                    'price': position['price'],
                    'quantity': position['quantity']
                }
            )

        return stock

