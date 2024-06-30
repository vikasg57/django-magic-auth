from django.conf import settings
from django.utils.module_loading import import_string


def get_user_profile_model():
    profile_model = getattr(
        settings, 'CUSTOM_PROFILE_MODEL', 'django_users.models.UserProfile')
    return import_string(profile_model)


_user_profile_model = None


def get_cached_user_profile_model():
    global _user_profile_model
    if _user_profile_model is None:
        _user_profile_model = get_user_profile_model()
    return _user_profile_model


def get_login_view():
    return import_string(settings.CUSTOM_LOGIN_VIEW)


def get_signup_view():
    return import_string(settings.CUSTOM_SIGNUP_VIEW)


def get_signup_response(profile, jwt=False, *args, **kwargs):
    response_generator = import_string(settings.CUSTOM_SIGNUP_RESPONSE)
    return response_generator(profile, jwt, *args, **kwargs)


def get_login_response(profile, jwt=False, *args, **kwargs):
    response_generator = import_string(settings.CUSTOM_LOGIN_RESPONSE)
    return response_generator(profile, jwt, *args, **kwargs)
