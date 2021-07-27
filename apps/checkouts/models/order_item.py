import uuid
from django.db import models
from django.db.models.expressions import F
from apps.checkouts.models import Order
from apps.products.models import Product
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class OrderItem(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='order_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False
    )
    product_name = models.CharField(max_length=100, null=False, blank=False)
    price = models.PositiveIntegerField(null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_item"
        ordering = ["created_at"]
        
    def __str__(self):
        return "{}-{}".format(self.id, self.order)