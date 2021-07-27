from apps.checkouts.filters import OrderItemFilterSet
from apps.checkouts.serializers.order_item import OrderItemReadOnlySerializer, OrderItemSerializer
from apps.checkouts.models import OrderItem
from core.mixins import GetSerializerClassMixin
from rest_framework import viewsets, status
class OrderItemViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.prefetch_related("item").all()
    serializer_class = OrderItemSerializer
    serializer_action_classes = {
        'list': OrderItemReadOnlySerializer,
        'retrieve': OrderItemReadOnlySerializer,
    }
    filterset_class = OrderItemFilterSet