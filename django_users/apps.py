from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_users"
    label = "users"

    def ready(self):
        profile_model = getattr(
            settings, 'CUSTOM_PROFILE_MODEL', 'django_users.models.UserProfile')
        try:
            import_string(profile_model)
        except ImportError:
            raise ImportError(
                f"Could not import the profile model '{profile_model}' specified in CUSTOM_PROFILE_MODEL setting.")
