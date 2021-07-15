from operator import truediv
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed, AuthenticationFailed
from rest_framework.permissions import BasePermission

from apps.users.models.permission import Permission
from apps.users.models.user import User
from apps.customers.models import Customer

class UserRolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not isinstance(user, User):
            return False
        if user.is_superuser:
            return True
        if request.method.lower() not in view.action_map:
            raise MethodNotAllowed(_("Method {method} is not allowed on this api. "
                                 "Only {allowed_methods} is allowed!").format(method=request.method,
                                                                              allowed_methods=view.allowed_methods))
        action = view.action
        module = view.basename

        try:
            Permission.objects.get(role=user.role, module=module, action=action)
            return True
        except Permission.DoesNotExist:
            pass

        raise PermissionDenied(
            _("You do not have permission to perform this action.")
        )

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if isinstance(user, Customer):
            return True
        return False   

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if isinstance(user, AnonymousUser):
            return False
        return user.is_superuser 