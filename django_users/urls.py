from django.urls import path

from django_users.views import (
    AuthSignUpView,
    AuthLogInView,
)

urlpatterns = [
    # Onboarding
    path("signup/", AuthSignUpView.as_view(), name="signup"),
    path("login/", AuthLogInView.as_view(), name="login")
]
