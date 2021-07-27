from rest_framework import serializers

from ..models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['deleted']

class OrderItemReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    order = serializers.UUIDField(read_only=True, source='order_id')
    product = serializers.UUIDField(read_only=True, source='product_id')
    product_name = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
