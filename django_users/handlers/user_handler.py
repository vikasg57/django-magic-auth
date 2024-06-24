from rest_framework.exceptions import APIException

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from django_users.models import UserProfile


class UserHandler:
    def get_user(self, email, password):
        user_profile = UserProfile.objects.filter(
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
        user_profile = UserProfile.objects.filter(
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
            user = User.objects.create(
                first_name=first_name, last_name=last_name, username=email, email=email
            )
        user.set_password(password)
        user.save()
        name = self.get_full_name(first_name, last_name)
        user_profile = UserProfile.objects.create(
            name=name,
            user=user,
            mobile=mobile,
            is_verified=True
        )
        return self.generate_profile_response(user_profile, jwt=True)

    def generate_profile_response(self, profile, jwt=True):
        response = {
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name,
            "mobile": profile.mobile,
            "email": profile.email,
            "uuid": str(profile.uuid),
        }
        if jwt:
            self.get_tokens_for_user(profile.user, response)
        return response

    def get_tokens_for_user(self, user, response):
        refresh = RefreshToken.for_user(user)
        response["refresh"] = (str(refresh),)
        response["access"] = str(refresh.access_token)

    def get_full_name(self, first_name, last_name):
        if last_name:
            return first_name + ' ' + last_name
        else:
            return first_name
