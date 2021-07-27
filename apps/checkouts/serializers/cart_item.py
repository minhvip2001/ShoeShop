from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.checkouts.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ["deleted"]
        read_only_fields = ["created_at"]

    def to_internal_value(self, data):
        user = self.context['request'].user
        if not data.get('cart') and not isinstance(user, AnonymousUser):
            data['cart'] = user.cart.id
        ret = super(CartItemSerializer, self).to_internal_value(data)
        return ret

    def validate_quantity(self, quantity):
        if(quantity <= 0):
            raise serializers.ValidationError(_("Number of products must be greater than 0"))
        return quantity
        
class CartItemReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    cart_id = serializers.UUIDField(read_only=True)
    product_id = serializers.UUIDField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True ,source="product.price")
    created_at = serializers.DateTimeField(read_only=True)