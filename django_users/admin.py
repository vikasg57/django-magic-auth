from django.contrib import admin
from base.admin import BaseModelAdmin
from users.models import UserProfile, UserFollower, FriendRequest


@admin.register(UserProfile)
class UserProfileAdmin(BaseModelAdmin):
    search_fields = ('uuid', 'user__email', 'mobile', 'name', 'is_verified')
    list_display = (
        'uuid', 'user', 'mobile', 'name', 'is_verified')


@admin.register(UserFollower)
class UserFollowerAdmin(BaseModelAdmin):
    search_fields = (
        'uuid', 'profile__user__email', 'followed_by__user__email', 'name', 'is_verified')
    list_display = (
        'uuid', 'profile', 'followed_by', 'status')


@admin.register(FriendRequest)
class FriendRequestAdmin(BaseModelAdmin):
    search_fields = (
        'uuid', 'from_user__user__email', 'to_user__user__email')
    list_display = (
        'uuid', 'from_user', 'to_user', 'status')
