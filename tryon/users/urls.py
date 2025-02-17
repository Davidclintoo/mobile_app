from django.urls import path
from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.google.views import GoogleLogin
# from allauth.socialaccount.providers.facebook.views import FacebookLogin
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from .views import (RegisterUser, LoginUser, LogoutUser, UserProfileView, 
                    PasswordResetView, PasswordResetConfirmView, VerifyEmail, GoogleLoginView, ImageUploadView)

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-confirm/<int:user_id>/<str:token>/', PasswordResetConfirmView.as_view(), name='reset-confirm'),
    path('verify-email/<int:user_id>/<str:token>/', VerifyEmail.as_view(), name='verify-email'),
    path('social/google/', GoogleLoginView.as_view(), name='google-login'),
    # path('social/facebook/', FacebookLogin.as_view(), name='facebook-login'),
    path('upload-image/', ImageUploadView.as_view(), name='upload-image'),
]
