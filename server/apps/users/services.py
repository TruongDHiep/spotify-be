from .models import User
from django.core.exceptions import ObjectDoesNotExist

class UserService:
    @staticmethod
    def update_user_info(user_id, validated_data):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

        for attr, value in validated_data.items():
            setattr(user, attr, value)

        user.save()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
        return user