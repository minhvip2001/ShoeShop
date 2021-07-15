import uuid

from .category import Category
from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from django.utils.translation import gettext_lazy as _

class Product(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    price = models.PositiveIntegerField(blank=False, null=False)
    sku = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
    )
    image = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
    )
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "product"
        ordering = ["created_at"]