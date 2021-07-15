from rest_framework import viewsets

from apps.users.models import Permission
from apps.users.serializers import PermissionSerializer, PermissionReadOnlySerialiser
from core.mixins import GetSerializerClassMixin


class PermissionViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    serializer_action_classes = {
        "list": PermissionReadOnlySerialiser,
        "retrieve": PermissionReadOnlySerialiser,
    }
