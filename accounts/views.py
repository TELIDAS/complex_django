from rest_framework import permissions, views, response, status

from . import serializers


class UserView(views.APIView):
    """ User info view """

    serializer_class = serializers.UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class CreateTokenView(views.APIView):
    """ View for create jwt access and refresh token """

    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        serializer = serializers.TokenCreateSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        result = {
            'access': validated_data['access'],
            'refresh': validated_data['refresh']
        }
        return response.Response(result, status=status.HTTP_202_ACCEPTED)


class TokenRefreshView(views.APIView):
    """ View for refresh jwt access token """

    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        serializer = serializers.TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)
