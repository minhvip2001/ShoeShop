from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["deleted"]

    def validate_name(self, data):
        category_name = data.get("name")
        for category in Category.objects.all():
            if(category.name == category_name):
                raise serializers.ValidationError(_("Category_name is existed"))

class CategoryReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
