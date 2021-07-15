import uuid

from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from django.utils.translation import gettext_lazy as _
from .product import Product

class ProductImage(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.CharField(max_length=150, blank=False, null=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="product_images",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_image"
        ordering = ["created_at"]