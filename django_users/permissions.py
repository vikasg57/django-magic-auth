from rest_framework import permissions

from users.models import FriendRequest


class IsRequestOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            friend_request = FriendRequest.objects.get(
                uuid=view.kwargs.get('request_id')
            )
        except Exception as e:
            return False
        return friend_request.to_user.user == request.user

    def has_object_permission(self, request, view, obj):
        return True
