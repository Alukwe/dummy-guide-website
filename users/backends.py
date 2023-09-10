from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            user=None

        if user and user.check_password(password):
            return user