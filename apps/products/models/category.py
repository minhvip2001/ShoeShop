import uuid

from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from django.utils.translation import gettext_lazy as _

class Category(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "category"
        ordering = ["created_at"]

    def __str__(self):
        return self.name