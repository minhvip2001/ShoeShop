from core.permissions import IsAdmin, UserRolePermission
from django.db import transaction
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.filters import UserFilterSet
from apps.users.models import User
from apps.users.serializers import UserSerializer, UserReadOnlySerializer, LoginSerializer, RegisterSerializer
from core.mixins import GetSerializerClassMixin
from core.swagger_schemas import ManualParametersAutoSchema


class UserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        "list": UserReadOnlySerializer,
        "retrieve": UserReadOnlySerializer,
    }
    filterset_class = UserFilterSet
    permission_classes = [UserRolePermission]

    def get_queryset(self):
        queryset = self.queryset.all()
        if not self.request.user.is_superuser:
            queryset = queryset.exclude(is_superuser=True)
        return queryset

    @swagger_auto_schema(
        operation_description="Get me",
        auto_schema=ManualParametersAutoSchema,
        responses={200: UserReadOnlySerializer},
    )
    @action(
        methods=["GET"],
        detail=False,
        url_path="profile",
        url_name="profile",
        filterset_class=None,
        pagination_class=None,
    )
    def profile(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_action_classes.get("retrieve")(
            user
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Login",
        request_body=LoginSerializer,
        auto_schema=ManualParametersAutoSchema,
        responses={200: UserReadOnlySerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="login",
        url_name="login",
        filterset_class=None,
        permission_classes=[],  
        pagination_class=None,
    )
    def login(self, request, *args, **kwargs):   
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        try:
            user = authenticate(username=username, password=password)
        except exceptions.NotFound:
            raise APIException(
                _("User or password is wrong"),
                status.HTTP_404_NOT_FOUND,
            )
        except:
            raise APIException(_("Invalid token"), status.HTTP_400_BAD_REQUEST)
        if not user:
            raise APIException(
                _("User with username {username} not found").format(username=username),
                status.HTTP_404_NOT_FOUND,
            )
        token = user.token
        data = {"token": token}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        url_path="register",
        url_name="register",
        filterset_class=None,
        permission_classes=[IsAdmin],
        pagination_class=None,    
    )
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
       
        try:
            user = request.user
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                intance = serializer.save()
                intance.set_password(data['password'])
                intance.save()

        except Exception as e:
            raise APIException(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

        token = intance.token
        data = {"token": token}
        return Response(data=data, status=status.HTTP_200_OK)