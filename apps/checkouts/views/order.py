from apps.products.models.product import Product
from rest_framework.response import Response
from apps.checkouts.serializers import OrderSerializer, OrderReadOnlySerializer
from apps.checkouts.models import Order, OrderItem
from rest_framework import status, viewsets
from core.mixins import GetSerializerClassMixin
from django.utils.translation import gettext_lazy as _
from apps.checkouts.filters import InvoiceFilterSet
from django.db import transaction

class OrderViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Order.objects.select_related("customer").order_by('-created_at')
    serializer_class = OrderSerializer
    serializer_action_classes = {
        'list': OrderReadOnlySerializer,
        'retrieve': OrderReadOnlySerializer,
    }
    filterset_class = InvoiceFilterSet

    def create_order_item(self, instance, order_item):
        product = Product.objects.get(pk=order_item["product"])
        price = order_item.get("price", product.price)
        quantity = order_item.get("quantity",1)
        ot = OrderItem(
            order=instance,
            product=product,
            product_name=product.name,
            price = price,
            quantity = quantity
        )
        return ot

    def create_or_update_quantity(self, product, quantity):
        update_quantity = Product.objects.select_for_update().get(id=product)
        update_quantity.quantity += quantity
        return update_quantity

    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        items = serializer.validated_data.pop("order_items", None)
        serializer.validated_data.pop("deleted_invoice_items",None)
        with transaction.atomic():
            instance = serializer.save()
            insert_data = []
            total = 0
            if items:
                for item in items:
                    product_updated = []
                    product = Product.objects.get(pk = item["product"])
                    total += product.price * item.get("quantity", 1)
                    ot = self.create_order_item(
                        instance = instance,
                        order_item = item
                    )
                    update_quantity = self.create_or_update_quantity(
                        product=product.id,
                        quantity=-item.get("quantity", 1)
                    )
                    product_updated.append(update_quantity)
                    insert_data.append(ot)
            Product.objects.bulk_update(product_updated, ['quantity'])
            OrderItem.objects.bulk_create(insert_data)

        total_amount = serializer.validated_data.get("total", None)
        instance.total = total_amount if total_amount else total
        return Response(status=status.HTTP_200_OK)
