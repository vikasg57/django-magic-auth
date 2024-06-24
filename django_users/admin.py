from django.contrib import admin
from django_users.models import UserProfile


class BaseModelAdmin(admin.ModelAdmin):
    default_readonly_fields = ('created_at', 'uuid')
    ordering = ('-created_at',)
    search_fields = ('uuid',)
    readonly_fields = ('uuid', 'created_at', 'updated_at')

    foreign_key_fields = ()


@admin.register(UserProfile)
class UserProfileAdmin(BaseModelAdmin):
    search_fields = ('uuid', 'user__email', 'mobile', 'name', 'is_verified')
    list_display = (
        'uuid', 'user', 'mobile', 'name', 'is_verified')
