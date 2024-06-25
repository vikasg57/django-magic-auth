from rest_framework import status
from django_users.response import APIResponse
from rest_framework.exceptions import APIException
import re

from django.utils.html import strip_tags
from django.core.validators import validate_email
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django_users.handlers.user_handler import UserHandler


class AbstractAPIView(APIView):

    def get_bool_query_value(self, param_str):
        value = self.request.GET.get(param_str)
        if value == 'false' or value == 'False' or not value:
            return False
        return True

    def get_bool_value_from_string(self, value):
        if value == 'false' or value == 'False' or not value:
            return False
        return True

    def get_sanitized_string(self, data_string, is_param_str=False):
        start_url_pattern = r'(?:http://\S+|https://\S+|www\.\S+)'
        end_url_pattern = r'\S+(?:\.com|\.org|\.net|\.gov|\.edu|\.mil|\.int|\.uk|\.ca|\.au|\.in|\.de|\.jp|\.fr|\.it|' \
                          r'\.es|\.nl|\.se|\.no|\.dk|\.br|\.ru|\.cn|\.kr|\.sg|\.hk|\.tw|\.io|\.me|\.info|\.biz|' \
                          r'\.coop|\.museum|\.aero|\.name)'
        match_symbol_pattern = r'[\{\}\[\]\(\)://<>]'
        if is_param_str:
            string = self.request.GET.get(data_string)
        else:
            string = self.request.data.get(data_string)
        if string:
            string = strip_tags(string)
            string = re.sub(start_url_pattern, '', string)
            string = re.sub(end_url_pattern, '', string)
            string = re.sub(match_symbol_pattern, '', string)
            string = string.strip()
            return string

    def get_email(self, email):
        email = email.lower()
        if email is not None:
            try:
                validate_email(email)
            except Exception as e:
                raise APIException(
                    'Enter a valid email address.', 'validation_failed'
                )
        return email


class AuthLogInView(AbstractAPIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = self.get_email(request.data.get("email"))
        password = request.data.get("password")
        data = UserHandler().get_user(email, password)
        return APIResponse(data=data, status=status.HTTP_200_OK)


class AuthSignUpView(AbstractAPIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        mobile = request.data.get("mobile")
        password = request.data.get("password")
        email = self.get_email(request.data.get("email"))
        data = UserHandler().crete_user(
            first_name, last_name, mobile, email, password)
        return APIResponse(data=data, status=status.HTTP_200_OK)
