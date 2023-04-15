from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from .models import User
from .jwt_manager import JWTManager


class JWTAuthentication(BaseAuthentication):
    """ Custom authentication class for DRF and JWT """

    TOKEN_PREFIX = settings.CUSTOM_JWT['TOKEN_PREFIX']
    AUTHORIZATION = 'Authorization'

    def __init__(self):
        self.jwt_manager = JWTManager()

    def authenticate(self, request):
        authorization_header = request.headers.get(self.AUTHORIZATION)

        if not authorization_header:
            return None

        headers_params = authorization_header.split(' ')
        header_token_prefix = headers_params[0]

        if header_token_prefix != self.TOKEN_PREFIX:
            raise exceptions.AuthenticationFailed('Invalid token prefix')

        if self.TOKEN_PREFIX not in header_token_prefix:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        access_token = headers_params[1]
        payload = self.jwt_manager.check_token_expire_signature(access_token, 'access')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Account does not exist')

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'Your account is not activated or deactivated, '
                'please contact the Administrator'
            )

        return user, None
