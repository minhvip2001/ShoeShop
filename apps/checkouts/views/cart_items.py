from core.permissions import IsCustomer
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.checkouts.models import CartItem
from apps.checkouts.serializers import CartItemSerializer, CartItemReadOnlySerializer
from core.mixins import GetSerializerClassMixin
from core.swagger_schemas import ManualParametersAutoSchema


class CartItemViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    serializer_action_classes = {
        "list": CartItemReadOnlySerializer,
        "retrieve": CartItemReadOnlySerializer,
    }
    filterset_class = ()
    permission_classes = [IsCustomer]

    def get_queryset(self):
        queryset = self.queryset.all()
        return queryset
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        cart_items = serializer.validated_data['cart'].cart_items.filter(product_id = product.id)
        if cart_items:
            cart_item = cart_items.first()
            cart_item.quantity += serializer.validated_data.get('quantity', 1)
            cart_item.save()
        else:
            cart_item = serializer.save()

        serializer = self.serializer_action_classes.get("retrieve")(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
