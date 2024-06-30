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
        if not hasattr(settings, 'CUSTOM_LOGIN_URL'):
            settings.CUSTOM_LOGIN_URL = 'login/'
        if not hasattr(settings, 'CUSTOM_SIGNUP_URL'):
            settings.CUSTOM_SIGNUP_URL = 'signup/'
        if not hasattr(settings, 'CUSTOM_LOGIN_VIEW'):
            settings.CUSTOM_LOGIN_VIEW = 'django_users.views.login_view'
        if not hasattr(settings, 'CUSTOM_SIGNUP_VIEW'):
            settings.CUSTOM_SIGNUP_VIEW = 'django_users.views.signup_view'
        if not hasattr(settings, 'CUSTOM_SIGNUP_RESPONSE'):
            settings.CUSTOM_SIGNUP_RESPONSE = 'django_users.handlers.user_handler.UserHandler.generate_signup_response'
        if not hasattr(settings, 'CUSTOM_LOGIN_RESPONSE'):
            settings.CUSTOM_SIGNUP_RESPONSE = 'django_users.handlers.user_handler.UserHandler.generate_login_response'
        try:
            import_string(profile_model)
        except ImportError:
            raise ImportError(
                f"Could not import the profile model '{profile_model}' specified in CUSTOM_PROFILE_MODEL setting.")
