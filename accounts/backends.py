from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import User

class UserBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass