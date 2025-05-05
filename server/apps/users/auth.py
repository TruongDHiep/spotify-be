from django.contrib.auth.hashers import check_password
from .models import User

class CustomBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            # Tìm user theo username
            user = User.objects.get(username=username)
            if check_password(password, user.pass_hash):
                return user
        except User.DoesNotExist:
            try:
                # Thử tìm theo email
                user = User.objects.get(email=username)
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