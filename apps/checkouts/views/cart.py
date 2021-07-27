from apps.checkouts.models.cart_item import CartItem
from core.permissions import IsCustomer
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.checkouts.models import Cart
from apps.checkouts.serializers import CartSerializer, CartReadOnlySerializer, RemoveItemSerializer
from core.mixins import GetSerializerClassMixin

class CartViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    serializer_action_classes = {
        "list": CartReadOnlySerializer,
        "retrieve": CartReadOnlySerializer,
    }
    filterset_class = ()
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        queryset = self.queryset.all()
        return queryset

    @action(
        methods=["Delete"],
        detail=False,
        url_path="remove_item",
        url_name="remove_item",
        filterset_class=None,
        permission_classes=[IsAuthenticated],
        pagination_class=None,
    )
    def remove_item(self, request):
        serializer = RemoveItemSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        cart = CartItem.objects.filter(id = serializer.validated_data['id'])
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)