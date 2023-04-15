from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from rest_framework.exceptions import AuthenticationFailed, APIException

import jwt

from .models import User


class JWTManager:
    """ Service for work with jwt token """

    ALGORITHM = settings.CUSTOM_JWT['ALGORITHM']
    SECRET_KEY = settings.SECRET_KEY
    ACCESS_TOKEN_MINUTE = settings.CUSTOM_JWT['ACCESS_TOKEN_MINUTE']
    REFRESH_TOKEN_MINUTE = settings.CUSTOM_JWT['REFRESH_TOKEN_MINUTE']

    def generate_token(self, user, token_type: str):
        assert token_type is not None, 'token_type should not be None'
        if user is None:
            raise APIException("User does not exist")
        else:
            token_type_map = {'access': self.ACCESS_TOKEN_MINUTE, 'refresh': self.REFRESH_TOKEN_MINUTE}
            payload = self.__generate_payload(user=user, token_lifetime=token_type_map[token_type])
            token = jwt.encode(payload, self.SECRET_KEY, self.ALGORITHM)
            return token

    def check_token_expire_signature(self, token: str, token_type: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, self.ALGORITHM)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(f'{token_type.title()} token expired, please login again')
        except jwt.InvalidSignatureError:
            raise AuthenticationFailed(f'Invalid {token_type} token')
        return payload

    @staticmethod
    def __generate_payload(user: User, token_lifetime: int):
        tz_now = timezone.now()
        minute_for_add = timedelta(minutes=token_lifetime)
        payload = {'user_id': user.id, 'exp': tz_now + minute_for_add, 'iat': tz_now}
        return payload
