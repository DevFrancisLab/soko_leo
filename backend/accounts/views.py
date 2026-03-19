from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer


class LoginView(TokenObtainPairView):
	"""Expose the standard JWT token pair endpoint."""


class RegisterView(APIView):
    """Register a new user."""

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
	"""Blacklist a refresh token to log out the user."""

	def post(self, request, *args, **kwargs):
		refresh_token = request.data.get("refresh")
		if not refresh_token:
			return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)

		try:
			token = RefreshToken(refresh_token)
			token.blacklist()
		except Exception:
			return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

		return Response(status=status.HTTP_205_RESET_CONTENT)
	"""Blacklist a refresh token to log out the user."""

	def post(self, request, *args, **kwargs):
		refresh_token = request.data.get("refresh")
		if not refresh_token:
			return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)

		try:
			token = RefreshToken(refresh_token)
			token.blacklist()
		except Exception:
			return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

		return Response(status=status.HTTP_205_RESET_CONTENT)
