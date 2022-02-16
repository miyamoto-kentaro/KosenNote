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

# 仮登録モデル
class PreRegister(models.Model):
    email = models.EmailField(_('email address'), unique=True,null=False,blank=False)
    authentication_code = models.CharField(max_length=144,null=False,blank=False)
    create_at = models.DateField(auto_now_add=True)

    class Meta():
        pass

    def __str__(self) -> str:
        return self.email
    
    def confirm_code(self, code):
        if self.AuthenticationCode == code:
            return True
        else:
            return False
