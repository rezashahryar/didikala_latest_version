from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import User


class SettingsBackend(BaseBackend):

    def authenticate(self, request, username=None, email=None, password=None):
        try:
            user = get_user_model().objects.get(email=username)
        except get_user_model().DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
