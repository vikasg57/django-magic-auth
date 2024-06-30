from django.urls import path
from django_users.import_utils import get_login_view, get_signup_view
from django.conf import settings

urlpatterns = [
    # Onboarding
    path(settings.CUSTOM_LOGIN_URL, get_login_view().as_view(), name='login'),
    path(settings.CUSTOM_SIGNUP_URL, get_signup_view().as_view(), name='signup'),
]
