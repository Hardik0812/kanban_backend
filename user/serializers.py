from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from user.models import User


class BasePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "password",
            "confirm_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match.")
        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"error": str(e)[2:-2]})
        return data


class UserRegistrationSerializer(BasePasswordSerializer):
    class Meta(BasePasswordSerializer.Meta):
        fields = [
            "full_name",
            "email",
            "password",
            "confirm_password",
        ]

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        return user


class ResetPasswordSerializer(BasePasswordSerializer):
    class Meta(BasePasswordSerializer.Meta):
        fields = ["password", "confirm_password", "token"]
