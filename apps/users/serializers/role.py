from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ['deleted']

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.is_superuser:
            raise serializers.ValidationError(_('This user cannot set permission for other user\'s roles'))
        return attrs


class RoleReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)