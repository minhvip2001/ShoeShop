from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["deleted"]

class ProductImageReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    image = serializers.CharField(read_only=True)
    product = serializers.UUIDField(read_only=True, source="product_id")
    created_at = serializers.DateTimeField(read_only=True)
