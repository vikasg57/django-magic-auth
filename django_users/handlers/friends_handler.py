from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage
)
from django.utils import timezone
from django.db.models import Q
from django.db import transaction

from datetime import timedelta

from base.choices import BaseChoices
from base.exceptions import (
    TooManyRequestsException,
    BaseAPIException
)
from users.choices import (
    FriendRequestStatusChoices,
    FRIEND_REQUEST_STATUS_CHOICES,
    FollowerStatusChoices
)
from users.handlers.user_handler import UserHandler
from users.models import (
    FriendRequest,
    UserProfile,
    UserFollower
)


class FriendsHandler:

    def get_all_users_on_platform(self, page_num, search_term):
        profiles = UserProfile.objects.all()

        if search_term and len(search_term) > 2:
            profiles = profiles.filter(
                Q(user__email__icontains=search_term) |
                Q(name__icontains=search_term) |
                Q(mobile__icontains=search_term)
            )
        # pagination
        paginator = Paginator(profiles, 10)
        try:
            paginated_response = paginator.page(page_num)
        except PageNotAnInteger:
            paginated_response = paginator.page(1)
        except EmptyPage:
            paginated_response = paginator.page(paginator.num_pages)

        response_data = dict()
        response_data['profiles'] = [
            UserHandler().generate_profile_response(profile, jwt=False) for profile in
            paginated_response.object_list]
        response_data['total_pages'] = paginator.num_pages
        response_data['current_page'] = int(page_num)
        return response_data

    def get_all_friends_for_user(self, user, page_num, search_term):
        user_followers = UserFollower.objects.filter(
            profile=user.profile
        )

        if search_term and len(search_term) > 2:
            user_followers = user_followers.filter(
                Q(followed_by__user__email__icontains=search_term) |
                Q(followed_by__name__icontains=search_term) |
                Q(followed_by__mobile__icontains=search_term)
            )

        paginator = Paginator(user_followers, 10)
        try:
            paginated_response = paginator.page(page_num)
        except PageNotAnInteger:
            paginated_response = paginator.page(1)
        except EmptyPage:
            paginated_response = paginator.page(paginator.num_pages)

        response_data = dict()
        response_data['friends'] = [
            {**UserHandler().generate_profile_response(
                user_follower.followed_by, jwt=False),
             'is_close_friend': user_follower.is_close_friend,
             'followed_date': user_follower.followed_date
             } for user_follower in
            paginated_response.object_list]
        response_data['total_pages'] = paginator.num_pages
        response_data['current_page'] = int(page_num)
        return response_data

    def get_all_pending_friend_requests(self, user, page_num, search_term):
        pending_friend_requests = FriendRequest.objects.filter(
            to_user=user.profile,
            status=FriendRequestStatusChoices.PENDING
        )
        paginator = Paginator(pending_friend_requests, 10)
        try:
            paginated_response = paginator.page(page_num)
        except PageNotAnInteger:
            paginated_response = paginator.page(1)
        except EmptyPage:
            paginated_response = paginator.page(paginator.num_pages)

        response_data = dict()
        response_data['pending_requests'] = [
            {**UserHandler().generate_profile_response(
                pending_friend_request.from_user, jwt=False),
                'request_id': pending_friend_request.uuid
        } for pending_friend_request in
            paginated_response.object_list]
        response_data['total_pages'] = paginator.num_pages
        response_data['current_page'] = int(page_num)
        return response_data

    def send_friend_request(self, user, to_profile_id):
        to_profile = UserProfile.objects.get(uuid=to_profile_id)
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if FriendRequest.objects.filter(
                from_user=user.profile, to_user=to_profile).exists():
            raise BaseAPIException(
                'Friend request already sent.',
                'request_already_exists')

        recent_requests_count = FriendRequest.objects.filter(
            from_user=user.profile,
            created_at__gte=one_minute_ago).count()

        if recent_requests_count >= 3:
            raise TooManyRequestsException(
                'You can not send more than 3 friend requests within a minute.',
                'too_many_requests')

        friend_request = FriendRequest.objects.create(
            from_user=user.profile,
            to_user=to_profile)
        return self.generate_friend_request_response(friend_request)

    def generate_friend_request_response(self, friend_request):
        return {
            **UserHandler().generate_profile_response(friend_request.to_user, jwt=False),
            'request_id': friend_request.uuid,
            'status': BaseChoices.get_choice_str(
                FRIEND_REQUEST_STATUS_CHOICES, friend_request.status)
        }

    def take_action_on_friend_request(self, user, request_id, action):
        action = BaseChoices.get_choice_value(
            FRIEND_REQUEST_STATUS_CHOICES, action)
        try:
            with transaction.atomic():
                friend_request = FriendRequest.objects.get(
                    uuid=request_id,
                )
                if friend_request.status == FriendRequestStatusChoices.ACCEPTED:
                    raise BaseAPIException(
                        "Friend Request already accepted",
                        "request_already_accepted"
                    )

                if friend_request.status == FriendRequestStatusChoices.REJECTED:
                    raise BaseAPIException(
                        "Friend Request already Rejected",
                        "request_already_rejected"
                    )

                friend_request.status = action
                friend_request.save()
                if friend_request.status == FriendRequestStatusChoices.ACCEPTED:
                    UserFollower.objects.update_or_create(
                        profile=friend_request.from_user,
                        followed_by=friend_request.to_user,
                        defaults={
                            'followed_date': timezone.now().date(),
                            'status': FollowerStatusChoices.FOLLOWING
                    })
            return self.generate_friend_request_response(friend_request)

        except Exception as e:
            if e.args[0] in ("Friend Request already Rejected",
                             "Friend Request already accepted"):
                raise BaseAPIException(
                    e,
                    "error_while_processing_request"
                )
            else:
                raise BaseAPIException(
                    "Error while processing request",
                    "error_while_processing_request"
                )

    def get_all_block_friends(self):
        pass

    def get_all_close_friends(self):
        pass
