from django.core.exceptions import ValidationError
import re


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Password length should be at most 8 characters.")
        if not any(char.isupper() for char in password):
            raise ValidationError(
                "Password should contain at least one uppercase letter."
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                "Password should contain at least one lowercase letter."
            )
        if not re.search(r"[!@#$%^&*()_+=\[\]{};':\",./<>?|\\]", password):
            raise ValidationError({"error":"Password should contain at least one special character."}
            )

    def get_help_text(self):
        return "Your password must be at most 8 characters and contain at least one uppercase letter, one lowercase letter, and one special character."
