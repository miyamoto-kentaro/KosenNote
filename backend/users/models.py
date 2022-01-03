from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    locked = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
