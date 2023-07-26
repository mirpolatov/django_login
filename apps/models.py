from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField, BooleanField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = CharField(max_length=255)
    email = EmailField(_("email address"), unique=True)
    is_active = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
