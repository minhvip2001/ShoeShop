from core.permissions import UserRolePermission
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from apps.users.filters import ProductFilterSet
from apps.products.models import Product
from apps.products.serializers import ProductSerializer, ProductReadOnlySerializer
from core.mixins import GetSerializerClassMixin
from core.swagger_schemas import ManualParametersAutoSchema


class ProductViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    serializer_action_classes = {
        "list": ProductReadOnlySerializer,
        "retrieve": ProductReadOnlySerializer,
    }
    filterset_class = ()
    permission_classes = [IsAuthenticated, UserRolePermission]

    def get_queryset(self):
        queryset = self.queryset.all()
        return queryset

def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    with transaction.atomic():
        instance = serializer.save()
    serializer = self.serializer_action_classes.get("retrieve")(instance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)