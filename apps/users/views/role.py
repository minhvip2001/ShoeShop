from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from apps.users.models import Role
from apps.users.serializers import RoleSerializer, RoleReadOnlySerializer
from core.mixins import GetSerializerClassMixin


class RoleViewSet(
    GetSerializerClassMixin, viewsets.ModelViewSet
):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    serializer_action_classes = {
        "list": RoleReadOnlySerializer,
        "retrieve": RoleReadOnlySerializer,
    }

    def create(self, request, *args, **kwargs):
        # on this time, we do not handle this case
        return Response(data={'message': _('this function is not allowed on this moment')},
                        status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        # on this time, we do not handle this case
        return Response(data={'message': _('this function is not allowed on this moment')},
                        status=status.HTTP_204_NO_CONTENT)