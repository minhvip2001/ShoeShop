from apps.products.models import Product
from apps.checkouts.models import Order
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class OrderItemWriteSerializer(serializers.Serializer):
    id = serializers.UUIDField(required = False)
    product = serializers.UUIDField(required=False)
    quantity = serializers.IntegerField(required=False, min_value=1, default=1)   
 
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemWriteSerializer(many=True, required=False)
    created_at = serializers.DateTimeField(read_only=False, required=False)
    deleted_order_items = serializers.ListField(child=serializers.UUIDField(), required=False, allow_null=True)

    class Meta:
        model = Order
        exclude = ["deleted"]
        read_only_fields = ["code", "state"]
        extra_kwargs = {
            "total": {"required": True},
        }

    def validate_order_items(self, order_items):
        errors=[]
        if self.instance:
            dic_invoice_items = {i.id: i for i in self.instance.order_items.all()}
        dic_products={p.id: p for p in Product.objects.all()}

        for ot in order_items:
            if "id" in ot:
                if "product" in ot:
                    errors.append(_("Can not change product of an Invoice Item"))
                    continue
                if dic_invoice_items.get(ot.get("id")) is None:
                    errors.append(_("OrderItem {id} does not exist in Order {order}").format(id = ot.get("id"), order=self.instance.id))
                    continue
            else:
                if "product" not in ot:
                    errors.append(_("Can not blank product when create InvoiceItem"))
                    continue
                else:
                    if dic_products.get(ot.get("product")) is None:
                        errors.append(_("Product {id} does not exist in store").format(id = ot.get("product")))
                        continue

        if len(errors)>0:
                raise serializers.ValidationError(errors)
        return order_items

    def validate_deleted_invoice_items(self, deleted_order_items):
        if self.instance:
            order_item_ids = self.instance.order_items.all().values_list("id",flat=True)
            invalid_ids=set(deleted_order_items)-set(order_item_ids)
            errors=[]
            for id in invalid_ids:
                errors.append(_("OrderItem {id} does not exist in Order {order}").format(id = id,order = self.order.id))
            if len(errors) >0:
                raise serializers.ValidationError(errors)
        return deleted_order_items

class OrderReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.UUIDField(read_only=True, source="user_id")
    customer = serializers.UUIDField(read_only=True, source="customer_id")
    status = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    total = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    customer_name = serializers.CharField(
        read_only=True, source="customer.name"
    )
    note = serializers.CharField(read_only=True)