import json
import jwt
import os
import requests
from allauth.socialaccount.models import SocialToken
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from urllib.request import urlopen


class DjangoAdminAuthKeycloak(BaseBackend):
    def __init__(self):
        self.public_key = self.get_keycloak_public_key()

    def authenticate(self, request, **credentials):
        try:
            return self.validate_sso_tokens(credentials.get("user"))
        except Exception as e:
            pass
        return None

    @classmethod
    def get_keycloak_public_key(cls):
        try:
            url = settings.KEYCLOAK[
                      "BASE_URL"] + '/auth/realms/' + 'dehaat'
            json_url = urlopen(url)
            data = json.loads(json_url.read())
        except Exception as e:
            msg = "Not able to acquire Keycloak Public Key"
            raise Exception(msg)

        return '-----BEGIN PUBLIC KEY-----\n' + data[
            "public_key"] + '\n-----END PUBLIC KEY-----'

    def refresh_toekn(self, refresh_toekn):
        data = {
            "client_id": settings.KEYCLOAK.get("CLIENT_ID"),
            "client_secret": settings.KEYCLOAK.get("CLIENT_SECRET"),
            "grant_type": "refresh_token",
            "refresh_token": refresh_toekn
        }
        realm_name = 'dehaat'
        response = requests.post(
            settings.KEYCLOAK["BASE_URL"]
            + settings.KEYCLOAK["ENDPOINTS"][
                "acquire_service_token"].format(
                realm_name
            ),
            data=data,
        )
        if response.status_code not in {
            200,
        }:
            return None

        token_info = response.json()

        return token_info

    def validate_sso_tokens(self, user):
        try:
            result = list(SocialToken.objects.filter(account__user=user,
                                          account__provider="keycloak"))

            access_token = result[0].token
            refresh_token = result[0].token_secret

            public_key = self.public_key
            decoded_access_token = jwt.decode(access_token, public_key,
                                              audience="account",
                                              algorithms=["RS256"])
        except jwt.exceptions.ExpiredSignatureError:
            msg = 'Token is expired.'
            try:
                self.refresh_toekn(refresh_token)
            except Exception as e:
                return None

        return User.objects.get(pk=user)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
