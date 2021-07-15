from django.utils.translation import gettext_lazy as _
from apps.customers.models.customer import Customer
from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["deleted", 'is_superuser']
        read_only_fields = ["created_at", "updated_at"]
        
class UserReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    address = serializers.CharField(read_only=True)
    avatar_url = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    def validate_username(self, username):
        for account in Customer.objects.all():
            if(account.username == username):
                raise serializers.ValidationError(_("Username is existed"))