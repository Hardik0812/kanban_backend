from django.urls import path
from user.views import (
    register_user,
    check_email,
    forgot_user_password,
    reset_user_password,
    send_otp,
    verify_otp,
)
from user.auth_token import CustomTokenObtainPairView

urlpatterns = [
    path("send-otp", send_otp, name="send_otp"),
    path("verify-otp", verify_otp, name="verify_otp"),
    path("signup", register_user, name="register"),
    path("signin", CustomTokenObtainPairView.as_view(), name="login"),
    path("forgot-password", forgot_user_password, name="check_users"),
    path("reset-password", reset_user_password, name="check_users"),
    path("check-email", check_email, name="check_email"),
]
