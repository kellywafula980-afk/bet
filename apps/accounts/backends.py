from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        # The admin login uses 'password', our custom login uses 'pin'
        # Accept both
        pin = password or kwargs.get('pin')
        if not phone_number or not pin:
            return None
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None
        if user.check_password(pin):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
