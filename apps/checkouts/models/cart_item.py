import uuid

from django.db import models
from safedelete.config import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel
from apps.checkouts.models import Cart
from apps.products.models import Product

class CartItem(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart,
        on_delete= models.CASCADE,
        related_name="cart_items"
    )
    product = models.ForeignKey(
        Product,
        on_delete= models.DO_NOTHING,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(blank=False, null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.cart, self.product)