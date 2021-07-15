import uuid
from enum import Enum
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.config import HARD_DELETE_NOCASCADE
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class RoleMName(Enum):
    ADMIN = "Admin",
    MANAGER = "Manager",
    SALE = "Sale"

class Role(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    permission = models.ManyToManyField(
        to='users.Permission',
        verbose_name =_('role permission')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role'
        ordering = ["created_at"]

    def __str__(self):
        return self.name