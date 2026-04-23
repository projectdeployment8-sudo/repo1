from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class UsernameEmailPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get('identifier')
        if not identifier or not password:
            return None

        user = (
            User.objects.filter(
                Q(username__iexact=identifier)
                | Q(email__iexact=identifier)
                | Q(profile__phone__iexact=identifier)
            )
            .order_by('id')
            .first()
        )

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
