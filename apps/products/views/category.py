from core.permissions import UserRolePermission
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from django.db.models import Count, F, Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException


from apps.products.filters import CategoryFilterSet
from apps.products.models import Category
from apps.products.serializers import (
    CategorySerializer,
    CategoryReadOnlySerializer,
)
from core.mixins import GetSerializerClassMixin


class CategoryViewSet(
    GetSerializerClassMixin, viewsets.ModelViewSet
):
    queryset = Category.objects.annotate(
        product_number=Count("products", filter=Q(products__deleted__isnull=True))
    ).order_by("-created_at")
    serializer_class = CategorySerializer
    serializer_action_classes = {
        "list": CategoryReadOnlySerializer,
        "retrieve": CategoryReadOnlySerializer,
    }
    filterset_class = CategoryFilterSet
    permission_classes = [UserRolePermission]