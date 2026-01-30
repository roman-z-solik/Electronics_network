from rest_framework import serializers
from .models import Product, NetworkNode


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='products',
        many=True,
        write_only=True,
        required=False
    )
    level = serializers.IntegerField(read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'node_type', 'email', 'country', 'city',
            'street', 'house_number', 'products', 'product_ids',
            'supplier', 'supplier_name', 'debt', 'created_at', 'level'
        ]
        read_only_fields = ['created_at']  # debt убрали

    def validate(self, data):
        if self.instance and 'debt' in data:
            if data['debt'] != self.instance.debt:
                raise serializers.ValidationError(
                    {'debt': 'Обновление задолженности запрещено через API'}
                )
        return data

    def update(self, instance, validated_data):
        validated_data.pop('debt', None)
        return super().update(instance, validated_data)
