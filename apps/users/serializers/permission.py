from rest_framework import serializers

from ..models.permission import Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        exclude = ['deleted']


class PermissionReadOnlySerialiser(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    module = serializers.CharField(read_only=True)
    action = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)