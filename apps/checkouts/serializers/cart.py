from apps.checkouts.serializers.cart_item import CartItemReadOnlySerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser


from apps.checkouts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ["deleted"]
        read_only_fields = ["created_at"]
    
        
class CartReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    customer_id = serializers.UUIDField(read_only=True)
    cart_items = CartItemReadOnlySerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)

class RemoveItemSerializer(serializers.Serializer):
    id =  serializers.UUIDField(required = True)

    def to_internal_value(self, data):
        
        user = self.context['request'].user

        if not data.get('cart') and not isinstance(user, AnonymousUser):
            data['cart'] = user.cart.id
        ret = super(RemoveItemSerializer, self).to_internal_value(data)
        return ret

    def validate_id(self, id):
        user = self.context['request'].user
        if user.cart is None:
            raise serializers.ValidationError(_("Cart is not existed"))
        cart_item = user.cart.cart_items.filter(id = id)
        if not cart_item:
            raise serializers.ValidationError(_("Cart Item is not existed"))
        return id