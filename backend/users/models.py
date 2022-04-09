from datetime import datetime, date, timedelta

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db import IntegrityError
from django.contrib.auth.models import AbstractUser
from django.conf import settings


from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    locked = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    

# 仮登録モデル
class PreRegister(models.Model):
    email = models.EmailField(_('email address'), unique=True,null=False,blank=False)
    authentication_code = models.CharField(max_length=144,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta():
        pass

    def __str__(self) -> str:
        return self.email
    
    def confirm_code(self, code):
        # 仮登録モデルの有効期限(時間)
        limited = 1
        
        if timezone.now() - timedelta(hours=limited) < self.created_at:
            print('code : ',self.authentication_code, code )
            if self.authentication_code == code:
                print('ture')
                return 'Success'
            else:
                print('false')
                return 'FailureAuthentication'
        else:
            print('timelimit!')
            return 'Expired'

    
class ChangeEmailTicket(models.Model):
    previous_email = models.EmailField(_('email address'), unique=True,null=False,blank=False)
    email = models.EmailField(_('email address'), unique=True,null=False,blank=False)
    authentication_code = models.CharField(max_length=144,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta():
        pass

    def __str__(self) -> str:
        return self.email
    
    def confirm_code(self, code):
        # 仮登録モデルの有効期限(時間)
        limited = 1
        if timezone.now() - timedelta(hours=limited) < self.created_at:
            print('code : ',self.authentication_code, code )
            if self.authentication_code == code:
                print('ture')
                return 'Success'
            else:
                print('false')
                return 'FailureAuthentication'
        else:
            print('timelimit!')
            return 'Expired'


