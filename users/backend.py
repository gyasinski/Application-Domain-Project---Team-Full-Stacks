from django.contrib.auth.backends import ModelBackend
from users.models import User

class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            user.check_password(password)
            return user
        except User.DoesNotExist:
            print('User not found!')
            pass
    def get_user(self, username):
        try:
            user = User.objects.get(pk=username)
            return user
        except User.DoesNotExist:
            return None