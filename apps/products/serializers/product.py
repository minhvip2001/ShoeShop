from apps.products.serializers.product_image import ProductImageReadOnlySerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]
    
        
class ProductReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    price = serializers.CharField(read_only=True)
    sku = serializers.EmailField(read_only=True)
    description = serializers.CharField(read_only=True)
    image = serializers.CharField(read_only=True)
    product_images = serializers.ListField(
        child = ProductImageReadOnlySerializer(),
        source = "product_images.all",
        allow_null = True,
        allow_empty = True
    )
    category = serializers.UUIDField(read_only=True, source="category_id")
    size = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)
    height = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)