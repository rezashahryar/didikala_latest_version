from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# create your models here


class User(AbstractUser):
    mobile = models.CharField(_('شماره موبایل'), max_length=13, unique=True)

    USERNAME_FIELD = 'mobile'

    @property
    def get_id(self):
        return f'user_{self.id}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.mobile

    class Meta:
        ordering = ('-mobile',)


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(_('کد'), max_length=20, unique=True)
    email = models.EmailField(_('ایمیل'), blank=True)
