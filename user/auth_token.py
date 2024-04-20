from django.utils.timezone import now
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs["email"] = attrs.get("email").lower()
        data = {}
        try:
            token = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(
                {
                    "success": False,
                    "message": "Please enter valid credentials",
                    "data": [],
                }
            )

        token.update(
            {
                "userData": {
                    "user_id": self.user.id,
                    "email": self.user.email,
                    "full_name": self.user.full_name,
                    "last_login": self.user.last_login,
                    "is_active": self.user.is_active,
                    "email_verified": self.user.email_verified,
                }
            }
        )
        self.user.last_login = now()
        self.user.token = token["access"]
        self.user.save()
        token.update()
        data["success"] = True
        data["message"] = "Login Successful"
        data["data"] = token
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
