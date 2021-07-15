import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteMixin
from django.contrib.auth.hashers import (
    check_password, make_password,
)

class CustomerGender(models.TextChoices):
    MALE = "MALE", _("MALE")
    FEMALE = "FEMALE", _("FEMALE")
    UNKNOWN = "UNKNOWN", _("UNKNOWN")

class Customer(SafeDeleteMixin):
    _safedelete_policy = SOFT_DELETE_CASCADE
    USERNAME_FIELD = "username"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=150, unique=True, blank=True, null=True
    )
    password = models.CharField(_('password'), max_length=128)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    address = models.TextField(max_length=150, null=True, blank=True)
    avatar_url = models.CharField(max_length=1000, null=True, blank=True)
    gender = models.CharField(
        choices=CustomerGender.choices,
        max_length=20,
        default=CustomerGender.UNKNOWN,
    )
    active = models.BooleanField(null=True, blank=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def token(self):
        return self._generate_jwt_token()

    def clean(self):
        super().clean()

    class Meta:
        db_table = "customer"
        ordering = ["created_at"]

    def _generate_jwt_token(self):
        iat = datetime.now()
        exp = iat + timedelta(days=60)
        payload = {
            "id": str(self.id),
            "fullname": self.fullname,
            "phone": self.phone,
            "email": self.email,
            "exp": exp,
            "iat": iat,
            "user": False 
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return token.decode("utf-8")

    @property
    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username if self.username else self.name if self.name else ""
