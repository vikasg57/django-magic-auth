from rest_framework import status
from base.response import APIResponse

from base.views import AbstractAPIView
from users.handlers.friends_handler import FriendsHandler
from users.handlers.user_handler import UserHandler
from rest_framework.permissions import AllowAny

from users.permissions import IsRequestOwner


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


class AllUsersView(AbstractAPIView):

    def get(self, request, *args, **kwargs):
        page_num = request.GET.get('page_num') or 1
        search_term = request.GET.get('search_term')
        data = FriendsHandler().get_all_users_on_platform(
            page_num, search_term)
        return APIResponse(data=data, status=status.HTTP_200_OK)


class FriendsView(AbstractAPIView):
    def get(self, request, *args, **kwargs):
        page_num = request.GET.get('page_num') or 1
        search_term = request.GET.get('search_term')
        user = request.user
        data = FriendsHandler().get_all_friends_for_user(
            user, page_num, search_term)
        return APIResponse(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        to_profile_id = request.data.get('to_profile_id')
        user = request.user
        data = FriendsHandler().send_friend_request(
            user, to_profile_id)
        return APIResponse(data=data, status=status.HTTP_200_OK)


class PendingFriendRequestView(AbstractAPIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        page_num = request.GET.get('page_num') or 1
        search_term = request.GET.get('search_term')
        data = FriendsHandler().get_all_pending_friend_requests(
            user, page_num, search_term)
        return APIResponse(data=data, status=status.HTTP_200_OK)


class FriendRequestActionView(AbstractAPIView):
    permission_classes = (IsRequestOwner, )

    def post(self, request, *args, **kwargs):
        user = request.user
        request_id = kwargs.get("request_id")
        action = request.data.get("action")
        data = FriendsHandler().take_action_on_friend_request(user, request_id, action)
        return APIResponse(data=data, status=status.HTTP_200_OK)
