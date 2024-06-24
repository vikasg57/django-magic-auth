from django.contrib.auth.models import User
from django.db import models
from base.models import AbstractBaseModel
from users.choices import (
    FOLLOWER_STATUS_CHOICES,
    FollowerStatusChoices,
    FRIEND_REQUEST_STATUS_CHOICES,
    FriendRequestStatusChoices
)


class UserProfile(AbstractBaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(
        max_length=20, unique=True, null=True, blank=True, db_index=True)
    name = models.CharField(
        max_length=200, null=False, blank=False, db_index=True)
    profile_url = models.URLField(max_length=2048, null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def email(self):
        return self.user.email

    @property
    def last_name(self):
        return self.user.last_name


class UserFollower(AbstractBaseModel):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="user_profile",
    )
    followed_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="followed_by",
    )
    followed_date = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    unfollowed_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(
        choices=FOLLOWER_STATUS_CHOICES,
        default=FollowerStatusChoices.FOLLOWING
    )
    is_close_friend = models.BooleanField(default=False)


class FriendRequest(AbstractBaseModel):
    from_user = models.ForeignKey(
        UserProfile, related_name='sent_requests',
        on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        UserProfile, related_name='received_requests',
        on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=FRIEND_REQUEST_STATUS_CHOICES,
        default=FriendRequestStatusChoices.PENDING
    )
