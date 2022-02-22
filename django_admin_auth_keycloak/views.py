import requests
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.conf import settings
from allauth.socialaccount.models import SocialToken
from django.contrib.sessions.models import Session
from django_admin_auth_keycloak.utils import get_keycloak_tokens, \
    get_user_from_django_session
from django_admin_auth_keycloak.constants import KEYCLOAK_LOGOUT_END_POINT


def logout_from_keycloak(user):

    access_token, refresh_token = get_keycloak_tokens(user)
    headers = {"Authorization": "Bearer {}".format(access_token)}

    data = {
      "client_id": settings.KEYCLOAK.get("CLIENT_ID"),
      "client_secret": settings.KEYCLOAK.get("CLIENT_SECRET"),
      "refresh_token": refresh_token
    }
    url = settings.KEYCLOAK["BASE_URL"] + KEYCLOAK_LOGOUT_END_POINT
    response = requests.post(url, data=data, headers=headers)

    return True


def logout_view(request):
    user = get_user_from_django_session(request)
    logout_from_keycloak(user)
    result = logout(request)
    response = redirect('admin/logout/')

    return response
