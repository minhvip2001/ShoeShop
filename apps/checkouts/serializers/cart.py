from apps.products.serializers.product_image import ProductImageReadOnlySerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.checkouts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ["deleted"]
        read_only_fields = ["created_at"]
    
        
class CartReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    customer_id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)