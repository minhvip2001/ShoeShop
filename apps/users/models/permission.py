import uuid
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import UUIDField
from django.db.models.query_utils import Q
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class Permission(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.CharField(max_length=50, blank=False, null=False)
    action = models.CharField(max_length=40, blank=False, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "permission"
        constraints = [
            models.UniqueConstraint(fields=['module', 'action'], name='unique_permission',
                                    condition=Q(deleted__isnull=True)),
        ]
        ordering = ["created_at"]
