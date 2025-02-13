from django.urls import path
from .views import (RegisterUser, LoginUser, LogoutUser, UserProfileView, 
                    PasswordResetView, PasswordResetConfirmView, VerifyEmail)

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-confirm/<int:user_id>/<str:token>/', PasswordResetConfirmView.as_view(), name='reset-confirm'),
    path('verify-email/<int:user_id>/<str:token>/', VerifyEmail.as_view(), name='verify-email'),
]
