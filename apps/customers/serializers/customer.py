from django.utils.translation import gettext_lazy as _
from apps.users.models.user import User
from rest_framework import serializers

from apps.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]
    
        
class CustomerReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    fullname = serializers.CharField(read_only=True)
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
    fullname = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    def validate_username(self, username):
        for account in User.objects.all():
            if(account.username == username):
                raise serializers.ValidationError(_("Username is existed"))