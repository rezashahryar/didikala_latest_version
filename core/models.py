from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save

# create your models here


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError("the mobile must be set")
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("superuser must have an is_staff=True")

        return self.create_user(mobile=mobile, password=password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=11, unique=True)
    email = models.EmailField(blank=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'mobile'

    objects = CustomUserManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.mobile

    class Meta:
        ordering = ('-mobile',)



class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)