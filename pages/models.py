from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class NewsLetter(models.Model):
    email = models.EmailField(_('ایمیل'))

    class Meta:
        app_label = 'blog'

    def __str__(self):
        return self.email
