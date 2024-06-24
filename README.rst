============
django-users
============

django-users is a Django app for smooth users onboarding.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "users" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_users",
    ]

2. Include the users URLconf in your project urls.py like this::

    path("users/", include("django_users.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a maage users.

5. Visit the ``/users/`` URL to participate in the users