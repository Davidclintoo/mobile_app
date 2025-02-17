from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .models import UploadedImage
from .serializers import ImageUploadSerializer

User = get_user_model()

class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'All fields are required'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already in use'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        token = default_token_generator.make_token(user)
        verification_url = f"http://127.0.0.1:8000/api/users/verify-email/{user.pk}/{token}/"

        send_mail(
            "Email Verification",
            f"Click the link below to verify your email:\n{verification_url}",
            "clintoodavi01@gmail.com",  # Replace with your email
            [email],
            fail_silently=False,
        )

        return Response({'message': 'Verification email sent. Please check your inbox.'}, status=200)
# login
class LoginUser(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

# logout
class LogoutUser(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)

# user profile
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user
    
# password reset
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email()
            return Response({"message": "Password reset link sent to your email."}, status=200)
        return Response(serializer.errors, status=400)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_id, token):
        user = get_object_or_404(User, pk=user_id)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=400)

        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user)
            return Response({"message": "Password has been reset successfully."}, status=200)
        return Response(serializer.errors, status=400)
    
class VerifyEmail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id, token):
        user = get_object_or_404(User, pk=user_id)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=400)

        user.is_active = True
        user.save()

        return Response({"message": "Email verified successfully. You can now log in."}, status=200)
    
class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # Optionally, set a callback_url if needed
    callback_url = "http://localhost:8000/accounts/google/login/callback/"


class ImageUploadView(CreateAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)