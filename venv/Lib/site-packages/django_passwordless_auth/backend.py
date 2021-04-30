from django.contrib.auth.backends import ModelBackend, UserModel

USERNAME_FIELD = UserModel.USERNAME_FIELD if hasattr(
    UserModel, 'USERNAME_FIELD') else 'username'


class PasswordlessAuthBackend(ModelBackend):

    def authenticate(self, username=None):
        try:
            return UserModel.objects.get(**{USERNAME_FIELD: username})
        except UserModel.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            pass
