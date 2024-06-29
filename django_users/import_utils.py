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
