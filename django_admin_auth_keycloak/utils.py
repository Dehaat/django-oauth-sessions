from django.contrib.sessions.models import Session
from allauth.socialaccount.models import SocialToken


def get_user_from_django_session(request):
    session_key = request.COOKIES.get("sessionid")
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded()
    user = uid["_auth_user_id"]

    return user


def get_keycloak_tokens(user):
    access_token = refresh_token = None
    social_token = SocialToken.objects.filter(account__user=user,
                                              account__provider="keycloak").first()

    if social_token:
        access_token = social_token.token
        refresh_token = social_token.token_secret

    return access_token, refresh_token
