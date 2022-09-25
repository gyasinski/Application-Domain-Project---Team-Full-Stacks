from django.contrib.auth.backends import BaseBackend
from users.models import User
from django.contrib.auth import get_user_model

class UserBackend(BaseBackend):
    def authenticate(self, username, password):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username, password=password)
            return user
        except User.DoesNotExist:
            print('User not found!')
            pass
    def get_user(self, username):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(username=username)
        except User.DoesNotExist:
            return None