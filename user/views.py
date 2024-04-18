from django.db import transaction
from django.utils import timezone

from datetime import timedelta

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user.models import OtpModel, User

from utils.send_mail import (
    send_otp_email,
    send_verification_email,
    send_forgot_password_email,
)
from utils.helpers import decode_token, generate_otp

from .serializers import ResetPasswordSerializer, UserRegistrationSerializer

import threading


@transaction.atomic
@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        try:
            data = request.data
            email = data.get("email").lower()

            if User.objects.filter(email=email.lower()).exists():
                return Response(
                    {
                        "success": False,
                        "message": "Email already exists",
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            otp_record = OtpModel.objects.filter(email=email).first()
            print(otp_record)

            if not otp_record.verified:
                return Response(
                    {
                        "success": False,
                        "message": "Please verified email address",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

            serializer = UserRegistrationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success": True, "message": "Successfully sign up"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"Error occurred when registaring user" + str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["POST"])
def check_email(request):
    if request.method == "POST":
        try:
            email = request.data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                return Response(
                    {
                        "message": "This email is already Register",
                        "success": False,
                    },
                    status=status.HTTP_409_CONFLICT,
                )
            return Response(
                {
                    "message": "This Email is not Register",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
def forgot_user_password(request):
    if request.method == "POST":
        email = request.data["email"]
        try:
            user = User.objects.get(email=email)
            if user:
                context = {
                    "email": user.email,
                    "name": user.first_name,
                }
                thread = threading.Thread(
                    target=send_forgot_password_email,
                    args=("Forgot Password Link", "forgot-password-link.html", context),
                )
                thread.start()
                return Response(
                    {
                        "message": "Reset password link sent to email.",
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
        except User.DoesNotExist:
            return Response(
                {
                    "message": "User with this email does not exist.",
                    "success": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

@transaction.atomic
@api_view(["POST"])
def reset_user_password(request):
    if request.method == "POST":
        try:
            data = request.data
            decode = decode_token(data["token"])
            if decode:
                user = User.objects.get(email=decode["email"])
                serializer = ResetPasswordSerializer(data=data)
                if serializer.is_valid():
                    user.set_password(serializer.validated_data["password"])
                    user.save()
                    return Response(
                        {
                            "message": "Password reset successful",
                            "success": True,
                        },
                        status=status.HTTP_200_OK,
                    )
                print(serializer.errors.values())
                error_message = ",".join(
                    [value[0] for value in serializer.errors.values()]
                )
                return Response(
                    {"error": error_message, "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "Invalid token", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
def send_otp(request):
    try:
        email = request.data.get("email").lower()
        otp = generate_otp()

        expiration_time = timezone.now() + timedelta(minutes=5)
        expires_timestamp = expiration_time.timestamp()

        save_otp = OtpModel.objects.create(
            email=email, otp=otp, expires=expires_timestamp
        )
        context = {"otp": save_otp.otp, "email": save_otp.email}
        email_thread = threading.Thread(
            target=send_otp_email,
            args=("Otp", "send-otp.html", context),
        )
        email_thread.start()

        return Response(
            {
                "success": True,
                "message": "OTP sent successfully",
                "data": [{"expires": save_otp.expires}],
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {
                "success": False,
                "message": "Error occurred when send otp",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def verify_otp(request):
    try:
        otp = request.data.get("otp")
        email = request.data.get("email").lower()
        expire_time = timezone.now()

        otp_record = (
            OtpModel.objects.filter(email=email, expires__gte=expire_time.timestamp())
            .order_by("createdAt")
            .last()
        )

        if otp_record:
            if otp_record.verified:
                return Response(
                    {"success": False, "message": "OTP already verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if otp_record.otp == otp:
                otp_record.verified = True
                otp_record.save()
                return Response(
                    {"success": True, "message": "OTP verified successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"success": False, "message": "Invalid OTP"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"success": False, "message": "OTP has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response(
            {"success": False, "message": "Error occurred when verify otp"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
