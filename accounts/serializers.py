from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework import exceptions

from . import models, jwt_manager


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'username',)


class TokenCreateSerializer(serializers.Serializer, jwt_manager.JWTManager):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        if not email or not password:
            raise exceptions.APIException('Both "email" and "password" are required')

        user = authenticate(request=request, email=email, password=password)

        if not user:
            try:
                db_user = models.User.objects.get(email=email)
                db_user.password = make_password(db_user.password)
                if not db_user.is_active:
                    raise exceptions.AuthenticationFailed(
                        'Your account is not activated or deactivated, '
                        'please contact the Administrator'
                    )
                if not db_user.check_password(password):
                    raise exceptions.APIException('Access denied: wrong email or password')
            except models.User.DoesNotExist:
                raise exceptions.APIException('User with this email doe`s not exist')

        attrs['access'] = self.generate_token(user, 'access')
        attrs['refresh'] = self.generate_token(user, 'refresh')

        return attrs


class TokenRefreshSerializer(serializers.Serializer, jwt_manager.JWTManager):
    """ Serializer for validate refresh jwt token and check user """

    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')

        if refresh_token is None:
            raise exceptions.AuthenticationFailed('Refresh token were not provided')

        payload = self.check_token_expire_signature(refresh_token, token_type='refresh')

        try:
            user = models.User.objects.get(id=payload.get('user_id'))
        except models.User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exist')

        attrs['access'] = self.generate_token(user, 'access')

        return attrs
