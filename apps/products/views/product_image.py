from core.permissions import UserRolePermission
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException


from apps.products.models import ProductImage
from apps.products.serializers import (
    ProductImageSerializer,
    ProductImageReadOnlySerializer,
)
from core.mixins import GetSerializerClassMixin


class ProductImageViewSet(
    GetSerializerClassMixin, viewsets.ModelViewSet
):
    queryset = ProductImage.objects.all().order_by("-created_at")
    serializer_class = ProductImageSerializer
    serializer_action_classes = {
        "list": ProductImageReadOnlySerializer,
        "retrieve": ProductImageReadOnlySerializer,
    }
    filterset_class = ()
    permission_classes = [UserRolePermission]