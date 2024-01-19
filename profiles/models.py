from django.db import models
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    full_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='profile_image', default='avatar.png', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    national_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)

    credit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'user: {self.user}, full_name: {self.full_name}'