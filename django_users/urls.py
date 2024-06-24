from django.urls import path

from users.views import (
    AllUsersView,
    AuthSignUpView,
    AuthLogInView,
    FriendsView,
    PendingFriendRequestView,
    FriendRequestActionView
)

urlpatterns = [
    # Onboarding
    path("signup/", AuthSignUpView.as_view(), name="signup"),
    path("login/", AuthLogInView.as_view(), name="login"),

    # Networking
    path("get_all/", AllUsersView.as_view(), name="all_users"),
    path("get/friends/", FriendsView.as_view(), name="all_friends"),
    path("get/pending_requests/", PendingFriendRequestView.as_view(), name="pending_requests"),
    path("send_request/", FriendsView.as_view(), name="all_friends"),
    path("request/<uuid:request_id>/action/", FriendRequestActionView.as_view(), name="all_friends"),

]
