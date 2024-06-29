from rest_framework.exceptions import APIException

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from django_users.import_utils import get_cached_user_profile_model
from django_users.serializers import (
    UserProfileSerializer,
    UserCreateSerializer
)


class UserHandler:

    def __init__(self):
        self.custom_profile = get_cached_user_profile_model()

    def get_user(self, email, password):
        user_profile = self.custom_profile.objects.filter(
            user__email=email
        ).first()
        if user_profile:
            if user_profile.user.check_password(password):
                return self.generate_profile_response(user_profile)
            else:
                raise APIException(
                    "Incorrect Password",
                    "validation_failed"
                )
        else:
            raise APIException(
                "User not exists! signup instead.",
                "user_not_exists"
            )

    def crete_user(self, first_name, last_name, mobile, email, password):
        user_profile = self.custom_profile.objects.filter(
            user__email=email
        ).exists()
        if user_profile:
            raise APIException(
                "User Already exists! login instead.",
                "user_already_exists"
            )
        try:
            user = User.objects.get(
                email=email
            )
        except Exception as e:
            user_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password
            }
            user_serializer = UserCreateSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            user.set_password(password)
            user.save()
        name = self.get_full_name(first_name, last_name)
        user_profile = self.custom_profile.objects.create(
            name=name,
            user=user,
            mobile=mobile,
            is_verified=True
        )
        return self.generate_profile_response(user_profile, jwt=True)

    def generate_profile_response(self, profile, jwt=True):
        response_data = UserProfileSerializer(profile).data
        if jwt:
            tokens = self.get_tokens_for_user(profile.user)
            response_data['tokens'] = tokens
        return response_data

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    def get_full_name(self, first_name, last_name):
        if last_name:
            return first_name + ' ' + last_name
        else:
            return first_name
