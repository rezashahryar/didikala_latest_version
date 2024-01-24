from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name=_('کاربر'))

    full_name = models.CharField(_('نام و نام خانوادگی'), max_length=50, null=True, blank=True)
    image = models.ImageField(_('عکس'), upload_to='profile_image', default='avatar.png', null=True, blank=True)
    email = models.EmailField(_('ایمیل'), null=True, blank=True)
    national_code = models.CharField(_('کد ملی'), max_length=20, null=True, blank=True)
    phone_number = models.CharField(_('شماره موبایل'), max_length=12, null=True, blank=True)

    credit = models.PositiveIntegerField(_('اعتبار'), default=0)

    def __str__(self):
        return f'user: {self.user}, full_name: {self.full_name}'