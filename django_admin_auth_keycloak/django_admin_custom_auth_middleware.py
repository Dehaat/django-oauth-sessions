from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse

from django_admin_auth_keycloak.backends import DjangoAdminAuthKeycloak
from django_admin_auth_keycloak.utils import get_user_from_django_session

class DjangoAdminCustomAuthMiddleware:
    def __init__(self, get_response):
        if not settings.KEYCLOAK or not settings.KEYCLOAK.get(
                'BASE_URL') \
                or not settings.KEYCLOAK.get('CLIENT_ID'):
            raise ImproperlyConfigured(
                "Keycloak configuration missing in"
                " setting file. Plz make sure that "
                "the following is there in keycloak"
                "setting BASE_URL,CLIENT_ID,CLIENT_SECRET"
                "acquire_service_token endpoint.")
        self.get_response = get_response
        self.custom_auth_obj = DjangoAdminAuthKeycloak()

    def __call__(self, request):
        try:
            if hasattr(request, "COOKIES") and request.COOKIES.get(
                    "sessionid") \
                    and self.check_request_path(request):
                user = get_user_from_django_session(request)
                if not self.custom_auth_obj.authenticate(request,
                                                         user=user):
                    session_key = request.COOKIES.get("sessionid")
                    Session.objects.filter(
                        session_key=session_key).delete()
                    return redirect('login')
        except Session.DoesNotExist as e:
            pass
        except Exception as e:
            return redirect(reverse('login'))

        response = self.get_response(request)

        return response


    def check_request_path(self, request):
        parts = set(request.path.split("/"))

        if "login" in parts or "keycloak" in parts:
            return False
        if "admin" in parts:
            return True

        return False
