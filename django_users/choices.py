class FollowerStatusChoices:
    FOLLOWING = 0
    UN_FOLLOWED = 1
    BLOCKED = 2
    RESTRICTED = 3


FOLLOWER_STATUS_CHOICES = (
    (FollowerStatusChoices.FOLLOWING, 'FOLLOWING'),
    (FollowerStatusChoices.UN_FOLLOWED, 'UN_FOLLOWED'),
    (FollowerStatusChoices.BLOCKED, 'BLOCKED'),
    (FollowerStatusChoices.RESTRICTED, 'RESTRICTED')

)


class FriendRequestStatusChoices:
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2


FRIEND_REQUEST_STATUS_CHOICES = (
    (FriendRequestStatusChoices.PENDING, 'PENDING'),
    (FriendRequestStatusChoices.ACCEPTED, 'ACCEPTED'),
    (FriendRequestStatusChoices.REJECTED, 'REJECTED'),
)
