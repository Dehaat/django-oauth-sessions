=====
Custom Keycloak Auth
=====

django_admin_auth_keycloak is a Django app to validate SSO tokens.


Quick start
-----------

1. Add "django_admin_auth_keycloak" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_admin_auth_keycloak',
    ]

2. Add following middleware in your settings file

    MIDDLEWARE = [
        ...
        'django_admin_auth_keycloak.django_admin_custom_auth_middleware.DjangoAdminCustomAuthMiddleware',
]

3. Update the logout url in urls.py as
        path('admin/logout/', logout_view, name='logout')
    import logout_view from django_admin_auth_keycloak
    e.g from django_admin_auth_keycloak.views import logout_view

4. Start the development server and visit http://localhost:8000/admin/
   to create a django_admin_auth_keycloak (you'll need the Admin app enabled).
