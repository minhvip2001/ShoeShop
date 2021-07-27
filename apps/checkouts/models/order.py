import uuid
from django.utils.translation import gettext_lazy as _
from core.utils import get_generated_code
from django.db import models
from django.db.models.fields import DateTimeField
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from apps.users.models import User
from apps.customers.models import Customer

class Status(models.TextChoices):
    DRAFT = "DRAFT", _("DRAFT")
    PAYING = "PAYING", _("PAYING")
    FINISH = "FINISH", _("FINISH")
    
class Order(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="orders",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20, null=False, blank=False, choices=Status.choices,
    )
    code = models.CharField(max_length=10, blank=False, null=False)
    note = models.TextField(blank=True, null=True)
    total = models.PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order"
        ordering = ["created_at"]

    def __str__(self):
        return "{}-{}".format(self.id, self.customer)
    
    def save(self, keep_deleted=False, **kwargs):
        if not self.code:
            self.code = get_generated_code(Order, "I")
        total_bill = self.total
        if total_bill == 0:
            self.status = Status.FINISH
        super(Order, self).save(keep_deleted=keep_deleted, **kwargs)