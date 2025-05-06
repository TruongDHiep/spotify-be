from django.contrib.auth.hashers import check_password
from .models import User

class CustomBackend:
    def authenticate(self, request, email=None, password=None):
        try:
            # Thử tìm theo email
            user = User.objects.get(email=email)
            if check_password(password, user.pass_hash):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None